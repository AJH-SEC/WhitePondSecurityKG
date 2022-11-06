from django.conf.urls import url

from webapp.services.industry import views

urlpatterns = [
    # 行业
    url(r'^industry_management/$', views.industry_management, {"template_name": "industry/industry.html"}, name="industry_management"),
    url(r'^industry_management/data/$', views.industry_management_data),
    url(r'^industry_management/data/edit/(?P<id>\w+)/$', views.industry_management_edit),
    url(r'^industry_management/delete/(?P<id>\w+)/$', views.industry_management_delete),
]

