from django.urls import path
from .views import NewOrderView, EstimatePriceView, OrderDetailView, OrderDownloadView


urlpatterns = [
    path('new/', NewOrderView.as_view(), name='new-order'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('price/estimate/', EstimatePriceView.as_view(), name='estimate-price'),
    path('download/<int:pk>/', OrderDownloadView.as_view(), name='download-file'),
]