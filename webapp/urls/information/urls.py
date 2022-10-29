from django.conf.urls import url

from webapp.services.information import views

urlpatterns = [
    url(r'^target/$', views.information, {"template_name": "information/information.html"}, name="information"),
    url(r'^target/data/$', views.information_data),
    # url(r'^target/data/create/$', views.information_create),
    # url(r'^target/data/search/$', views.information_search),
    # url(r'^target/import/data/$', views.information_import_data),
    # url(r'^target/operation/(?P<id>\w+)/$', views.information_operation),
]

