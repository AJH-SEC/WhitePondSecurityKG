import json
import os
import time
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from webapp.const import NodeLabel, ATTACK_LABEL_LIST
from webapp.neo4j_conf.attack_manage.cretate_graph import load_graph
from webapp.neo4j_conf.attack_manage.data_conversion import read_excel
from webapp.neo4j_conf.attack_manage.neo4j_web import showNode, searchNode, createNode, modifyNode, deleteNode, \
    showRelationships, createRelationships, modifyRelationship, deleteRelationships
from webapp.shortcuts.ajax import ajax_success, ajax_error


@login_required
def attack_overview(request, template_name):
    """
    overview页面
    """
    dic = showNode()

    return render(request, template_name, dic)


@login_required
def attack_overview_data(request):
    """
    overview数据
    """
    try:
        dic = showNode()
        return ajax_success(data=dic)
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def attack_overview_import_data(request):
    """
    overview 批量导入
    """
    if request.method != "POST":
        return ajax_error("上传失败")
    # 文件格式判断
    if request.FILES.__len__():
        file = request.FILES.get('excel')
        if file.name.split(".")[-1] != "xlsx":
            return HttpResponse(json.dumps({"error": "not_xlsx"}))
    excel = request.FILES.get("excel", None)

    if excel:
        try:
            dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            dir_path = os.path.dirname(dir_path)
            cache_path = os.path.join(dir_path, 'static', 'cache_data')
            read_excel(excel, cache_path)
            time.sleep(10)
            load_graph(cache_path)

            return ajax_success()
        except Exception as e:
            return ajax_error('创建图谱失败')

    else:
        return ajax_error("上传失败")


@login_required
def attack_tactics(request, template_name):
    """
    tactics页面
    """

    return render(request, template_name)


@login_required
def attack_tactics_data(request):
    """
    tactics数据
    """
    data = {'data': searchNode(NodeLabel.TACTICS)}
    return HttpResponse(json.dumps(data))


