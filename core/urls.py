from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('review/', include("review.urls", namespace="review")),
    path('account/', include("account.urls", namespace="account")),
    path('cart/', include("cart.urls", namespace="cart")),
    path('order/', include("order.urls", namespace="order")),
    path('coupon/', include("coupon.urls", namespace="coupon")),
    path('api/', include("drf.urls", namespace="drf")),
    path('', include("store.urls", namespace="store")),
    path("__debug__", include(debug_toolbar.urls)),
]

if settings.DEBUG:
  urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT)