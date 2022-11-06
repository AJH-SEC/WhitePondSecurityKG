from django.conf.urls import url

from webapp.services.threaten import views

urlpatterns = [
    # 威胁命中
    url(r'^target/$', views.threaten, {"template_name": "threaten/threaten.html"}, name="threaten"),
    url(r'^target/data/$', views.threaten_data),
    # url(r'^target/data/create/$', views.threaten_create),
    # url(r'^target/data/search/$', views.threaten_search),
    # url(r'^target/import/data/$', views.threaten_import_data),
    # url(r'^target/operation/(?P<id>\w+)/$', views.threaten_operation),
]

