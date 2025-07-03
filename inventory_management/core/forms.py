from django import forms
from .models import *

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'mobile', 'address']
class VendorPurchaseForm(forms.ModelForm):
    class Meta:
        model = VendorPurchase
        fields = ['vendor']

class VendorPurchaseItemForm(forms.ModelForm):
    class Meta:
        model = VendorPurchaseItem
        fields = ['product', 'quantity', 'price_per_unit']

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['name', 'mobile', 'address', 'due_balance']
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'vendor', 'purchase_price', 'profit_percent', 'gst_percent', 'stock']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['farmer', 'amount', 'note']


from django.forms import modelform_factory, inlineformset_factory
from .models import Bill, BillItem

BillForm = modelform_factory(Bill, fields=('farmer',))
BillItemFormset = inlineformset_factory(
    Bill, BillItem,
    fields=('product', 'quantity'),
    extra=1,
    can_delete=False
)

from django.forms import inlineformset_factory

VendorPurchaseItemFormSet = inlineformset_factory(
    VendorPurchase,
    VendorPurchaseItem,
    form=VendorPurchaseItemForm,
    extra=1,
    can_delete=True
)
