from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from .models import *
from .serializers import *


class VendorListorCreate(APIView):
    """
    List all Transformers, or create a new Transformer
    """

    def get(self, request, format=None):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecificVendor(APIView):

    def get(self, request, vendor_code):
        vendor = Vendor.objects.get(vendor_code=vendor_code)
        serialized_data = VendorSerializer(vendor)
        return Response(serialized_data.data)

    def put(self, request, vendor_code):
        vendor = Vendor.objects.get(vendor_code=vendor_code)
        serialized_data = VendorSerializer(vendor, data = request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_code):
        vendor = Vendor.objects.get(vendor_code=vendor_code)
        vendor.delete()
        return Response(status=status.HTTP_200_OK)

class PurchaseOrders(APIView):

    def get(self, request, format=None):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serialized_data = PurchaseOrderSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecificPurchaseOrder(APIView):

    def get(self, request, po_id):
        purchase_order = PurchaseOrder.objects.get(po_number=po_id)
        serialized_data = PurchaseOrderSerializer(purchase_order)
        return Response(serialized_data.data)

    def put(self, request, po_id):
        purchase_orders = PurchaseOrder.objects.get(po_number=po_id)
        serialized_data = PurchaseOrderSerializer(purchase_orders, data = request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id):
        purchase_order = PurchaseOrder.objects.get(po_number=po_id)
        purchase_order.delete()
        return Response(status=status.HTTP_200_OK)

class VendorPerformance(APIView):
    def get(self, request, vendor_code):
        metrics = HistoricalPerformance.objects.filter(vendor=Vendor.objects.get(vendor_code=vendor_code).id)
        serialized_metrics = HistoricalPerformanceSerializer(metrics)
        return Response(serialized_metrics.data)

class AcknowledgeOrder(APIView):
    def post(self, request, po_id):
        purchase_order = PurchaseOrder.objects.get(po_number=po_id)
        purchase_order.acknowledgment_date = datetime.now()
        purchase_order.save()
        return Response(status=status.HTTP_200_OK)
