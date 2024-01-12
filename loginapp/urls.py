"""URLs module"""
from django.conf import settings
from django.urls import path
from social_core.utils import setting_name

from social_django import views
from . import views as new_views
extra = getattr(settings, setting_name("TRAILING_SLASH"), True) and "/" or ""

app_name = "social"

urlpatterns = [
    # authentication / association
    path(f"login/<str:backend>{extra}", views.auth, name="begin"),
    path(f"complete/<str:backend>{extra}", views.complete, name="complete"),
    # disconnection
    path(f"disconnect/<str:backend>{extra}", views.disconnect, name="disconnect"),
    path(
        f"disconnect/<str:backend>/<int:association_id>{extra}",
        views.disconnect,
        name="disconnect_individual",
    ),
    path('sociallogin/',new_views.sociallogin,name = 'sociallogin'),

]
