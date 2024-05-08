from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vendor, PurchaseOrder

class VendorManagementSystemTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create sample vendor
        self.vendor = Vendor.objects.create(
            name='Sample Vendor',
            contact_details='sample@example.com',
            address='123 Sample St',
            vendor_code='VENDOR001'
        )

        # Create sample purchase order
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date='2024-05-01',
            delivery_date='2024-05-10',
            items={'item': 'sample item'},
            quantity=10,
            status='completed',
            quality_rating=4.5,
            issue_date='2024-05-01T08:00:00Z',
            acknowledgment_date='2024-05-01T08:05:00Z'
        )

    def test_vendor_profile_management(self):
        # Test creating a new vendor
        new_vendor_data = {
            'name': 'New Vendor',
            'contact_details': 'new@example.com',
            'address': '456 New St',
            'vendor_code': 'VENDOR002'
        }
        response = self.client.post(reverse('vendor-list'), new_vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test retrieving all vendors
        response = self.client.get(reverse('vendor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming we have only created 2 vendors

        # Test retrieving a specific vendor
        response = self.client.get(reverse('specific-vendor', args=[self.vendor.vendor_code]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor.name)

        # Test updating a vendor's details
        updated_vendor_data = {
            'name': 'Updated Vendor Name',
            'address': '789 Updated St'
        }
        response = self.client.put(reverse('specific-vendor', args=[self.vendor.vendor_code]), updated_vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_vendor_data['name'])

        # Test deleting a vendor
        response = self.client.delete(reverse('specific-vendor', args=[self.vendor.vendor_code]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_purchase_order_tracking(self):
        # Test creating a new purchase order
        new_po_data = {
            'po_number': 'PO002',
            'vendor': self.vendor.vendor_code,
            'order_date': '2024-05-02',
            'delivery_date': '2024-05-15',
            'items': {'item': 'another item'},
            'quantity': 5,
            'status': 'pending'
        }
        response = self.client.post(reverse('purchase-order-list'), new_po_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test retrieving all purchase orders
        response = self.client.get(reverse('purchase-order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming we have only created 2 purchase orders

        # Test retrieving a specific purchase order
        response = self.client.get(reverse('specific-purchase-order', args=[self.purchase_order.po_number]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.purchase_order.po_number)

        # Test updating a purchase order
        updated_po_data = {
            'status': 'completed'
        }
        response = self.client.put(reverse('specific-purchase-order', args=[self.purchase_order.po_number]), updated_po_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], updated_po_data['status'])

        # Test deleting a purchase order
        response = self.client.delete(reverse('specific-purchase-order', args=[self.purchase_order.po_number]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_vendor_performance_evaluation(self):
        # Test retrieving vendor performance metrics
        response = self.client.get(reverse('vendor-performance', args=[self.vendor.vendor_code]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('on_time_delivery_rate', response.data)
        self.assertIn('quality_rating_avg', response.data)
        self.assertIn('average_response_time', response.data)
        self.assertIn('fulfillment_rate', response.data)

    def test_update_acknowledgment(self):
        # Test acknowledging a purchase order
        acknowledgment_data = {
            'acknowledgment_date': '2024-05-03T08:10:00Z'
        }
        response = self.client.post(reverse('acknowledge-purchase-order', args=[self.purchase_order.po_number]), acknowledgment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['acknowledgment_date'], acknowledgment_data['acknowledgment_date'])

        # Verify average response time is updated
        response = self.client.get(reverse('vendor-performance', args=[self.vendor.vendor_code]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['average_response_time'])

# Additional tests can be added for edge cases, error handling, etc.

