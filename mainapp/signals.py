from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from datetime import timezone

def calculate_delivery_rate(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    count_completed_orders = completed_orders.count()
    if count_completed_orders == 0:
        on_time_delivery_rate = 0
    on_time_orders = completed_orders.filter(delivery_date__lte=timezone.now())
    on_time_delivery_rate = (on_time_orders.count() / count_completed_orders) * 100
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.save()

def average_quality_rating(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating!=None)
    count_completed_orders = completed_orders.count()
    total_qr, aqr = 0, 0
    if not count_completed_orders == 0:
        for i in completed_orders:
            total_qr += i.quality_rating
        aqr = total_qr/count_completed_orders
    vendor.quality_rating_avg = aqr
    vendor.save()

def average_response_time(vendor):
    all_orders = PurchaseOrder.objects.filter(vendor=vendor, issue_date != None, acknowledgment_date != None)
    total_rt = 0
    for i in all_orders:
        


@receiver(post_save, sender=PurchaseOrder)
def calculate_on_time_delivery_rate(sender, instance, created):
    if not created and instance.status == 'completed':
        calculate_delivery_rate(instance.vendor)
    if not created and instance.status == 'completed' and instance.quality_rating != None:
        average_quality_rating(instance.vendor)
    if instance.acknowledged_data is not None:


