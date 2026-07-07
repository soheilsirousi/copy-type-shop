from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from file.models import File
from order.models import Order, Language, InputFormat
from payment.models import Payment


class StaffRequiredMixin(LoginRequiredMixin):
    login_url = '/user/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)


class OrderListAdminView(StaffRequiredMixin, View):
    template_name = 'admin/orders_list.html'

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()

        data = {"orders": orders}
        return render(request, self.template_name, context=data)


class OrderDetailAdminView(StaffRequiredMixin, View):
    template_name = 'admin/admin_order_detail.html'

    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.filter(pk=pk)
        if not order.exists():
            response = {"error": "سفارش یافت نشد."}
            return render(request, self.template_name, context=response)

        order = order.first()
        input_file = order.files.filter(file_type=File.INPUT).first()
        output_file = order.files.filter(file_type=File.OUTPUT).first()

        return render(request, self.template_name, context={"order": order, "input_file": input_file, "output_file": output_file})


class OrderUploadFileAdmin(StaffRequiredMixin, View):
    template_name = 'admin/admin_order_detail.html'

    def post(self, request, pk, *args, **kwargs):
        order = Order.objects.filter(pk=pk)
        if not order.exists():
            response = {"error": "سفارش یافت نشد."}
            return render(request, self.template_name, context=response)

        attachment = request.FILES.get('final_file')

        if not attachment:
            response = {"error": "پیوست الزامی می‌باشد."}
            return render(request, template_name=self.template_name, context=response)

        allowed_extensions = ('.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png')
        if not attachment.name.lower().endswith(allowed_extensions):
            response = {"error": "فرمت فایل مجاز نیست. فقط PDF، Word، JPG یا PNG."}
            return render(request, template_name=self.template_name, context=response)


        order = order.first()
        order.order_status = 'READY'
        order.is_complete = True
        order.completed_at = timezone.now()
        order.save()
        file = File.objects.create(order=order, file=attachment, file_type=File.OUTPUT)
        return redirect('order-detail-admin', pk=order.pk)


class PaymentListAdminView (StaffRequiredMixin, View):
    template_name = 'admin/payments_list.html'

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        return render(request, self.template_name, context={"orders": orders})


class LanguageListAdminView(StaffRequiredMixin, View):
    template_name = 'admin/languages_list.html'

    def get(self, request, *args, **kwargs):
        languages = Language.objects.all()
        return render(request, self.template_name, context={"languages": languages})

class LanguageAddAdminView(StaffRequiredMixin, View):
    template_name = 'admin/languages_list.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        factor = request.POST.get('factor')

        if name is None or factor is None:
            response = {"error": "تمامی فیلدها ضروری می‌باشند."}
            return render(request, self.template_name, context=response)

        language = Language.objects.create(name=name, factor=float(factor))
        languages = Language.objects.all()

        return render(request, self.template_name, context={"languages": languages})


class LanguageEditAdminView(StaffRequiredMixin, View):
    template_name = 'admin/languages_list.html'

    def post(self, request, pk, *args, **kwargs):
        name = request.POST.get('name')
        factor = request.POST.get('factor')

        if name is None or factor is None:
            response = {"error": "تمامی فیلدها ضروری می‌باشند."}
            return render(request, self.template_name, context=response)

        language = Language.objects.filter(pk=pk)
        if not language.exists():
            response = {"error": "زبان یافت نشد."}
            return render(request, self.template_name, context=response)

        language = language.first()
        language.name = name
        language.factor = float(factor)
        language.save()
        languages = Language.objects.all()

        return render(request, self.template_name, context={"languages": languages})


class LanguageDeleteAdminView(StaffRequiredMixin, View):
    template_name = 'admin/languages_list.html'

    def get(self, request, pk, *args, **kwargs):
        language = Language.objects.filter(pk=pk)
        if not language.exists():
            response = {"error": "زبان یافت نشد."}
            return render(request, self.template_name, context=response)

        language = language.first()
        language.delete()
        languages = Language.objects.all()

        return render(request, self.template_name, context={"languages": languages})


class FormatListAdminView(StaffRequiredMixin, View):
    template_name = 'admin/formats_list.html'

    def get(self, request, *args, **kwargs):
        formats = InputFormat.objects.all()
        return render(request, self.template_name, context={"formats": formats})


class FormatAddAdminView(StaffRequiredMixin, View):
    template_name = 'admin/formats_list.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        factor = request.POST.get('factor')

        if name is None or factor is None:
            response = {"error": "تمامی فیلدها ضروری می‌باشند."}
            return render(request, self.template_name, context=response)

        format = InputFormat.objects.create(name=name, factor=float(factor))
        formats = InputFormat.objects.all()

        return render(request, self.template_name, context={"formats": formats})


class FormatEditAdminView(StaffRequiredMixin, View):
    template_name = 'admin/formats_list.html'

    def post(self, request, pk, *args, **kwargs):
        name = request.POST.get('name')
        factor = request.POST.get('factor')

        if name is None or factor is None:
            response = {"error": "تمامی فیلدها ضروری می‌باشند."}
            return render(request, self.template_name, context=response)

        format = InputFormat.objects.filter(pk=pk)
        if not format.exists():
            response = {"error": "فرمت یافت نشد."}
            return render(request, self.template_name, context=response)

        format = format.first()
        format.name = name
        format.factor = float(factor)
        format.save()
        formats = InputFormat.objects.all()

        return render(request, self.template_name, context={"formats": formats})


class FormatDeleteAdminView(StaffRequiredMixin, View):
    template_name = 'admin/formats_list.html'

    def get(self, request, pk, *args, **kwargs):
        format = InputFormat.objects.filter(pk=pk)
        if not format.exists():
            response = {"error": "زبان یافت نشد."}
            return render(request, self.template_name, context=response)

        format = format.first()
        format.delete()
        formats = InputFormat.objects.all()

        return render(request, self.template_name, context={"formats": formats})

class UserListAdminView(StaffRequiredMixin, View):
    template_name = 'admin/users_list.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, self.template_name, context={"users": users})

