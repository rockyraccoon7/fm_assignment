"""
URL configuration for fm_assessment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vendors/', VendorListorCreate.as_view(), name="vendor-list"),
    path('api/vendors/<str:vendor_code>', SpecificVendor.as_view(), name="specific-vendor"),
    path('api/purchase_orders/', PurchaseOrders.as_view(), name="purchase-order-list"),
    path('api/purchase_orders/<str:po_id>', SpecificPurchaseOrder.as_view(), name="specific-purchase-order"),
    path('api/vendors/<str:vendor_code>/performance/', VendorPerformance.as_view(), name="vendor-performance"),
    path('api/purchase_orders/<str:po_id>/acknowledge/', AcknowledgeOrder.as_view(), name="acknowledge-purchase-order")
]
