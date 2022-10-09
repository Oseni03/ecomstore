from django import forms

from account.models import Address

addresses=Address.objects.all()

class ShippingForm(forms.Form):
  address = forms.ModelChoiceField(queryset=addresses, required=False, empty_label="Select address")
  