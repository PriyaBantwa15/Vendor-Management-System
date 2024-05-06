import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Vendor, PurchaseOrder
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import models

# Vendor Profile Management API Endpoints 
@csrf_exempt
@api_view(['POST'])
def create_vendor(request):
    if request.method == 'POST':
        data = request.data
        vendor = Vendor.objects.create(
            name=data.get('name'),
            contact_details=data.get('contact_details'),
            address=data.get('address'),
            vendor_code=data.get('vendor_code')
        )
        return JsonResponse({'message': 'Vendor created successfully'})


def list_vendors(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        data = [{'id': vendor.id, 'name': vendor.name} for vendor in vendors]
        return JsonResponse(data, safe=False)


def retrieve_vendor(request, vendor_id):
    if request.method == 'GET':
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        data = {
            'id': vendor.id,
            'name': vendor.name,
            'contact_details': vendor.contact_details,
            'address': vendor.address,
            'vendor_code': vendor.vendor_code
        }
        return JsonResponse(data)

 
def update_vendor(request, vendor_id):
    if request.method == 'PUT':
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        data = request.data
        vendor.name = data.get('name', vendor.name)
        vendor.contact_details = data.get('contact_details', vendor.contact_details)
        vendor.address = data.get('address', vendor.address)
        vendor.vendor_code = data.get('vendor_code', vendor.vendor_code)
        vendor.save()
        return JsonResponse({'message': 'Vendor updated successfully'})

 
def delete_vendor(request, vendor_id):
    if request.method == 'DELETE':
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        vendor.delete()
        return JsonResponse({'message': 'Vendor deleted successfully'})

# Purchase Order Tracking API Endpoints 
def create_purchase_order(request):
    if request.method == 'POST':
        data = request.POST  # Assuming form data is sent via POST request
        vendor_id = data.get('vendor_id')
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        
        # Assuming form fields are named accordingly
        po_number = data.get('po_number')
        order_date = data.get('order_date')
        delivery_date = data.get('delivery_date')
        items = data.get('items')
        quantity = data.get('quantity')
        status = data.get('status')
        quality_rating = data.get('quality_rating')
        issue_date = data.get('issue_date')
        acknowledgment_date = data.get('acknowledgment_date')
        
        # Create Purchase Order
        purchase_order = PurchaseOrder.objects.create(
            po_number=po_number,
            vendor=vendor,
            order_date=order_date,
            delivery_date=delivery_date,
            items=items,
            quantity=quantity,
            status=status,
            quality_rating=quality_rating,
            issue_date=issue_date,
            acknowledgment_date=acknowledgment_date
        )
        
        return JsonResponse({'message': 'Purchase Order created successfully'})


def list_purchase_orders(request):
    if request.method == 'GET':
        purchase_orders = PurchaseOrder.objects.all()
        data = []
        for po in purchase_orders:
            # Assuming you want to return specific fields of the purchase order
            po_data = {
                'po_number': po.po_number,
                'vendor': po.vendor.name,  # Assuming Vendor model has a 'name' field
                'order_date': po.order_date.strftime('%Y-%m-%d'),  # Format date as string
                'delivery_date': po.delivery_date.strftime('%Y-%m-%d'),  # Format date as string
                'status': po.status,
            }
            data.append(po_data)
        return JsonResponse(data,safe=False)

def retrieve_purchase_order(request, po_id):
    if request.method == 'GET':
        po = get_object_or_404(PurchaseOrder, pk=po_id)  
        po_data = {
                'po_number': po.po_number,
                'vendor': po.vendor.name,  # Assuming Vendor model has a 'name' field
                'order_date': po.order_date.strftime('%Y-%m-%d'),  # Format date as string
                'delivery_date': po.delivery_date.strftime('%Y-%m-%d'),  # Format date as string
                'status': po.status,
            }      
    return JsonResponse(po_data,safe=False)

 
def update_purchase_order(request, po_id):
    if request.method == 'PUT':
        data = request.POST  # Assuming form data is sent via PUT request
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        
        # Assuming form fields are named accordingly
        purchase_order.po_number = data.get('po_number', purchase_order.po_number)
        purchase_order.order_date = data.get('order_date', purchase_order.order_date)
        purchase_order.delivery_date = data.get('delivery_date', purchase_order.delivery_date)
        purchase_order.items = data.get('items', purchase_order.items)
        purchase_order.quantity = data.get('quantity', purchase_order.quantity)
        purchase_order.status = data.get('status', purchase_order.status)
        purchase_order.quality_rating = data.get('quality_rating', purchase_order.quality_rating)
        purchase_order.issue_date = data.get('issue_date', purchase_order.issue_date)
        purchase_order.acknowledgment_date = data.get('acknowledgment_date', purchase_order.acknowledgment_date)
        
        purchase_order.save()
        
        return JsonResponse({'message': 'Purchase Order updated successfully'})

 
def delete_purchase_order(request, po_id):
    if request.method == 'DELETE':
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        purchase_order.delete()
        return JsonResponse({'message': 'Purchase Order deleted successfully'})

# Vendor Performance Evaluation API Endpoint

def vendor_performance(request, vendor_id):
    if request.method == 'GET':
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        completed_pos = vendor.purchaseorder_set.filter(status='Completed')
        total_completed_pos = completed_pos.count()
        
        # On-Time Delivery Rate
        on_time_delivery_pos = completed_pos.filter(delivery_date__lte=models.F('delivery_date'))
        on_time_delivery_rate = (on_time_delivery_pos.count() / total_completed_pos) * 100 if total_completed_pos > 0 else 0
        
        # Quality Rating Average
        quality_ratings = completed_pos.exclude(quality_rating=None).values_list('quality_rating', flat=True)
        quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0
        
        # Average Response Time
        response_times = completed_pos.exclude(acknowledgment_date=None).annotate(
            response_time=models.F('acknowledgment_date') - models.F('issue_date')
        ).values_list('response_time', flat=True)
        average_response_time = sum(response_times, datetime.timedelta()).total_seconds() / 60 / len(response_times) if response_times else 0
    
        # Fulfilment Rate
        fulfilled_pos = completed_pos.exclude(acknowledgment_date=None)
        fulfillment_rate = (fulfilled_pos.count() / total_completed_pos) * 100 if total_completed_pos > 0 else 0
        
        # Update vendor's performance metrics
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.quality_rating_avg = quality_rating_avg
        vendor.average_response_time = average_response_time
        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()

        data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate
        }
    return JsonResponse(data,safe=False)
        