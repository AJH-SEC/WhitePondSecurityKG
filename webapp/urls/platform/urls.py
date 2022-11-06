from django.conf.urls import url

from webapp.services.platform import views

urlpatterns = [
    # 平台
    url(r'^management/$', views.management, {"template_name": "platform/platform.html"}, name="platform_management"),
    url(r'^management/data/$', views.management_data),
    url(r'^management/data/edit/(?P<id>\w+)/$', views.management_edit),
    url(r'^management/delete/(?P<id>\w+)/$', views.management_delete),
]

