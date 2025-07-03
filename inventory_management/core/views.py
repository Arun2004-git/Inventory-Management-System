# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import json
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages # Import messages

from .models import *
from .forms import *

@login_required
def home(request):
    return render(request, 'home.html')


# --- Vendor Views ---
@login_required
def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor_list.html', {'vendors': vendors})

@login_required
def vendor_add(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor added successfully!')
            return redirect('vendor-list')
    else:
        form = VendorForm()
    return render(request, 'vendor_form.html', {'form': form})

@login_required
def vendor_edit(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor updated successfully!')
            return redirect('vendor-list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendor_form.html', {'form': form})

@login_required
def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST': # Added POST check for confirmation
        vendor.delete()
        messages.success(request, 'Vendor deleted successfully!')
        return redirect('vendor-list')
    return render(request, 'confirm_delete.html', {'obj': vendor, 'type': 'Vendor'})


# --- Vendor Purchase Views ---
@login_required
def vendor_purchase_list(request):
    purchases = VendorPurchase.objects.all()
    return render(request, 'vendor_purchase_list.html', {'purchases': purchases})

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import VendorPurchaseForm, VendorPurchaseItemFormSet

@login_required
def vendor_purchase_add(request):
    if request.method == 'POST':
        form = VendorPurchaseForm(request.POST)
        formset = VendorPurchaseItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            purchase = form.save(commit=False)
            purchase.total_paid = 0  # will calculate later
            purchase.save()

            total = 0
            items = formset.save(commit=False)

            for item in items:
                item.purchase = purchase
                item.save()
                total += item.total

            purchase.total_paid = total
            purchase.save()

            messages.success(request, 'Vendor Purchase created successfully!')
            return redirect('vendor-purchase-list')
    else:
        form = VendorPurchaseForm()
        formset = VendorPurchaseItemFormSet()

    return render(request, 'vendor_purchase_form.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def vendor_purchase_edit(request, pk):
    purchase = get_object_or_404(VendorPurchase, pk=pk)
    if request.method == 'POST':
        form = VendorPurchaseForm(request.POST, instance=purchase)
        formset = VendorPurchaseItemFormSet(request.POST, instance=purchase)

        if form.is_valid() and formset.is_valid():
            form.save()
            items = formset.save(commit=False)

            total = 0
            for item in items:
                item.purchase = purchase
                item.total = item.quantity * item.price_per_unit
                item.save()

                # Update stock
                item.product.stock += item.quantity
                item.product.purchase_price = item.price_per_unit
                item.product.save()

                total += item.total

            # Handle deleted items
            for obj in formset.deleted_objects:
                obj.product.stock -= obj.quantity  # Reverse stock if deleted
                obj.product.save()
                obj.delete()

            purchase.total_paid = total
            purchase.save()

            messages.success(request, 'Vendor purchase updated successfully!')
            return redirect('vendor-purchase-list')
    else:
        form = VendorPurchaseForm(instance=purchase)
        formset = VendorPurchaseItemFormSet(instance=purchase)

    return render(request, 'vendor_purchase_form.html', {
        'form': form,
        'formset': formset
    })
@login_required
def vendor_purchase_delete(request, pk):
    purchase = get_object_or_404(VendorPurchase, pk=pk)
    if request.method == 'POST':
        # First restore stock before deletion
        for item in purchase.items.all():
            item.product.stock -= item.quantity
            item.product.save()

        purchase.delete()
        messages.success(request, 'Vendor purchase deleted successfully!')
        return redirect('vendor-purchase-list')
    return render(request, 'confirm_delete.html', {'obj': purchase, 'type': 'Vendor Purchase'})

# --- Farmer Views ---
@login_required
def farmer_list(request):
    farmers = Farmer.objects.all()
    return render(request, 'farmer_list.html', {'farmers': farmers})

@login_required
def farmer_add(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farmer added successfully!')
            return redirect('farmer-list')
    else:
        form = FarmerForm()
    return render(request, 'farmer_form.html', {'form': form})

@login_required
def farmer_edit(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.method == 'POST':
        form = FarmerForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farmer updated successfully!')
            return redirect('farmer-list')
    else:
        form = FarmerForm(instance=farmer)
    return render(request, 'farmer_form.html', {'form': form})

@login_required
def farmer_delete(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.method == 'POST':
        farmer.delete()
        messages.success(request, 'Farmer deleted successfully!')
        return redirect('farmer-list')
    return render(request, 'confirm_delete.html', {'obj': farmer, 'type': 'Farmer'})


# --- Product Views ---
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product-list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product-list')
    return render(request, 'confirm_delete.html', {'obj': product, 'type': 'Product'})


# --- Bill Views ---
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import BillForm, BillItemFormset

@login_required
def create_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        formset = BillItemFormset(request.POST)

        # Get the value of the paid/not paid dropdown from the form
        payment_status = request.POST.get('payment_status', 'not_paid')

        if form.is_valid() and formset.is_valid():
            bill = form.save(commit=False)
            bill.total_amount = 0
            bill.total_gst = 0

            # Calculate totals before saving the bill
            for item_form in formset:
                product = item_form.cleaned_data.get('product')
                qty = item_form.cleaned_data.get('quantity')
                if product and qty:
                    price_per_unit = product.selling_price()
                    total_per_item = price_per_unit * qty
                    gst_per_item = product.gst_amount() * qty

                    bill.total_amount += total_per_item
                    bill.total_gst += gst_per_item

            bill.net_total = bill.total_amount + bill.total_gst
            bill.save()

            # Save bill items and update product stock
            for item_form in formset:
                if item_form.cleaned_data.get('product') and item_form.cleaned_data.get('quantity'):
                    bill_item = item_form.save(commit=False)
                    bill_item.bill = bill
                    bill_item.price = bill_item.product.selling_price()
                    bill_item.total = bill_item.price * bill_item.quantity
                    bill_item.save()

                    # Update stock
                    bill_item.product.stock -= bill_item.quantity
                    bill_item.product.save()

            # ✅ Update due_balance only if status is "not_paid"
            if payment_status == 'not_paid':
                farmer = bill.farmer
                farmer.due_balance += bill.net_total
                farmer.save()

            messages.success(request, 'Bill created successfully!')
            return redirect('bill-list')
    else:
        form = BillForm()
        formset = BillItemFormset()

    return render(request, 'bill_form.html', {
        'form': form,
        'formset': formset
    })

@login_required
def bill_list(request):
    bills = Bill.objects.select_related('farmer').all()
    return render(request, 'bill_list.html', {'bills': bills})

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bill

@login_required
def bill_pdf(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    html_string = render_to_string('bill_invoice.html', {'bill': bill})

    # Generate PDF in memory using BytesIO
    pdf_buffer = BytesIO()
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(target=pdf_buffer)

    # Prepare response
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=bill_{bill.id}.pdf'

    return response

# --- Payment Views (for Farmers) ---
@login_required
def payment_add(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            payment.farmer.due_balance -= payment.amount
            payment.farmer.save()
            messages.success(request, f'Payment of ₹{payment.amount} recorded for {payment.farmer.name}!')
            return redirect('farmer-list')
    else:
        form = PaymentForm()
    return render(request, 'payment_form.html', {'form': form})

# --- Stock Dashboard ---
@login_required
def stock_dashboard(request):
    products = Product.objects.all().order_by('name') # Order for consistent chart
    low_threshold = 10
    low_stock = products.filter(stock__lt=low_threshold)

    labels = [p.name for p in products]
    data = [p.stock for p in products]

    return render(request, 'stock_dashboard.html', {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'low_stock': low_stock,
    })

# --- Reports ---
@login_required
def reports(request):
    today = timezone.now().date()

    # Sales totals
    daily_sales = Bill.objects.filter(date__date=today).aggregate(Sum('net_total'))['net_total__sum'] or 0
    weekly_sales = Bill.objects.filter(date__date__gte=today - timedelta(days=7)).aggregate(Sum('net_total'))['net_total__sum'] or 0
    monthly_sales = Bill.objects.filter(date__month=today.month, date__year=today.year).aggregate(Sum('net_total'))['net_total__sum'] or 0
    yearly_sales = Bill.objects.filter(date__year=today.year).aggregate(Sum('net_total'))['net_total__sum'] or 0

    # Profit calculation: (selling price - purchase price) * quantity for each BillItem
    # Ensure 'price' in BillItem is the selling_price at the time of billing
    daily_profit = BillItem.objects.filter(bill__date__date=today).annotate(
        profit=F('quantity') * (F('price') - F('product__purchase_price'))
    ).aggregate(total_profit=Sum('profit'))['total_profit'] or 0

    weekly_profit = BillItem.objects.filter(bill__date__date__gte=today - timedelta(days=7)).annotate(
        profit=F('quantity') * (F('price') - F('product__purchase_price'))
    ).aggregate(total_profit=Sum('profit'))['total_profit'] or 0

    monthly_profit = BillItem.objects.filter(bill__date__month=today.month, bill__date__year=today.year).annotate(
        profit=F('quantity') * (F('price') - F('product__purchase_price'))
    ).aggregate(total_profit=Sum('profit'))['total_profit'] or 0

    yearly_profit = BillItem.objects.filter(bill__date__year=today.year).annotate(
        profit=F('quantity') * (F('price') - F('product__purchase_price'))
    ).aggregate(total_profit=Sum('profit'))['total_profit'] or 0

    context = {
        'daily_sales': daily_sales,
        'weekly_sales': weekly_sales,
        'monthly_sales': monthly_sales,
        'yearly_sales': yearly_sales,
        'daily_profit': daily_profit,
        'weekly_profit': weekly_profit,
        'monthly_profit': monthly_profit,
        'yearly_profit': yearly_profit,
    }
    return render(request, 'reports.html', context)