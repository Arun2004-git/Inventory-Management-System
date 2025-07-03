# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Vendor URLs
    path('vendor/', views.vendor_list, name='vendor-list'),
    path('vendor/add/', views.vendor_add, name='vendor-add'),
    path('vendor/edit/<int:pk>/', views.vendor_edit, name='vendor-edit'),
    path('vendor/delete/<int:pk>/', views.vendor_delete, name='vendor-delete'),

    # Vendor Purchase URLs
    path('vendor/purchase/', views.vendor_purchase_list, name='vendor-purchase-list'),
    path('vendor/purchase/add/', views.vendor_purchase_add, name='vendor-purchase-add'),
    path('vendor/purchase/edit/<int:pk>/', views.vendor_purchase_edit, name='vendor-purchase-edit'),
    path('vendor/purchase/delete/<int:pk>/', views.vendor_purchase_delete, name='vendor-purchase-delete'),

   
    # Farmer URLs
    path('farmer/', views.farmer_list, name='farmer-list'),
    path('farmer/add/', views.farmer_add, name='farmer-add'),
    path('farmer/edit/<int:pk>/', views.farmer_edit, name='farmer-edit'),
    path('farmer/delete/<int:pk>/', views.farmer_delete, name='farmer-delete'),

    # Product URLs
    path('product/', views.product_list, name='product-list'),
    path('product/add/', views.product_add, name='product-add'),
    path('product/edit/<int:pk>/', views.product_edit, name='product-edit'),
    path('product/delete/<int:pk>/', views.product_delete, name='product-delete'),

    # Bill URLs
    path('bill/', views.bill_list, name='bill-list'),
    path('bill/add/', views.create_bill, name='bill-add'),
    path('bill/pdf/<int:bill_id>/', views.bill_pdf, name='bill-pdf'),

    # Payment URL (for Farmers)
    path('payment/add/', views.payment_add, name='payment-add'),

    # Dashboard & Reports URLs
    path('stock/', views.stock_dashboard, name='stock-dashboard'),
    path('reports/', views.reports, name='reports'),
]