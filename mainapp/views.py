from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

    def get(self, request, vendor_id):
        vendor = Vendor.objects.get(id=vendor_id)
        serialized_data = VendorSerializer(vendor)
        return Response(serialized_data.data)

    def put(self, request, vendor_id):
        vendor = Vendor.objects.get(id=vendor_id)
        serialized_data = VendorSerializer(vendor, data = request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        vendor = Vendor.objects.get(id=vendor_id)
        vendor.delete()
        return Response(status=status.HTTP_200_OK)