@login_required
def attack_tactics_create(request):
    """
    tactics 创建
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'created': now_str, 'last modified': now_str})
        create_ret = createNode(NodeLabel.TACTICS, form_dic)
        if create_ret == "此节点已经存在":
            return ajax_error("此节点已经存在")
        return ajax_success()
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def attack_tactics_edit(request, id):
    """
    tactics 数据修改
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'last modified': now_str})
        node_info = {"ID": id}
        modifyNode(NodeLabel.TACTICS, node_info, form_dic)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def attack_tactics_delete(request, id):
    """
    tactics 删除
    """
    try:
        deleteNode(NodeLabel.TACTICS, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_technology(request, template_name):
    """
    technology页面
    """

    return render(request, template_name)


@login_required
def attack_technology_data(request):
    """
    technology数据
    """
    data = {'data': searchNode(NodeLabel.TECHNIQUES)}
    return HttpResponse(json.dumps(data))


@login_required
def attack_technology_create(request):
    """
    technology 创建
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'created': now_str, 'last modified': now_str})
        create_ret = createNode(NodeLabel.TECHNIQUES, form_dic)
        if create_ret == "此节点已经存在":
            return ajax_error("此节点已经存在")
        return ajax_success()
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def attack_technology_edit(request, id):
    """
    technology 修改
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'last modified': now_str})
        node_info = {"ID": id}
        modifyNode(NodeLabel.TECHNIQUES, node_info, form_dic)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def attack_technology_delete(request, id):
    """
    technology 删除
    """
    try:
        deleteNode(NodeLabel.TECHNIQUES, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_sub_technology(request, template_name):
    """
    sub_technology 页面
    """

    return render(request, template_name)


@login_required
def attack_sub_technology_data(request):
    """
    sub_technology 数据
    """
    data = {'data': searchNode(NodeLabel.SUBTECHNIQUES)}
    return HttpResponse(json.dumps(data))


@login_required
def attack_sub_technology_create(request):
    """
    sub_technology 创建
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'created': now_str, 'last modified': now_str})
        create_ret = createNode(NodeLabel.SUBTECHNIQUES, form_dic)
        if create_ret == "此节点已经存在":
            return ajax_error("此节点已经存在")
        return ajax_success()
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def attack_sub_technology_edit(request, id):
    """
    sub_technology 修改
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'last modified': now_str})
        node_info = {"ID": id}
        modifyNode(NodeLabel.SUBTECHNIQUES, node_info, form_dic)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def attack_sub_technology_delete(request, id):
    """
    sub_technology 删除
    """
    try:
        deleteNode(NodeLabel.SUBTECHNIQUES, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_mitigations(request, template_name):
    """
    mitigations 页面
    """

    return render(request, template_name)


@login_required
def attack_mitigations_data(request):
    """
    mitigations 数据
    """
    data = {'data': searchNode(NodeLabel.MITIGATIONS)}
    return HttpResponse(json.dumps(data))


@login_required
def attack_mitigations_create(request):
    """
    mitigations 创建
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'created': now_str, 'last modified': now_str})
        create_ret = createNode(NodeLabel.MITIGATIONS, form_dic)
        if create_ret == "此节点已经存在":
            return ajax_error("此节点已经存在")
        return ajax_success()
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def attack_mitigations_edit(request, id):
    """
    mitigations 修改
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'last modified': now_str})
        node_info = {"ID": id}
        modifyNode(NodeLabel.MITIGATIONS, node_info, form_dic)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def attack_mitigations_delete(request, id):
    """
    mitigations 删除
    """
    try:
        deleteNode(NodeLabel.MITIGATIONS, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_organization(request, template_name):
    """
    organization 页面
    """

    return render(request, template_name)


@login_required
def attack_organization_data(request):
    """
    organization 数据
    """
    data = {'data': searchNode(NodeLabel.GROUPS)}
    return HttpResponse(json.dumps(data))


@login_required
def attack_organization_create(request):
    """
    organization 创建
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'created': now_str, 'last modified': now_str})
        create_ret = createNode(NodeLabel.GROUPS, form_dic)
        if create_ret == "此节点已经存在":
            return ajax_error("此节点已经存在")
        return ajax_success()
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def attack_organization_edit(request, id):
    """
    organization 修改
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'last modified': now_str})
        node_info = {"ID": id}
        modifyNode(NodeLabel.GROUPS, node_info, form_dic)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def attack_organization_delete(request, id):
    """
    organization 删除
    """
    try:
        deleteNode(NodeLabel.GROUPS, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_software(request, template_name):
    """
    software 页面
    """

    return render(request, template_name)


@login_required
def attack_software_data(request):
    """
    software 数据
    """
    data = {'data': searchNode(NodeLabel.SOFTWARE)}
    return HttpResponse(json.dumps(data))


@login_required
def attack_software_create(request):
    """
    software 创建
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'created': now_str, 'last modified': now_str})
        create_ret = createNode(NodeLabel.SOFTWARE, form_dic)
        if create_ret == "此节点已经存在":
            return ajax_error("此节点已经存在")
        return ajax_success()
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def attack_software_edit(request, id):
    """
    software 修改
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'last modified': now_str})
        node_info = {"ID": id}
        modifyNode(NodeLabel.SOFTWARE, node_info, form_dic)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def attack_software_delete(request, id):
    """
    software 删除
    """
    try:
        deleteNode(NodeLabel.SOFTWARE, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_data_sources(request, template_name):
    """
    data_sources 页面
    """

    return render(request, template_name)


@login_required
def attack_data_sources_data(request):
    """
    data_sources 数据
    """
    data = {'data': searchNode(NodeLabel.DATASOURCE)}
    return HttpResponse(json.dumps(data))


@login_required
def attack_data_sources_create(request):
    """
    data_sources 创建
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'created': now_str, 'last modified': now_str})
        create_ret = createNode(NodeLabel.DATASOURCE, form_dic)
        if create_ret == "此节点已经存在":
            return ajax_error("此节点已经存在")
        return ajax_success()
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def attack_data_sources_edit(request, id):
    """
    data_sources 修改
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'last modified': now_str})
        node_info = {"ID": id}
        modifyNode(NodeLabel.DATASOURCE, node_info, form_dic)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def attack_data_sources_delete(request, id):
    """
    data_sources 删除
    """
    try:
        deleteNode(NodeLabel.DATASOURCE, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_datasource_component(request, template_name):
    """
    datasource_component 页面
    """

    return render(request, template_name)


@login_required
def attack_datasource_component_data(request):
    """
    datasource_component 数据
    """
    data = {'data': searchNode(NodeLabel.DATASOURCECOMPONENT)}
    return HttpResponse(json.dumps(data))


@login_required
def attack_datasource_component_create(request):
    """
    datasource_component 创建
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'created': now_str, 'modified': now_str})
        create_ret = createNode(NodeLabel.DATASOURCECOMPONENT, form_dic)
        if create_ret == "此节点已经存在":
            return ajax_error("此节点已经存在")
        return ajax_success()
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def attack_datasource_component_edit(request, name):
    """
    datasource_component 修改
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'modified': now_str})
        node_info = {"name": name}
        modifyNode(NodeLabel.DATASOURCECOMPONENT, node_info, form_dic)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def attack_datasource_component_delete(request, name):
    """
    datasource_component 删除
    """
    try:
        deleteNode(NodeLabel.DATASOURCECOMPONENT, {'name': name})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_campaign(request, template_name):
    """
    datasource_component 页面
    """

    return render(request, template_name)


