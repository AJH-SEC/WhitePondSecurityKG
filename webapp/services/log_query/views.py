
import json
from datetime import datetime
import ast
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from webapp.neo4j_conf.log_search.log_cof import show_node_property, search_node, show_node, add_property
from webapp.shortcuts.ajax import ajax_success, ajax_error


@login_required
def log_query(request, template_name):
    """
    log_query 页面
    """
    type1 = show_node_property('type')
    event__type = show_node_property('event__type')
    res = {'type': type1, 'event__type': event__type}
    return render(request, template_name, res)


@login_required
def log_query_data(request):
    """
    log_query 数据
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
            reservationtime_str = ao_search.get('reservationtime')
            event__type = ao_search.get('event__type')
            if reservationtime_str:
                start, end = reservationtime_str.split(' - ')
                start = datetime.strptime(start, '%m/%d/%Y %I:%M %p').strftime('%Y-%m-%dT%H:%M:%S.000Z')
                end = datetime.strptime(end, '%m/%d/%Y %I:%M %p').strftime('%Y-%m-%dT%H:%M:%S.000Z')
                reservationtime_str1 = (' - ').join([start, end])
                ao_search.update(reservationtime=reservationtime_str1)
            if event__type:
                event__type = ast.literal_eval(event__type)
                ao_search.update(event__type=event__type)
        if ao_name == 'iDisplayStart':
            iDisplayStart = ao.get('value', None)
        if ao_name == 'iDisplayLength':
            iDisplayLength = ao.get('value', None)
        if ao_name == 'sEcho':
            sEcho = ao.get('value', None)
    # 存在查询条件则按照条件查询
    if ao_search:
        all_node, info_count = search_node(ao_search, iDisplayStart, iDisplayLength)
    else:
        all_node, info_count = show_node(iDisplayStart, iDisplayLength)
    res1 = {"draw": sEcho, "data": all_node, "recordsFiltered": info_count, "recordsTotal": info_count}
    return HttpResponse(json.dumps(res1))


@login_required
def log_query_search(request):
    """
    log_query 搜索
    """
    try:
        dic = request.GET.dict()
        dic.pop('_')
        res = {
            "data": [

            ]
        }
        data = json.dumps(res)
        return HttpResponse(data)
    except Exception as e:
        return ajax_error("查找失败")


@login_required
def log_query_operation(request):
    """
    log_query 操作
    """
    try:
        dic = request.GET.dict()
        name = dic.pop('name')
        now = datetime.now()
        mlsec = now.strftime('%Y-%m-%d %I:%M:%S.%f').split('.')[1][:3]
        now_str = now.strftime('%Y-%m-%dT%I:%M:%S.{}Z'.format(mlsec))
        dic.update({'last modified': now_str})
        add_property({"name": name}, dic)
        return ajax_success()
    except Exception as e:

        return ajax_error("操作失败")

