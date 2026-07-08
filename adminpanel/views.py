import datetime
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum, Count
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


class UserEditAdminView(StaffRequiredMixin, View):
    template_name = 'admin/user_form.html'

    def get(self, request, pk, *args, **kwargs):
        user = User.objects.filter(pk=pk)
        if not user.exists():
            response = {"error": "کاربر یافت نشد."}
            return render(request, 'admin/users_list.html', context=response)

        user = user.first()

        return render(request, self.template_name, context={"user": user})

    def post(self, request, pk, *args, **kwargs):
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        new_password = request.POST.get('new_password')
        is_active = request.POST.get('is_active')

        user = User.objects.filter(pk=pk)
        if not user.exists():
            response = {"error": "کاربر یافت نشد."}
            return render(request, self.template_name, context=response)

        user = user.first()

        if email is None or fname is None or lname is None:
            response = {"error": "ایمیل، نام و نام خانوادگی الزامی می‌باشد.", "user": user}
            return render(request, self.template_name, context=response)

        if new_password is not None and new_password != '':
            user.set_password(new_password)

        if is_active == 'on':
            user.is_active = True
        else:
            user.is_active = False


        pattern = r'^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$'
        check = re.search(pattern, email)
        if not check:
            response = {"error": "ایمیل وارد شده معتبر نیست.", "user": user}
            return render(request, self.template_name, context=response)

        find_user = User.objects.filter(email=email)

        if find_user.exists() and user != find_user[0]:
            response = {"error": "این ایمیل قبلا ثبت شده است.", "user": user}
            return render(request, self.template_name, context=response)

        user.email = email
        user.first_name = fname
        user.last_name = lname
        user.save()

        return render(request, self.template_name, context={"user": user})


class UserDeleteAdminView(StaffRequiredMixin, View):
    template_name = 'admin/users_list.html'

    def post(self, request, pk, *args, **kwargs):
        user = User.objects.filter(pk=pk)
        if not user.exists():
            response = {"error": "کاربر یافت نشد."}
            return render(request, self.template_name, context=response)

        user = user.first()

        user.delete()
        users = User.objects.all()
        return render(request, self.template_name, context={"users": users})


class DashboardAdminView(StaffRequiredMixin, View):
    template_name = 'admin/dashboard.html'

    def get(self, request, *args, **kwargs):
        today = datetime.date.today()

        orders_today = Order.objects.filter(created_at__date=today).count()
        revenue_today = Payment.objects.filter(created_at__date=today).aggregate(total=Sum('amount'))['total'] or 0
        new_users_today = User.objects.filter(date_joined__date=today).count()

        total_orders = Order.objects.count()
        total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
        total_order_value = Order.objects.aggregate(total=Sum('estimated_price'))['total'] or 0
        total_users = User.objects.count()


        status_counts = {code: 0 for code, _ in Order.status}
        for row in Order.objects.values('order_status').annotate(count=Count('id')):
            status_counts[row['order_status']] = row['count']

        PERSIAN_WEEKDAYS = ['دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه', 'یکشنبه']
        daily_counts = []
        for i in range(6, -1, -1):
            day = today - datetime.timedelta(days=i)
            count = Order.objects.filter(created_at__date=day).count()
            daily_counts.append({'date': day, 'count': count})

        max_count = max((d['count'] for d in daily_counts), default=0) or 1
        daily_chart = [
            {
                'label': PERSIAN_WEEKDAYS[d['date'].weekday()],
                'count': d['count'],
                'height_percent': max(6, round(d['count'] / max_count * 100)),
            }
            for d in daily_counts
        ]

        return render(request, self.template_name, context={
        'orders_today': orders_today,
        'revenue_today_display': Order.toman(revenue_today),
        'new_users_today': new_users_today,
        'total_orders': total_orders,
        'total_revenue_display': Order.toman(total_revenue),
        'total_order_value_display': Order.toman(total_order_value),
        'total_users': total_users,
        'status_counts': status_counts,
        'daily_chart': daily_chart,
    })
