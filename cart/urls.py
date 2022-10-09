from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "cart"

urlpatterns = [
  path("add/", views.cart_add, name="add"),
  path("", login_required(views.CartListView.as_view()), name="list"),
]