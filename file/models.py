from django.db import models

from order.models import Order


class File(models.Model):
    INPUT = 1
    OUTPUT = 2

    choices = (
        (INPUT, 'ورودی'),
        (OUTPUT, 'خروجی'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='files')
    file_type = models.PositiveSmallIntegerField(choices=choices, default=INPUT)
    file = models.FileField(upload_to='files/%Y/%m/%d', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name