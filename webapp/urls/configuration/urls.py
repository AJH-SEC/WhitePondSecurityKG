from django.conf.urls import url

from webapp.services.configuration import views

urlpatterns = [
    url(r'^conf/$', views.configuration, {"template_name": "configuration/configuration.html"}, name="configuration"),
    url(r'^conf/save/$', views.configuration_save),
]