@login_required
def attack_campaign_data(request):
    """
    campaign 数据
    """
    data = {'data': searchNode(NodeLabel.CAMPAIGN)}
    return HttpResponse(json.dumps(data))


@login_required
def attack_campaign_create(request):
    """
    campaign 创建
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'created': now_str, 'modified': now_str})
        create_ret = createNode(NodeLabel.CAMPAIGN, form_dic)
        if create_ret == "此节点已经存在":
            return ajax_error("此节点已经存在")
        return ajax_success()
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def attack_campaign_edit(request, name):
    """
    campaign 修改
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'modified': now_str})
        node_info = {"name": name}
        modifyNode(NodeLabel.CAMPAIGN, node_info, form_dic)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def attack_campaign_delete(request, name):
    """
    campaign 删除
    """
    try:
        deleteNode(NodeLabel.CAMPAIGN, {'name': name})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_relationship(request, template_name):
    """
    relationship 页面
    """
    # res = showNode(only_show=True)
    res = {'label': ATTACK_LABEL_LIST}

    return render(request, template_name, res)


@login_required
def attack_relationship_data(request, name):
    """
    relationship 数据
    """
    print(name)
    data = {'data': showRelationships(name)}
    return HttpResponse(json.dumps(data))


# @login_required
# def attack_relationship_data(request, name):
#     """
#     relationship 数据
#     """
#     req = request.GET.get('aodata')
#     req = json.loads(req)
#     print(req, '-----------------')
#     print(type(req), '-----------------')
#     print(name)
#     all_list = showRelationships(name)
#     data = all_list[0:15]
#     total = len(all_list)
#     draw = req[0].get('value')
#     print(draw)
#     res = {"draw": draw,"data": data, "recordsFiltered": total, "recordsTotal": total}
#     # data = {'data': showRelationships(name)}
#     return HttpResponse(json.dumps(res))


@login_required
def attack_relationship_create(request):
    """
    relationship 创建
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        node1_label = form_dic.get('node1_label', None)
        node1_str = form_dic.get('node1', None)
        node2_label = form_dic.get('node2_label', None)
        node2_str = form_dic.get('node2', None)
        relation_type = form_dic.get('relationship', None)
        attribute_name = form_dic.get('attribute_name', None)
        attribute_value = form_dic.get('attribute_value', None)
        direction_left = form_dic.get('direction_left', None)
        node1 = {"name": node1_str}
        node2 = {"name": node2_str}
        if attribute_name and attribute_value:
            relation_properties = {attribute_name: attribute_value}
        else:
            relation_properties = None
        if direction_left:
            relation_direction = False
        else:
            relation_direction = True

        """
        
        
        此处数据所传参数   需要设置  
            node1_label: 节点1的标签
            node1: 节点1的信息【名字/ID】
            node2_label: 节点2的标签
            node2: 节点2的信息【名字/ID】
            relation_type: 两节点要创建的关系类型
            relation_properties: 关系属性，默认不添加关系属性
            relation_direction: 关系方向，默认为True:（）->（），False:（）<-（）
        """
        createRelationships(node1_label, node1, node2_label, node2, relation_type, relation_properties=relation_properties, relation_direction=relation_direction)

        return ajax_success()
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def attack_relationship_edit(request):
    """
    relationship 修改
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        print(form_dic)
        node1_label = form_dic.get('start_node label', None)
        node1_str = form_dic.get('start_node name', None)
        node2_label = form_dic.get('end_node label', None)
        node2_str = form_dic.get('end_node name', None)
        rel = form_dic.get('relationship', None)
        new_rel = form_dic.get('new_relationship', None)
        node1 = {"name": node1_str}
        node2 = {"name": node2_str}

        print(node1_label, node1, node2_label, node2, rel, new_rel)
        modifyRelationship(node1_label, node1, node2_label, node2, rel, new_rel)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def attack_relationship_delete(request, id):
    """
    relationship 删除
    """
    try:
        """
        此处数据所传参数   需要设置 
        节点1 label, 节点1信息【ID/name】
        节点2 label, 节点2信息【ID/name】
        关系类型
        """
        req_dic = request.GET.dict()
        node1_label = req_dic.get('start_node label', None)
        node1_str = req_dic.get('start_node name', None)
        node2_label = req_dic.get('end_node label', None)
        node2_str = req_dic.get('end_node name', None)
        relation_type = req_dic.get('relationship', None)
        node1 = {"name": node1_str}
        node2 = {"name": node2_str}
        deleteRelationships(node1_label, node1, node2_label, node2, relation_type)

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_relationship_get_node(request, name):
    """
    relationship 根据 label_type 查询数据
    """
    try:
        res = searchNode(name, only_show=True)
        return ajax_success(data=res)
    except Exception as e:

        return ajax_error("查询失败")


