
import json
import os
import time
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from webapp.neo4j_conf.hit_rule.data_conversion import read_excel
from webapp.neo4j_conf.hit_rule.hit_map import show_rule, create_singleRule, search_rule, delete_rule, load_graph
from webapp.shortcuts.ajax import ajax_success, ajax_error


@login_required
def rule_target(request, template_name):
    """
    rule_target 页面
    """

    return render(request, template_name)


@login_required
def rule_target_data(request):
    """
    rule_target datatables展示的数据
    """
    node_label = 'Rule'
    data = {'data': show_rule(node_label)}
    return HttpResponse(json.dumps(data))


@login_required
def rule_target_create(request):
    """
    rule_target 创建
    """
    try:
        dic = request.POST.dict()
        dic.pop('csrfmiddlewaretoken')
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        dic.update({'created': now_str, 'last_modified': now_str})
        node_label = 'Rule'
        create_ret = create_singleRule(node_label, dic)
        if create_ret == "此节点已经存在":
            return ajax_error("此节点已经存在")
        return ajax_success()
    except Exception as e:
        return ajax_error("创建失败")


@login_required
def rule_target_search(request):
    """
    rule_target 搜索
    """
    dic = request.GET.dict()
    dic.pop('_')
    node_label = 'Rule'
    data = {'data': search_rule(node_label, dic)}
    return HttpResponse(json.dumps(data))


@login_required
def rule_target_delete(request):
    """
    rule_target 删除
    """
    try:
        req = request.GET.dict()
        logvalue = req.get('log_value')
        node_label = 'Rule'
        delete_rule(node_label, {'log_value': logvalue})
        return ajax_success()
    except Exception as e:
        return ajax_error("删除失败")


@login_required
def rule_target_import_data(request):
    """
    rule_target 批量导入
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
            cache_path = os.path.join(dir_path, 'static', 'cache_rule')
            read_excel(excel, cache_path)
            time.sleep(3)
            load_graph(cache_path)

            return ajax_success()
        except Exception as ex:
            print(ex)
            return ajax_error('创建图谱失败')
    else:
        return ajax_error("上传失败")


@login_required
def rule_target_operation(request, id):
    """
    rule_target 操作
    """
    try:
        dic = request.GET.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        dic.update({'last modified': now_str})
        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")


