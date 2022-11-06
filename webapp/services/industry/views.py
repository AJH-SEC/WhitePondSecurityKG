
import json
from datetime import datetime
import ast
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from webapp.const import ATTACK_LABEL_LIST
from webapp.models import Configuration
from webapp.neo4j_conf.attack_manage.neo4j_web import deleteNode
from webapp.neo4j_conf.industry_manage.industry import industry_search, modify_industry_property
from webapp.neo4j_conf.platform_class.platforms import platforms_search, platforms_type
from webapp.shortcuts.ajax import ajax_success, ajax_error


@login_required
def industry_management(request, template_name):
    """
    industry 页面
    """
    industry_list = Configuration.objects.values_list('industry', flat=True)
    res = {'attack_label_list': ATTACK_LABEL_LIST, 'industry_list': industry_list}
    return render(request, template_name, res)


@login_required
def industry_management_data(request):
    """
    industry datatables展示的数据
    aodata 开启服务端模式后datatables提交的数据
    sEcho 数据加载次数
    iDisplayStart 数据起始位置
    iDisplayLength 请求数据量
    recordsTotal、recordsFiltered 数据总数
    """
    aodata = request.GET.get('aodata')
    aodata = json.loads(aodata)
    ao_search = {}
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
    all_node, info_count = industry_search(ao_search, iDisplayStart, iDisplayLength)
    res1 = {"draw": sEcho, "data": all_node, "recordsFiltered": info_count, "recordsTotal": info_count}
    return HttpResponse(json.dumps(res1))


@login_required
def industry_management_edit(request, id):
    """
    industry 修改行业
    """
    if request.method != "POST":
        return ajax_error("请求方式错误")
    try:
        industry_list = request.POST.getlist('select2_industry')
        industry = ','.join(industry_list)
        form_dic = {}
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        form_dic.update({'last modified': now_str})
        form_dic.update({'industry': industry})
        node_info = {"ID": id}
        modify_industry_property(node_info, form_dic)

        return ajax_success()
    except Exception as e:
        return ajax_error("修改失败")


@login_required
def industry_management_delete(request, id):
    """
    industry 删除单条数据
    """
    try:
        dic = request.GET.dict()
        label = dic.get('label')
        deleteNode(label, {'ID': id})

        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")

