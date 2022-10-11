from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView

from .forms import RegistrationForm, UserEditForm, UserLoginForm, UserAddressForm, TwoStepForm
from .token import account_activation_token
from .models import Customer, Address, UserToken

from store.models import Product 

# Create your views here.
class DashboardView(LoginRequiredMixin, generic.TemplateView):
  template_name = "account/new_dash.html"


class MyLoginView(LoginView):
  template_name = "account/login.html"
  form_class = UserLoginForm 
  
  def form_valid(self, form):
    if form.is_valid():
      username = form.cleaned_data["username"]
      password = form.cleaned_data["password"]
      user = authenticate(email=username, password=password)
      if user.is_active:
        if user.two_step_active:
          current_site = get_current_site(self.request)
          subject = "Two Factor Authentication"
          otp = account_activation_token.generate_otp()
          message = render_to_string("account/email/tf_authentication.html", {
            "user": user,
            "domain": current_site.domain,
            "otp": otp,
          })
          user.email_user(subject, message)
          
          UserToken.objects.get_or_create(two_step_code=otp, customer=user, is_email=True)
          
          messages.info(self.request, "A verification code has been sent to your email.")
          return redirect(reverse("account:tf_verification"))
        else:
          login(self.request, user)
          messages.success(self.request, "login succesful")
          return redirect(reverse("account:dashboard"))
    return super().form_valid(form)


def two_factor_auth(request):
  form = TwoStepForm()
  if request.method == "POST":
    form = TwoStepForm(request.POST)
    if form.is_valid():
      otp = form.cleaned_data["two_step_code"]
      token = UserToken.objects.get(two_step_code=otp, is_active=True)
      if token:
        token.is_active=False
        token.save()
        login(request, token.customer)
        messages.success(request, "Login successful")
        return redirect(reverse("account:dashboard"))
      else:
        messages.info(request, "Invalid OTP code")
  return render(request, "account/tf_auth.html", {"form": form})


class RegistrationFormView(generic.FormView):
  template_name = "account/register.html"
  form_class = RegistrationForm 
  success_url = "/"
  
  def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect("/")
    if self.request.htmx:
      return render(self.request, "account/partials/register-element.html", {"form": self.form_class})
    return super().get(*args, **kwargs)
  
  def form_valid(self, form):
    user = form.save(commit=False)
    print(form.cleaned_data)
    user.set_password = form.cleaned_data["password"]
    user.email = form.cleaned_data["email"]
    user.is_active = False
    user.save()
    current_site = get_current_site(self.request)
    subject = "Activate your Account"
    message = render_to_string("account/email/account_activation.html", {
      "user": user,
      "domain": current_site.domain,
      "uid": urlsafe_base64_encode(force_bytes(user.pk)),
      "token": account_activation_token.make_token(user),
    })
    user.email_user(subject, message)
    
    messages.success(self.request, "Account created successfully. Verify your email to activate your account.")
    return super().form_valid(form)


@login_required
def user_update(request):
  form = UserEditForm(instance=request.user)
  if request.POST:
    form = UserEditForm(request.POST, instance=request.user)
    if form.is_valid:
      user = form.save()
  return render(request, "account/edit_detail.html", {"form": form})
  

def account_activate(request, uidb64, token):
  try:
    id = force_str(urlsafe_base64_decode(uidb64))
    user = Customer.objects.get(id=id)
  except():
    pass
  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True 
    user.save()
    login(request, user)
    messages.success(request, "Account confirmation successful")
    return redirect("account:dashboard")
  else:
    return render(request, "account/activation_invalid.html")


@login_required
def delete_user(request):
  user = Customer.objects.get(id=request.user.pk)
  user.is_active = False 
  user.save()
  logout(user)
  return redirect(reverse("account:logout"))


class AddressListView(generic.ListView):
  template_name = "account/addresses.html"
  context_object_name = "addresses"
  
  def get_queryset(self, *args, **kwargs):
    return Address.objects.filter(customer=self.request.user)


@login_required
def address_add(request):
  form = UserAddressForm()
  if request.method == "POST":
    form = UserAddressForm(request.POST)
    if form.is_valid():
      addr =form.save(commit=False)
      addr.customer = request.user 
      addr.save()
      messages.success(request, "Address added successfully.")
      
      addresses = Address.objects.filter(customer=request.user)
      return render(request, "account/addresses.html", {"addresses": addresses})
  return render(request, "account/address_form.html", {"form": form})


@login_required
def address_update(request, pk):
  addr = get_object_or_404(Address, id=pk)
  form = UserAddressForm(instance=addr)
  if request.method == "POST":
    form = UserAddressForm(request.POST, instance=addr)
    if form.is_valid():
      addr =form.save()
      messages.success(request, "Address added successfully.")
      
      addresses = Address.objects.filter(customer=request.user)
      return render(request, "account/partials/address_list.html", {"addresses": addresses})
  return render(request, "account/address_form.html", {"form": form, "pk": pk})


@login_required
def address_delete(request, pk):
  get_object_or_404(Address, id=pk).delete()
  
  addresses = Address.objects.filter(customer=request.user)
  return render(request, "account/partials/address_list.html", {"addresses": addresses})


@login_required
def address_set_default(request, pk):
  Address.objects.filter(customer=request.user, default=True).update(default=False)
  Address.objects.filter(customer=request.user, id=pk).update(default=True)
  
  addresses = Address.objects.filter(customer=request.user)
  return render(request, "account/partials/address_list.html", {"addresses": addresses})


@login_required
def wishlist_add(request, slug):
  print(request.POST)
  action = request.POST.get("action")
  product = get_object_or_404(Product, slug=slug)
  if product.wish_list.filter(id=request.user.id).exists():
    product.wish_list.remove(request.user)
  else:
    product.wish_list.add(request.user)
  
  if action:
    return render(request, "partials/header.html")
  else:
    return redirect(request.META["HTTP_REFERER"])


@login_required
def wishlist(request):
  products = Product.objects.prefetch_related("wish_list").filter(wish_list=request.user)
  return render(request, "account/wishlist.html", {"wishlist": products})


def two_factor(request):
  user = request.user 
  if user.two_step_active == True:
    user.two_step_active = False 
  else:
    user.two_step_active = True 
  user.save()
  return redirect(request.META["HTTP_REFERER"])