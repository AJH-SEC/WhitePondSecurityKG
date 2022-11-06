from django.conf.urls import url
from django.urls import path

from webapp.services.attack import views

urlpatterns = [
    # 总览
    url(r'^overview/$', views.attack_overview, {"template_name": "attack/overview.html"}, name="attack_overview"),
    url(r'^overview/data/$', views.attack_overview_data),
    url(r'^overview/import/data/$', views.attack_overview_import_data),
    # 战术
    url(r'^tactics/$', views.attack_tactics, {"template_name": "attack/tactics.html"}, name="attack_tactics"),
    url(r'^tactics/data/$', views.attack_tactics_data),
    url(r'^tactics/data/create/$', views.attack_tactics_create),
    url(r'^tactics/data/edit/(?P<id>\w+)/$', views.attack_tactics_edit),
    url(r'^tactics/delete/(?P<id>\w+)/$', views.attack_tactics_delete),
    # 技术
    url(r'^technology/$', views.attack_technology, {"template_name": "attack/technology.html"}, name="attack_technology"),
    url(r'^technology/data/$', views.attack_technology_data),
    url(r'^technology/data/create/$', views.attack_technology_create),
    url(r'^technology/data/edit/(?P<id>\w+)/$', views.attack_technology_edit),
    url(r'^technology/delete/(?P<id>\w+)/$', views.attack_technology_delete),
    # 子技术
    url(r'^sub_technology/$', views.attack_sub_technology, {"template_name": "attack/sub_technology.html"}, name="attack_sub_technology"),
    url(r'^sub_technology/data/$', views.attack_sub_technology_data),
    url(r'^sub_technology/data/create/$', views.attack_sub_technology_create),
    url(r'^sub_technology/data/edit/(?P<id>\w+)/$', views.attack_sub_technology_edit),
    url(r'^sub_technology/delete/(?P<id>\w+)/$', views.attack_sub_technology_delete),
    # 缓解措施
    url(r'^mitigations/$', views.attack_mitigations, {"template_name": "attack/mitigations.html"}, name="attack_mitigations"),
    url(r'^mitigations/data/$', views.attack_mitigations_data),
    url(r'^mitigations/data/create/$', views.attack_mitigations_create),
    url(r'^mitigations/data/edit/(?P<id>\w+)/$', views.attack_mitigations_edit),
    url(r'^mitigations/delete/(?P<id>\w+)/$', views.attack_mitigations_delete),
    # 组织
    url(r'^organization/$', views.attack_organization, {"template_name": "attack/organization.html"}, name="attack_organization"),
    url(r'^organization/data/$', views.attack_organization_data),
    url(r'^organization/data/create/$', views.attack_organization_create),
    url(r'^organization/data/edit/(?P<id>\w+)/$', views.attack_organization_edit),
    url(r'^organization/delete/(?P<id>\w+)/$', views.attack_organization_delete),
    # 软件
    url(r'^software/$', views.attack_software, {"template_name": "attack/software.html"}, name="attack_software"),
    url(r'^software/data/$', views.attack_software_data),
    url(r'^software/data/create/$', views.attack_software_create),
    url(r'^software/data/edit/(?P<id>\w+)/$', views.attack_software_edit),
    url(r'^software/delete/(?P<id>\w+)/$', views.attack_software_delete),
    # 数据资源
    url(r'^data_sources/$', views.attack_data_sources, {"template_name": "attack/data_sources.html"}, name="attack_data_sources"),
    url(r'^data_sources/data/$', views.attack_data_sources_data),
    url(r'^data_sources/data/create/$', views.attack_data_sources_create),
    url(r'^data_sources/data/edit/(?P<id>\w+)/$', views.attack_data_sources_edit),
    url(r'^data_sources/delete/(?P<id>\w+)/$', views.attack_data_sources_delete),
    # 数据组件
    url(r'^datasource_component/$', views.attack_datasource_component, {"template_name": "attack/datasource_component.html"}, name="attack_datasource_component"),
    url(r'^datasource_component/data/$', views.attack_datasource_component_data),
    url(r'^datasource_component/data/create/$', views.attack_datasource_component_create),
    url(r'^datasource_component/data/edit/(?P<name>\w+)/$', views.attack_datasource_component_edit),
    url(r'^datasource_component/delete/(?P<name>\w+)/$', views.attack_datasource_component_delete),
    # 战役
    url(r'^campaign/$', views.attack_campaign, {"template_name": "attack/campaign.html"}, name="attack_campaign"),
    url(r'^campaign/data/$', views.attack_campaign_data),
    url(r'^campaign/data/create/$', views.attack_campaign_create),
    url(r'^campaign/data/edit/(?P<name>\w+)/$', views.attack_campaign_edit),
    url(r'^campaign/delete/(?P<name>\w+)/$', views.attack_campaign_delete),
    # 关系管理
    url(r'^relationship/$', views.attack_relationship, {"template_name": "attack/relationship.html"}, name="attack_relationship"),
    # url(r'^relationship/data/$', views.attack_relationship_data),
    url(r'^relationship/data/(?P<name>\w+)/$', views.attack_relationship_data),
    url(r'^relationship/create/$', views.attack_relationship_create),
    url(r'^relationship/edit/$', views.attack_relationship_edit),
    url(r'^relationship/delete/(?P<id>\w+)/$', views.attack_relationship_delete),
    url(r'^relationship/get_node/(?P<name>\w+)/$', views.attack_relationship_get_node),

]

