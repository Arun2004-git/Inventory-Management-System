from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    due_balance = models.FloatField(default=0)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    purchase_price = models.FloatField()     # Price paid to vendor
    profit_percent = models.FloatField(default=10)  # Desired profit margin percentage
    gst_percent = models.FloatField(default=5)      # GST percentage to apply on selling price
    stock = models.IntegerField(default=0)          # Current stock quantity

    def selling_price(self):
        # Calculate selling price based on profit percentage
        return self.purchase_price * (1 + self.profit_percent/100)

    def gst_amount(self):
        # Calculate GST amount on the selling price
        return self.selling_price() * (self.gst_percent/100)
    def total_paid(self):
        return self.purchase_price * self.stock 

    def __str__(self):
        return f"{self.name} ({self.vendor.name})"
class VendorPurchase(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    total_paid = models.FloatField(default=0)

    def __str__(self):
        return f"Purchase from {self.vendor.name} on {self.purchase_date}"


class VendorPurchaseItem(models.Model):
    purchase = models.ForeignKey(VendorPurchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.FloatField()
    total = models.FloatField()

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)

        # ✅ Update product stock and price
        self.product.stock += self.quantity
        self.product.purchase_price = self.price_per_unit
        self.product.save()

        # ✅ Update total_paid in VendorPurchase
        total = sum(item.total for item in self.purchase.items.all())
        self.purchase.total_paid = total
        self.purchase.save()


class Bill(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()  # Sum of item totals (without GST)
    total_gst = models.FloatField()     # Sum of GST amounts
    net_total = models.FloatField()     # total_amount + total_gst

    def __str__(self):
        return f"Bill {self.id} for {self.farmer.name}"

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()  # selling price per unit at time of billing
    total = models.FloatField()  # price * quantity
class Payment(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    note = models.CharField(max_length=200, blank=True)
