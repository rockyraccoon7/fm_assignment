from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import *

from .models import *
from .serializers import *

class VendorListorCreate(APIView):
    """
    API endpoint to list all vendors or create a new vendor.
    """

    def get(self, request, format=None):
        """
        Retrieve a list of all vendors.
        """
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new vendor.
        """
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecificVendor(APIView):
    """
    API endpoint to retrieve, update, or delete a specific vendor.
    """

    def get(self, request, vendor_code):
        """
        Retrieve details of a specific vendor.
        """
        vendor = Vendor.objects.get(vendor_code=vendor_code)
        serialized_data = VendorSerializer(vendor)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def put(self, request, vendor_code):
        """
        Update details of a specific vendor.
        """
        vendor = Vendor.objects.get(vendor_code=vendor_code)
        serialized_data = VendorSerializer(vendor, data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_code):
        """
        Delete a specific vendor.
        """
        vendor = Vendor.objects.get(vendor_code=vendor_code)
        vendor.delete()
        return Response(status=status.HTTP_200_OK)

class PurchaseOrders(APIView):
    """
    API endpoint to list all purchase orders or create a new purchase order.
    """

    def get(self, request, format=None):
        """
        Retrieve a list of all purchase orders.
        """
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new purchase order.
        """
        serialized_data = PurchaseOrderSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecificPurchaseOrder(APIView):
    """
    API endpoint to retrieve, update, or delete a specific purchase order.
    """

    def get(self, request, po_id):
        """
        Retrieve details of a specific purchase order.
        """
        purchase_order = PurchaseOrder.objects.get(po_number=po_id)
        serialized_data = PurchaseOrderSerializer(purchase_order)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def put(self, request, po_id):
        """
        Update details of a specific purchase order.
        """
        purchase_orders = PurchaseOrder.objects.get(po_number=po_id)
        serialized_data = PurchaseOrderSerializer(purchase_orders, data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id):
        """
        Delete a specific purchase order.
        """
        purchase_order = PurchaseOrder.objects.get(po_number=po_id)
        purchase_order.delete()
        return Response(status=status.HTTP_200_OK)

class VendorPerformance(APIView):
    """
    API endpoint to retrieve vendor performance metrics.
    """

    def get(self, request, vendor_code):
        """
        Retrieve performance metrics for a specific vendor.
        """
        metrics = HistoricalPerformance.objects.filter(vendor=Vendor.objects.get(vendor_code=vendor_code).id)
        serialized_metrics = HistoricalPerformanceSerializer(metrics, many=True)
        return Response(serialized_metrics.data, status=status.HTTP_200_OK)

class AcknowledgeOrder(APIView):
    """
    API endpoint to acknowledge a purchase order.
    """

    def post(self, request, po_id):
        """
        Acknowledge a purchase order.
        """
        purchase_order = PurchaseOrder.objects.get(po_number=po_id)
        purchase_order.acknowledgment_date = datetime.now()
        purchase_order.save()
        return Response(status=status.HTTP_200_OK)
