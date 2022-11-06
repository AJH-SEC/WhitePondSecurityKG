from django.conf.urls import url

from webapp.services.rule import views

urlpatterns = [
    # 命中规则
    url(r'^target/$', views.rule_target, {"template_name": "rule/rule.html"}, name="rule"),
    url(r'^target/data/$', views.rule_target_data),
    url(r'^target/data/create/$', views.rule_target_create),
    url(r'^target/data/search/$', views.rule_target_search),
    # url(r'^target/data/delete/(?P<logvalue>[\w\-]+)/$', views.rule_target_delete),
    url(r'^target/data/delete/$', views.rule_target_delete),
    url(r'^target/import/data/$', views.rule_target_import_data),
    # url(r'^target/operation/(?P<id>\w+)/$', views.rule_target_operation),
]

