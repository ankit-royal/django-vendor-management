from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vendor, PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()

    if completed_orders.exists():
        on_time_orders = completed_orders.filter(
            delivery_date__lte=models.F("delivery_date")
        ).count()
        vendor.on_time_delivery_rate = on_time_orders / completed_orders.count()

        quality_ratings = completed_orders.exclude(
            quality_rating__isnull=True
        ).values_list("quality_rating", flat=True)
        if quality_ratings:
            vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings)

        response_times = (
            completed_orders.exclude(acknowledgment_date__isnull=True)
            .annotate(
                response_time=models.F("acknowledgment_date") - models.F("issue_date")
            )
            .values_list("response_time", flat=True)
        )
        if response_times:
            vendor.average_response_time = sum(response_times, timedelta()) / len(
                response_times
            )

    if total_orders > 0:
        fulfilled_orders = completed_orders.exclude(status="issue")
        vendor.fulfillment_rate = fulfilled_orders.count() / total_orders

    vendor.save()
