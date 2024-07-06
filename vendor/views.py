from rest_framework import viewsets
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=["get"])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        data = {
            "on_time_delivery_rate": vendor.on_time_delivery_rate,
            "quality_rating_avg": vendor.quality_rating_avg,
            "average_response_time": vendor.average_response_time,
            "fulfillment_rate": vendor.fulfillment_rate,
        }
        return Response(data)


# class PurchaseOrderViewSet(viewsets.ModelViewSet):
#     queryset = PurchaseOrder.objects.all()
#     serializer_class = PurchaseOrderSerializer

#     def perform_create(self, serializer):
#         purchase_order = serializer.save()
#         self.update_vendor_metrics(purchase_order.vendor)

#     def perform_update(self, serializer):
#         purchase_order = serializer.save()
#         self.update_vendor_metrics(purchase_order.vendor)

#     def perform_destroy(self, instance):
#         vendor = instance.vendor
#         instance.delete()
#         self.update_vendor_metrics(vendor)

#     def update_vendor_metrics(self, vendor):
#         completed_orders = vendor.purchase_orders.filter(status="completed")
#         total_orders = vendor.purchase_orders.count()

#         if total_orders > 0:
#             on_time_deliveries = completed_orders.filter(
#                 delivery_date__lte=models.F("order_date")
#             ).count()
#             vendor.on_time_delivery_rate = (
#                 on_time_deliveries / completed_orders.count()
#             ) * 100

#             quality_ratings = completed_orders.exclude(quality_rating=None).values_list(
#                 "quality_rating", flat=True
#             )
#             if quality_ratings:
#                 vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings)

#             acknowledgment_times = vendor.purchase_orders.exclude(
#                 acknowledgment_date=None
#             ).values_list("acknowledgment_date", "issue_date")
#             if acknowledgment_times:
#                 response_times = [
#                     (ack - iss).total_seconds() for ack, iss in acknowledgment_times
#                 ]
#                 vendor.average_response_time = sum(response_times) / len(response_times)

#             fulfilled_orders = completed_orders.filter(status="completed").count()
#             vendor.fulfillment_rate = (fulfilled_orders / total_orders) * 100

#             vendor.save()


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None):
        po = self.get_object()
        po.acknowledgment_date = request.data.get("acknowledgment_date")
        po.save()
        return Response({"status": "acknowledged"}, status=status.HTTP_200_OK)
