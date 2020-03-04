from django.conf.urls import url
from .views import CreateUserAPIView, authenticate_user, UserRetrieveUpdateAPIView

urlpatterns = [
    url(r'^register/$', CreateUserAPIView.as_view(), name='register_user'),
    url(r'^update/$', UserRetrieveUpdateAPIView.as_view(), name='get_post_users'),
    url(r'^login/$', authenticate_user, name='authenticate_user'),
]