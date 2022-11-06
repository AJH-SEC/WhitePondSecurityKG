
import json
from datetime import datetime
import ast
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from webapp.const import ATTACK_LABEL_LIST
from webapp.neo4j_conf.attack_manage.neo4j_web import deleteNode
from webapp.neo4j_conf.platform_class.platforms import platforms_search, platforms_type, modify_industry_property
from webapp.shortcuts.ajax import ajax_success, ajax_error


@login_required
def management(request, template_name):
    """
    platform 页面
    """
    platforms = platforms_type()
    res = {'attack_label_list': ATTACK_LABEL_LIST, 'platforms': platforms}
    return render(request, template_name, res)


@login_required
def management_data(request):
    """
    platform datatables展示的数据
    sEcho 数据加载次数
    iDisplayStart 数据起始位置
    iDisplayLength 请求数据量
    recordsTotal、recordsFiltered 数据总数
    """
    # 开启服务端模式后datatables提交的数据
    aodata = request.GET.get('aodata')
    aodata = json.loads(aodata)
    ao_search = {'platforms': 'Windows'}
    sEcho = 0
    iDisplayStart = 0
    iDisplayLength = 15
    for ao in aodata:
        ao_name = ao.get('name', None)
        if ao_name == 'search':
            ao_search = ao.get('value', None)
        if ao_name == 'iDisplayStart':
            iDisplayStart = ao.get('value', None)
        if ao_name == 'iDisplayLength':
            iDisplayLength = ao.get('value', None)
        if ao_name == 'sEcho':
            sEcho = ao.get('value', None)
    all_node, info_count = platforms_search(ao_search, iDisplayStart, iDisplayLength)
    res1 = {"draw": sEcho, "data": all_node, "recordsFiltered": info_count, "recordsTotal": info_count}
    return HttpResponse(json.dumps(res1))


@login_required
def management_edit(request, id):
    """
    platform 修改
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        form_dic = request.POST.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'last modified': now_str})
        node_info = {"ID": id}

        #修改平台信息
        modify_industry_property(node_info, form_dic)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def management_delete(request, id):
    """
    platform 删除
    """
    try:
        dic = request.GET.dict()
        label = dic.get('label')
        deleteNode(label, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")

