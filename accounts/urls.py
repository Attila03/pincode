from django.conf.urls import url
from .views import Register, Address, DisplayPin, Login, Logout

urlpatterns = [
    url(r'register/$', Register.as_view(), name='register'),
    url(r'address/$', Address.as_view(), name='address'),
    url(r'displaypin/$', DisplayPin.as_view(), name='displaypin'),
    url(r'login/$', Login.as_view(), name='login'),
    url(r'logout/$', Logout.as_view(), name='logout'),
]