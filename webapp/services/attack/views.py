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
    总览页面
    """
    dic = showNode()

    return render(request, template_name, dic)


@login_required
def attack_overview_data(request):
    """
    总览页面 柱状图数据
    """
    try:
        dic = showNode()
        return ajax_success(data=dic)
    except Exception as e:
        return ajax_error("数据加载失败")


@login_required
def attack_overview_import_data(request):
    """
    总览页面 批量导入
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
            # 处理excel
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
    战术管理 页面
    """

    return render(request, template_name)


@login_required
def attack_tactics_data(request):
    """
    战术管理 datatables展示的数据
    """
    data_value = searchNode(NodeLabel.TACTICS)
    for oen_data in data_value:
        if "name_zh" not in oen_data.keys():
            oen_data["name_zh"] = ""
        if "description_zh" not in oen_data.keys():
            oen_data["description_zh"] = ""
    data = {'data': data_value}
    return HttpResponse(json.dumps(data))


@login_required
def attack_tactics_create(request):
    """
    战术管理 创建
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
    战术管理 数据修改
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
    战术管理 删除
    """
    try:
        deleteNode(NodeLabel.TACTICS, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_technology(request, template_name):
    """
    技术管理 页面
    """

    return render(request, template_name)


@login_required
def attack_technology_data(request):
    """
    技术管理 datatables展示的数据
    """
    data_value = searchNode(NodeLabel.TECHNIQUES)
    for oen_data in data_value:
        if "name_zh" not in oen_data.keys():
            oen_data["name_zh"] = ""
        if "description_zh" not in oen_data.keys():
            oen_data["description_zh"] = ""
    data = {'data': data_value}
    return HttpResponse(json.dumps(data))


@login_required
def attack_technology_create(request):
    """
    技术管理 创建
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
    技术管理 修改
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
    技术管理 删除
    """
    try:
        deleteNode(NodeLabel.TECHNIQUES, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_sub_technology(request, template_name):
    """
    子技术管理 页面
    """

    return render(request, template_name)


@login_required
def attack_sub_technology_data(request):
    """
    子技术管理 数据
    """
    data_value = searchNode(NodeLabel.SUBTECHNIQUES)
    for oen_data in data_value:
        if "name_zh" not in oen_data.keys():
            oen_data["name_zh"] = ""
        if "description_zh" not in oen_data.keys():
            oen_data["description_zh"] = ""
    data = {'data': data_value}
    return HttpResponse(json.dumps(data))


@login_required
def attack_sub_technology_create(request):
    """
    子技术管理 创建
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
    子技术管理 修改
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
    子技术管理 删除
    """
    try:
        deleteNode(NodeLabel.SUBTECHNIQUES, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_mitigations(request, template_name):
    """
    缓解措施管理 页面
    """

    return render(request, template_name)


@login_required
def attack_mitigations_data(request):
    """
    缓解措施管理 数据
    """
    data_value = searchNode(NodeLabel.MITIGATIONS)
    for oen_data in data_value:
        if "name_zh" not in oen_data.keys():
            oen_data["name_zh"] = ""
        if "description_zh" not in oen_data.keys():
            oen_data["description_zh"] = ""
    data = {'data': data_value}
    return HttpResponse(json.dumps(data))


@login_required
def attack_mitigations_create(request):
    """
    缓解措施管理 创建
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
    缓解措施管理 修改
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
    缓解措施管理 删除
    """
    try:
        deleteNode(NodeLabel.MITIGATIONS, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_organization(request, template_name):
    """
    组织管理 页面
    """

    return render(request, template_name)


@login_required
def attack_organization_data(request):
    """
    组织管理 数据
    """
    data_value = searchNode(NodeLabel.GROUPS)
    for oen_data in data_value:
        if "name_zh" not in oen_data.keys():
            oen_data["name_zh"] = ""
        if "description_zh" not in oen_data.keys():
            oen_data["description_zh"] = ""
    data = {'data': data_value}
    return HttpResponse(json.dumps(data))


@login_required
def attack_organization_create(request):
    """
    组织管理 创建
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
    组织管理 修改
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
    组织管理 删除
    """
    try:
        deleteNode(NodeLabel.GROUPS, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_software(request, template_name):
    """
    软件管理 页面
    """

    return render(request, template_name)


@login_required
def attack_software_data(request):
    """
    软件管理 数据
    """
    data_value = searchNode(NodeLabel.SOFTWARE)
    for oen_data in data_value:
        if "name_zh" not in oen_data.keys():
            oen_data["name_zh"] = ""
        if "description_zh" not in oen_data.keys():
            oen_data["description_zh"] = ""
    data = {'data': data_value}
    return HttpResponse(json.dumps(data))


@login_required
def attack_software_create(request):
    """
    软件管理 创建
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
    软件管理 修改
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
    软件管理 删除
    """
    try:
        deleteNode(NodeLabel.SOFTWARE, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_data_sources(request, template_name):
    """
    数据资源管理 页面
    """

    return render(request, template_name)


@login_required
def attack_data_sources_data(request):
    """
    数据资源管理 数据
    """
    data_value = searchNode(NodeLabel.DATASOURCE)
    for oen_data in data_value:
        if "name_zh" not in oen_data.keys():
            oen_data["name_zh"] = ""
        if "description_zh" not in oen_data.keys():
            oen_data["description_zh"] = ""
    data = {'data': data_value}
    return HttpResponse(json.dumps(data))


@login_required
def attack_data_sources_create(request):
    """
    数据资源管理 创建
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
    数据资源管理 修改
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
    数据资源管理 删除
    """
    try:
        deleteNode(NodeLabel.DATASOURCE, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_datasource_component(request, template_name):
    """
    数据组件 页面
    """

    return render(request, template_name)


@login_required
def attack_datasource_component_data(request):
    """
    数据组件 数据
    """
    data_value = searchNode(NodeLabel.DATASOURCECOMPONENT)
    for oen_data in data_value:
        if "name_zh" not in oen_data.keys():
            oen_data["name_zh"] = ""
        if "description_zh" not in oen_data.keys():
            oen_data["description_zh"] = ""
    data = {'data': data_value}
    return HttpResponse(json.dumps(data))


@login_required
def attack_datasource_component_create(request):
    """
    数据组件 创建
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
    数据组件 修改
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
    数据组件 删除
    """
    try:
        deleteNode(NodeLabel.DATASOURCECOMPONENT, {'name': name})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_campaign(request, template_name):
    """
    战役 页面
    """

    return render(request, template_name)


@login_required
def attack_campaign_data(request):
    """
    战役 datatables数据
    """
    data_value = searchNode(NodeLabel.CAMPAIGN)
    for oen_data in data_value:
        if "name_zh" not in oen_data.keys():
            oen_data["name_zh"] = ""
        if "description_zh" not in oen_data.keys():
            oen_data["description_zh"] = ""
    data = {'data': data_value}
    return HttpResponse(json.dumps(data))


@login_required
def attack_campaign_create(request):
    """
    战役 创建
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
    战役 修改
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
    战役 删除
    """
    try:
        deleteNode(NodeLabel.CAMPAIGN, {'name': name})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


@login_required
def attack_relationship(request, template_name):
    """
    关系页面
    """
    # res = showNode(only_show=True)
    res = {'label': ATTACK_LABEL_LIST}

    return render(request, template_name, res)


@login_required
def attack_relationship_data(request, name):
    """
    关系页面datatables数据
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
    新建节点关系
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
        # 关系属性名和属性值
        if attribute_name and attribute_value:
            relation_properties = {attribute_name: attribute_value}
        else:
            relation_properties = None
        # 关系指向
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
    关系修改
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

        modifyRelationship(node1_label, node1, node2_label, node2, rel, new_rel)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def attack_relationship_delete(request, id):
    """
    关系删除
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
    关系 根据标签查询数据
    """
    try:
        # 只查询名称 数据为列表
        res = searchNode(name, only_show=True)
        return ajax_success(data=res)
    except Exception as e:

        return ajax_error("查询失败")


