from django.db import models
from django.conf import settings


class Language(models.Model):
    name = models.CharField(max_length=100)
    factor = models.FloatField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class InputFormat(models.Model):
    name = models.CharField(max_length=100)
    factor = models.FloatField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    TYPE = 1
    TRANSLATE = 2

    choices = (
        (TYPE, 'تایپ'),
        (TRANSLATE, 'ترجمه'),
    )

    status = (
        ("PROGRESS", "درحال انجام"),
        ("READY", "آماده تحویل"),
        ("DELIVERED", "تحویل شده"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_type = models.PositiveSmallIntegerField(choices=choices, default=TYPE)
    order_status = models.CharField(choices=status, max_length=100, default='PROGRESS')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='orders')
    input_format = models.ForeignKey(InputFormat, on_delete=models.CASCADE, related_name='orders')
    page_count = models.IntegerField(default=0)
    estimated_price = models.IntegerField(default=0)
    estimated_days = models.IntegerField(default=0)
    paid_amount = models.IntegerField(default=0)
    remain_amount = models.IntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user}: {self.input_format} - {self.page_count}'

    class InvalidOrderInput(Exception):
        pass

    @classmethod
    def calculate_price(cls, order_type_code, pages, language_code, format_code):
        try:
            if order_type_code == 'typing':
                order_type = Order.TYPE
            elif order_type_code == 'translation':
                order_type = Order.TRANSLATE
            else:
                order_type = cls.InvalidOrderInput('نوع سفارش نامعتبر است.')
            language = Language.objects.get(id=language_code)
            input_format = InputFormat.objects.get(id=format_code)
        except (Language.DoesNotExist, InputFormat.DoesNotExist):
            raise cls.InvalidOrderInput('زبان یا فرمت فایل نامعتبر است.')

        if pages < 1:
            raise cls.InvalidOrderInput('تعداد صفحات باید حداقل ۱ باشد.')


        raw_price = order_type * 1000 * pages * float(language.factor) * float(input_format.factor)
        price = round(raw_price / 100) * 100

        if order_type == Order.TYPE:
            days = -(-pages // order_type * 0.1)
        elif order_type == Order.TRANSLATE:
            days = -(-pages // order_type * 0.2)
        else:
            days = 1

        days = 1 if days < 1 else days

        return {
            'price': int(price),
            'days': int(days),
            'half_payment': int(round(price / 2 / 100) * 100),
        }

    @classmethod
    def toman(cls, amount):
        return f'{int(amount or 0):,} تومان'