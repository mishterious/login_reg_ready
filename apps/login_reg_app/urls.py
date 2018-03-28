from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    url(r'^$', views.index),     # This line has changed!
    url(r'^add_user$', views.add_user), 
    url(r'^login$', views.login),
    url(r'^add_quote$', views.add_quote),
    url(r'^add_to_list/(?P<id>\d+)$', views.add_to_list),
    url(r'^see_user_posts/(?P<id>\d+)$', views.see_user_posts),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^quotes$', views.quotes),
    url(r'^logout$', views.logout),
]