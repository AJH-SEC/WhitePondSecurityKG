from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.contrib import admin

from webapp import views

urlpatterns = [
    url(r'^login/$', views.login, {"template_name": "login.html"}, name="login"),
    url(r'^accounts/login/$', views.login, {"template_name": "login.html"}, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^index/$', views.index, {"template_name": "base.html"}, name="index"),
    url(r'^start/$', views.index, {"template_name": "starter.html"}, name="start"),
    url(r'^$', RedirectView.as_view(url='/index/', permanent=True), name="default"),
    url(r'^attack/', include('webapp.urls.attack.urls')),
    url(r'^logquery/', include('webapp.urls.log_query.urls')),
    url(r'^rule/', include('webapp.urls.rule.urls')),
    url(r'^threaten/', include('webapp.urls.threaten.urls')),
    url(r'^information/', include('webapp.urls.information.urls')),
    url(r'^home/$', views.home, {"template_name": "home.html"}, name="home"),
    url(r'^home/data/$', views.home_data),
    url(r'^home/data/line/$', views.home_data_line),
    url(r'^home/data/radar/$', views.home_data_radar),

]
