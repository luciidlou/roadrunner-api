"""roadrunner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from roadrunnerapi.views import (BidView, EndorsementView, FreightTypeView,
                                 LoadStatusView, LoadView, TrailerTypeView,
                                 TruckView, AppUserView, login_user, register_user)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'loads', LoadView, 'load')
router.register(r'trucks', TruckView, 'truck')
router.register(r'endorsements', EndorsementView, 'endorsement')
router.register(r'trailertypes', TrailerTypeView, 'trailertype')
router.register(r'freighttypes', FreightTypeView, 'freighttype')
router.register(r'loadstatuses', LoadStatusView, 'loadstatus')
router.register(r'bids', BidView, 'bid')
router.register(r'users', AppUserView, 'user')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
