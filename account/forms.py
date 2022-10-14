from django import forms 
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

from .models import Customer, Address, UserToken


class UserLoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={
    "autocorrect": "off", 
    "autocapitalize": "off"}))
  password = forms.CharField(widget=forms.PasswordInput())


class RegistrationForm(forms.ModelForm):
  username = forms.CharField(label="Enter name", min_length=4, max_length=50, help_text="Required")
  first_name = forms.CharField(label="First Name")
  last_name = forms.CharField(label="Last Name")
  email = forms.EmailField(
    max_length=100, help_text="Required", 
    error_messages = {"required": "Sorry, you will need an email"})
  password = forms.CharField(label="Password", widget=forms.PasswordInput)
  password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)
  country = CountryField().formfield()
  
  class Meta:
    model = Customer 
    fields = ("username", "first_name", "last_name", "email", "mobile", "country")
  
  def clean_password2(self):
    cd = self.cleaned_data
    if cd["password"] != cd["password2"]:
      raise forms.ValidationError("Passwords do not match")
    return cd["password"]
  
  def clean_email(self):
    email = self.cleaned_data["email"]
    r = Customer.objects.filter(email=email)
    if r.exists():
      raise forms.ValidationError("Please choose another email, that's already taken")
    return email
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields["username"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Username",
    })
    self.fields["first_name"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "First Name",
    })
    self.fields["last_name"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "First Name",
    })
    self.fields["mobile"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Mobile",
    })
    self.fields["email"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Email",
    })
    self.fields["password"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Password",
    })
    self.fields["password2"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Confirm Password",
    })


class UserEditForm(forms.ModelForm):
  email = forms.EmailField(
    widget=forms.TextInput(
      attrs={
        "class": "form-control", 
        "placeholder": "Email", 
        "readonly": "readonly"}), 
      label="Account email (cannot be changed)", max_length=200)
  name = forms.CharField(
    widget=forms.TextInput(
      attrs={
        "class": "form-control", 
        "placeholder": "Name"}),
    label="Name", 
    max_length=150, min_length=4)
  
  class Meta:
    model = Customer 
    fields = ("email", "name", "mobile")
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields["email"].required = True
    self.fields["name"].required = True


class PwdResetForm(PasswordResetForm):
  email = forms.EmailField(max_length=254, widget=forms.TextInput())
  
  def clean_email(self):
    email = self.cleaned_data["email"]
    user = Customer.objects.filter(email=email)
    if not user:
      raise forms.ValidationError(
        "Unfortunately we could not find that email address"
      )
    return email


class UserAddressForm(forms.ModelForm):
  class Meta:
    model = Address
    fields = ["full_name", "phone", "address_line_1", "address_line_2", "town_city", "country", "delivery_instructions"]
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields["full_name"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Full Name",
    })
    self.fields["phone"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Phone Number",
    })
    self.fields["address_line_1"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Address 1",
    })
    self.fields["address_line_2"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Address 2",
    })
    self.fields["town_city"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Town/City/State",
    })
    self.fields["country"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Country",
    })
    self.fields["delivery_instructions"].widget.attrs.update({
      "class": "form-control",
      "placeholder": "Delivery Instructions",
    })


class ChangePasswordForm(PasswordChangeForm):
  old_password = forms.CharField(widget=forms.PasswordInput(attrs={
      "class": "form-control",
      "placeholder": "Old Password",
    }))
  new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
      "class": "form-control",
      "placeholder": "New Password",
    }))
  new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
      "class": "form-control",
      "placeholder": "Confirm New Password"
  }))
  
  class Meta:
    model = Customer 
    fields = ("password1", "password2",)


class TwoStepForm(forms.ModelForm):
  two_step_code = forms.CharField(max_length=6, required=True, widget=forms.TextInput(attrs={
      "class": "form-control",
      "placeholder": "Code..."
  }))
  
  class Meta:
    model = UserToken 
    fields = ("two_step_code",)