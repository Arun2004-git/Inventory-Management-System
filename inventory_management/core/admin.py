from django.contrib import admin
from .models import Vendor,VendorPurchase,VendorPurchaseItem, Farmer, Product, Bill, BillItem, Payment

admin.site.register(Vendor)
admin.site.register(Farmer)
admin.site.register(Product)
admin.site.register(VendorPurchase)
admin.site.register(VendorPurchaseItem)
admin.site.register(Bill)
admin.site.register(BillItem)
admin.site.register(Payment)
