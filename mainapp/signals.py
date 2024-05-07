from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from datetime import timezone

def calculate_delivery_rate(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    count_completed_orders = completed_orders.count()
    if count_completed_orders == 0:
        return 0
    on_time_orders = completed_orders.filter(delivery_date__lte=timezone.now())
    on_time_delivery_rate = (on_time_orders.count() / count_completed_orders) * 100
    return on_time_delivery_rate

def average_quality_rating(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating!=None)
    count_completed_orders = completed_orders.count()
    total_rq = 0
    if not count_completed_orders == 0:
        for i in completed_orders:
            total_qr += i.quality_rating
        return total_rq/count_completed_orders
    return 0


@receiver(post_save, sender=PurchaseOrder)
def calculate_on_time_delivery_rate(sender, instance, created):
    if not created and instance.status == 'completed':
        vendor = instance.vendor
        new_delivery_rate = calculate_delivery_rate(vendor)
        vendor.on_time_delivery_rate = new_delivery_rate
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def calculate_average_quality_rating(sender, instance, created):
    if not created and instance.status == 'completed' and instance.quality_rating != None:
        average_rq = average_quality_rating(instance.vendor)
        instance.vendor.quality_rating_avg = average_rq
        instance.vendor.save()


