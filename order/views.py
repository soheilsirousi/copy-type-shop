from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from file.models import File
from order.models import Language, InputFormat, Order


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return redirect('profile')

class NewOrderView(LoginRequiredMixin, View):
    template_name = 'new_order.html'
    login_url = '/user/login/'

    def get(self, request, *args, **kwargs):
        languages = Language.objects.all()
        input_formats = InputFormat.objects.all()
        data = {"languages": languages, "input_formats": input_formats}
        return render(request, template_name=self.template_name, context=data)

    def post(self, request, *args, **kwargs):
        order_type_code = request.POST.get('order_type', None)
        pages = request.POST.get('pages', None)
        language_code = request.POST.get('language', None)
        format_code = request.POST.get('format', None)


        if order_type_code is None or pages is None or language_code is None or format_code is None:
            response = {"error": "مقادیر وارد شده معتبر نمی‌باشد."}
            return render(request, template_name=self.template_name, context=response)


        result = Order.calculate_price(
                order_type_code=order_type_code,
                pages=int(pages),
                language_code=int(language_code),
                format_code=int(format_code),
            )

        if order_type_code == 'typing':
            order_type = Order.TYPE
        else:
            order_type = Order.TRANSLATE

        language = Language.objects.get(id=language_code)
        input_format = InputFormat.objects.get(id=int(format_code))
        total_price = result.get('price')
        paid_price = result.get('half_payment')
        days = result.get('days')
        remaining_price = total_price - paid_price

        order = Order.objects.create(user=request.user, order_type=order_type, page_count=int(pages),
                                     language=language, input_format=input_format, estimated_price=total_price,
                                     estimated_days=days, paid_amount=paid_price, remain_amount=remaining_price)

        return redirect('order-detail', pk=order.id)


class EstimatePriceView(View):

    def get(self, request, *args, **kwargs):
        try:
            pages = int(request.GET.get('pages', 0))
            result = Order.calculate_price(
                order_type_code=request.GET.get('order_type', ''),
                pages=pages,
                language_code=request.GET.get('language', ''),
                format_code=request.GET.get('format', ''),
            )
            return JsonResponse({'ok': True, **result})
        except (Order.InvalidOrderInput, ValueError) as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)


class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'order_detail.html'
    login_url = '/user/login/'

    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.filter(pk=pk, user=request.user)
        if not order.exists():
            response = {"error": "سفارش یافت نشد."}
            return render(request, template_name=self.template_name, context=response)

        order = order.first()
        return render(request, template_name=self.template_name, context={'order': order})

    def post(self, request, pk, *args, **kwargs):
        order = Order.objects.filter(pk=pk, user=request.user)
        if not order.exists():
            response = {"error": "سفارش یافت نشد."}
            return render(request, template_name=self.template_name, context=response)

        order = order.first()

        order.order_status = 'DELIVERED'
        order.is_complete = True
        order.completed_at = timezone.now()
        order.save()

        return render(request, template_name=self.template_name, context={'order': order})


class OrderDownloadView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.filter(pk=pk, user=request.user)

        if not order.exists():
            response = {"error": "سفارش یافت نشد."}
            return render(request, template_name='order_detail.html', context=response)

        order = order.first()
        file = order.files.filter(file_type=File.OUTPUT)
        if not file.exists():
            response = {"error": "فایل یافت نشد."}
            return render(request, template_name='order_detail.html', context=response)

        file = file.first()

        return HttpResponseRedirect(file.file.url)