from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("store.urls", namespace="store")),
    path('review/', include("review.urls", namespace="review")),
    path('account/', include("account.urls", namespace="account")),
]

if settings.DEBUG:
  urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT)