from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^api/posts/(?P<pk>[0-9]+)$', views.get_delete_update_post, name='get_delete_update_post'),
    url(r'^api/posts/like/(?P<pk>[0-9]+)$', views.like_post, name='like_post'),
    url(r'^api/posts/unlike/(?P<pk>[0-9]+)$', views.unlike_post, name='unlike_post'),
    url(r'^api/posts/$', views.get_post_posts, name='get_post_posts'),
]