from django.conf.urls import url
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^request/$',views.requestItem,name='request_item'),
    url(r'^profile/edit$', views.editprofile, name='edit_profile'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^claim/(?P<id>\d+)/$', views.claim, name='claim'),
    url(r'^upload/$', views.upload_view, name='upload'),
    path('guide', views.guide_view, name='guide')
]