from django.urls import include, path
from django.views import generic
from django.contrib.auth import views as auth_views

from . import views 
from .forms import UserLoginForm, PwdResetForm

app_name = "account"

urlpatterns = [
  path("register/", views.RegistrationFormView.as_view(), name="register"),
  path("activate/<slug:uidb64>/<slug:token>/", views.account_activate, name="activate"),
  path("logout/", auth_views.LogoutView.as_view(next_page="/account/login/"), name="logout"),
  path("login/", views.MyLoginView.as_view(), name="login"),
  path("otp-verification/", views.two_factor_auth, name="tf_verification"),
  # path("login/", auth_views.LoginView.as_view(
  #   template_name="account/login.html", 
  #   form_class=UserLoginForm), name="login"),
  path("password_reset/", auth_views.PasswordResetView.as_view(
    template_name="account/password_reset_form.html",
    success_url = "/account/reset-password-sent/",
    email_template_name='account/email/password_reset_email.html',
    form_class=PwdResetForm,
    ), name="password-reset"),
    
  path('password_reset_confirm/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(
      template_name="account/password_reset_confirm.html",
      success_url="/account/password-reset-complete/"), 
      name="password_reset_confirm"),
  
  path('reset-password-sent/', 
    auth_views.PasswordResetDoneView.as_view(
      template_name="account/password_reset_sent.html"), 
      name="password_reset_done"),
    
  path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
      template_name="account/password_reset_complete.html"),
      name="password_reset_complete"),
    
  # USER DASHBOARD
  path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
  path("profile/edit/", views.user_update, name="edit_detail"),
  path("profile/delete/", views.delete_user, name="delete_account"),
  path("profile/delete-confirm/", generic.TemplateView.as_view(template_name="account/delete_confirm.html"), name="delete_confirm"),
  path("two-factor/activation/", views.two_factor, name="tf_activation"),
  
  # ADDRESS 
  path("addresses/", views.AddressListView.as_view(), name="addresses"),
  path("add-address/", views.address_add, name="address_add"),
  path("update-address/<slug:pk>/", views.address_update, name="address_update"),
  path("delete-address/<slug:pk>/", views.address_delete, name="address_delete"),
  path("set-default/<slug:pk>/", views.address_set_default, name="address_set_default"),
  
  # WISH LIST
path("wishlist/add/<int:pk>/", views.wish_list_add, name="wishlist_add"),
path("wishlist/", views.wishlist, name="wishlist"),
]