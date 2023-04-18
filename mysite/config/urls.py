from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
# from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/accounts/login/')),
    path('accounts/', include('accounts.urls')),
    path('shop/', include('shop.urls')),
]
