from django.urls import path

from . import views

app_name = "review"
urlpatterns = [
  path("", views.review_submit, name="submit"),
]