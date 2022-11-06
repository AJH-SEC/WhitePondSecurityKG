from django.conf.urls import url

from webapp.services.log_query import views

urlpatterns = [
    # 日志查询
    url(r'^query/$', views.log_query, {"template_name": "log_query/log_query.html"}, name="log_query"),
    url(r'^query/data/$', views.log_query_data),
    # 没有使用
    # url(r'^query/data/search/$', views.log_query_search),
    # url(r'^query/operation/(?P<name>\w+)/$', views.log_query_operation),
    url(r'^query/operation/$', views.log_query_operation),
]

