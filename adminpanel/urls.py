from django.urls import path

from adminpanel.views import (OrderListAdminView,PaymentListAdminView,
                              LanguageListAdminView, FormatListAdminView, UserListAdminView,
                              OrderDetailAdminView, OrderUploadFileAdmin, LanguageAddAdminView,
                              LanguageEditAdminView, LanguageDeleteAdminView, FormatAddAdminView,
                              FormatEditAdminView, FormatDeleteAdminView, UserEditAdminView, UserDeleteAdminView)

urlpatterns = [
    path('order/list/', OrderListAdminView.as_view(), name='order-list-admin'),
    path('order/<int:pk>/', OrderDetailAdminView.as_view(), name='order-detail-admin'),
    path('order/<int:pk>/file-upload/', OrderUploadFileAdmin.as_view(), name='order-file-upload-admin'),

    path('payment/list/', PaymentListAdminView.as_view(), name='payment-list-admin'),

    path('language/list/', LanguageListAdminView.as_view(), name='language-list-admin'),
    path('language/add/', LanguageAddAdminView.as_view(), name='language-add-admin'),
    path('language/<int:pk>/edit/', LanguageEditAdminView.as_view(), name='language-edit-admin'),
    path('language/<int:pk>/delete/', LanguageDeleteAdminView.as_view(), name='language-delete-admin'),

    path('format/list/', FormatListAdminView.as_view(), name='format-list-admin'),
    path('format/add/', FormatAddAdminView.as_view(), name='format-add-admin'),
    path('format/<int:pk>/edit/', FormatEditAdminView.as_view(), name='format-edit-admin'),
    path('format/<int:pk>/delete/', FormatDeleteAdminView.as_view(), name='format-delete-admin'),

    path('user/list/', UserListAdminView.as_view(), name='user-list-admin'),
    path('user/<int:pk>/edit/', UserEditAdminView.as_view(), name='user-edit-admin'),
    path('user/<int:pk>/delete/', UserDeleteAdminView.as_view(), name='user-delete-admin'),
]