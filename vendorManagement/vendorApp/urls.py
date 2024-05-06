from django.urls import path
from .views import (
    create_vendor,
    list_vendors,
    retrieve_vendor,
    update_vendor,
    delete_vendor,
    create_purchase_order,
    list_purchase_orders,
    retrieve_purchase_order,
    update_purchase_order,
    delete_purchase_order,
    vendor_performance,
)

urlpatterns = [
    # Vendor Profile Management Endpoints
    path('vendors/', list_vendors, name='list_vendors'),
    path('vendors/<int:vendor_id>/', retrieve_vendor, name='retrieve_vendor'),
    path('vendors/create/', create_vendor, name='create_vendor'),
    path('vendors/<int:vendor_id>/update/', update_vendor, name='update_vendor'),
    path('vendors/<int:vendor_id>/delete/', delete_vendor, name='delete_vendor'),

    # Purchase Order Tracking Endpoints
    path('purchase_orders/', list_purchase_orders, name='list_purchase_orders'),
    path('purchase_orders/<int:po_id>/', retrieve_purchase_order, name='retrieve_purchase_order'),
    path('purchase_orders/create/', create_purchase_order, name='create_purchase_order'),
    path('purchase_orders/<int:po_id>/update/', update_purchase_order, name='update_purchase_order'),
    path('purchase_orders/<int:po_id>/delete/', delete_purchase_order, name='delete_purchase_order'),

    # Vendor Performance Evaluation Endpoint
    path('vendors/<int:vendor_id>/performance/', vendor_performance, name='vendor_performance'),
]
