from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance
from datetime import timezone, datetime

def calculate_delivery_rate(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    count_completed_orders = completed_orders.count()
    if count_completed_orders == 0:
        on_time_delivery_rate = 0
    on_time_orders = completed_orders.filter(delivery_date__lte=timezone.now())
    on_time_delivery_rate = (on_time_orders.count()/count_completed_orders) * 100
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
    total_rt, avg_rt = 0, 0
    for i in all_orders:
        total_rt += (i.acknowledgement_date - i.issue_date).days
    if not all_orders.count() == 0:
        avg_rt =  total_rt/all_orders.count()
    vendor.average_response_time = avg_rt
    vendor.save()

def fullfilment_rate(vendor):
    all_order_count = PurchaseOrder.objects.filter(vendor=vendor).count()
    all_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    if all_order_count > 0:
        vendor.fullfillment_rate = all_completed_orders/PurchaseOrder.objects.filter(vendor=vendor).count()
        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def calculate_on_time_delivery_rate(sender, instance, created):
    if not created and instance.status == 'completed':
        calculate_delivery_rate(instance.vendor)
        fullfilment_rate(instance.vendor)
        new_hp = HistoricalPerformance(vendor = instance.vendor, date = datetime.now(),
                                       on_time_delivery_rate = instance.vendor.on_time_delivery_rate,
                                       quality_rating_avg = instance.vendor.quality_rating_avg,
                                       average_response_time = instance.vendor.average_response_time,
                                       fulfillment_rate = instance.vendor.fullfilment_rate)
        new_hp.save()
    if not created and instance.status == 'completed' and instance.quality_rating != None:
        average_quality_rating(instance.vendor)
    if instance.acknowledged_data is not None:
        average_response_time(instance.vendor)




