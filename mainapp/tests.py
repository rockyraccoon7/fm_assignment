from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder

class VendorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_data = {
            "name": "Test Vendor",
            "contact_details": "test@example.com",
            "address": "123 Test Street",
            "vendor_code": "TEST001"
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_get_all_vendors(self):
        response = self.client.get(reverse('vendor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_vendor(self):
        response = self.client.get(reverse('specific-vendor', kwargs={'vendor_code': self.vendor.vendor_code}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        updated_data = {
            "name": "Updated Vendor",
            "contact_details": "updated@example.com",
            "address": "456 Updated Street",
            "vendor_code": "TEST001"
        }
        response = self.client.put(reverse('specific-vendor', kwargs={'vendor_code': self.vendor.vendor_code}), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.get(id=self.vendor.id).name, updated_data['name'])

    def test_delete_vendor(self):
        response = self.client.delete(reverse('specific-vendor', kwargs={'vendor_code': self.vendor.vendor_code}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.filter(id=self.vendor.id).count(), 0)

class PurchaseOrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="test@example.com", address="123 Test Street", vendor_code="TEST001")
        self.po_data = {
            "po_number": "PO001",
            "vendor": self.vendor,
            "order_date": "2024-05-08T10:00:00Z",
            "delivery_date": "2024-05-15T10:00:00Z",
            "items": [{"item1": "Product A", "item2": "Product B"}],
            "quantity": 10,
            "status": "pending",
            "issue_date": "2024-05-08T10:00:00Z"
        }

        self.purchase_order = PurchaseOrder.objects.create(**self.po_data)


    def test_get_all_purchase_orders(self):
        response = self.client.get(reverse('purchase-order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_purchase_order(self):
        response = self.client.get(reverse('specific-purchase-order', kwargs={'po_id': self.purchase_order.po_number}))
        print("hi", PurchaseOrder.objects.all())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        updated_data = {
            "po_number": "PO001",
            "vendor": self.vendor.id,
            "order_date": "2024-05-08T10:00:00Z",
            "delivery_date": "2024-05-15T10:00:00Z",
            "items": [{"item1": "Product A", "item2": "Product B"}],
            "quantity": 10,
            "status": "completed",
            "issue_date": "2024-05-08T10:00:00Z",
            "acknowledgment_date" : "2024-05-10T10:00:00Z"
        }

        response = self.client.put(reverse('specific-purchase-order', kwargs={'po_id': self.purchase_order.po_number}), updated_data, format="json")
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PurchaseOrder.objects.get(po_number = "PO001").status, updated_data['status'])

    def test_delete_purchase_order(self):
        response = self.client.delete(reverse('specific-purchase-order', kwargs={'po_id': self.purchase_order.po_number}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PurchaseOrder.objects.filter(po_number="PO001").count(), 0)

class VendorPerformanceAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="test@example.com", address="123 Test Street", vendor_code="TEST001")

    def test_get_vendor_performance(self):
        response = self.client.get(reverse('vendor-performance', kwargs={'vendor_code': self.vendor.vendor_code}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AcknowledgeOrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="test@example.com", address="123 Test Street", vendor_code="TEST001")
        self.purchase_order = PurchaseOrder.objects.create(po_number="PO001", vendor=self.vendor, order_date="2024-05-08T10:00:00Z",
                                                           delivery_date="2024-05-15T10:00:00Z", items={"item1": "Product A", "item2": "Product B"},
                                                           quantity=10, status="pending", issue_date="2024-05-08T10:00:00Z")

    def test_acknowledge_purchase_order(self):
        response = self.client.post(reverse('acknowledge-purchase-order', kwargs={'po_id': self.purchase_order.po_number}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(PurchaseOrder.objects.get(id=self.purchase_order.id).acknowledgment_date)
