from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "order"

urlpatterns = [
  path("", login_required(views.OrderListView.as_view()), name="orders"),
]