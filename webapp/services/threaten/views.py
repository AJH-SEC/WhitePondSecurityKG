
import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from webapp.neo4j_conf.log_search.log_cof import show_node_property
from webapp.neo4j_conf.threaten_hit.count_number import log_hit_search, log_hit_info
from webapp.shortcuts.ajax import ajax_success, ajax_error


@login_required
def threaten(request, template_name):
    """
    threaten 页面
    """
    type1 = show_node_property('type')
    res = {'type': type1}
    return render(request, template_name, res)


@login_required
def threaten_data(request):
    """
    threaten 数据
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
    # 存在查询条件则按照条件查询
    if ao_search:
        all_node, info_count = log_hit_search(ao_search, iDisplayStart, iDisplayLength)
    else:
        all_node, info_count = log_hit_info(iDisplayStart, iDisplayLength)
    res1 = {"draw": sEcho, "data": all_node, "recordsFiltered": info_count, "recordsTotal": info_count}
    return HttpResponse(json.dumps(res1))


@login_required
def threaten_create(request):
    """
    threaten 创建
    """
    try:
        dic = request.GET.dict()
        dic.pop('_')
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        dic.update({'created': now_str, 'last modified': now_str})
        res = {
            "data": [

            ]
        }
        data = json.dumps(res)
        return HttpResponse(data)
    except Exception as e:
        return ajax_error("查找失败")


@login_required
def threaten_search(request):
    """
    threaten 搜索
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
def threaten_import_data(request):
    """
    threaten 批量导入
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
        # try:
        #     dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        #     dir_path = os.path.dirname(dir_path)
        #     cache_path = os.path.join(dir_path, 'static', 'cache_data')
        #     read_excel(excel, cache_path)
        #     time.sleep(10)
        #     load_graph(cache_path)
        #
        #     return ajax_success()
        # except Exception as ex:
        #     # print(ex)
        #     return ajax_error('创建图谱失败')
        return ajax_success()

    else:
        return ajax_error("上传失败")


@login_required
def threaten_operation(request, id):
    """
    threaten 操作
    """
    try:
        dic = request.GET.dict()
        now = datetime.now()
        now_str = now.strftime("%d %B %Y")
        dic.update({'last modified': now_str})
        return ajax_success()
    except Exception as e:

        return ajax_error("删除失败")