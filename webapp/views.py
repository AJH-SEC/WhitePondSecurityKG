import json
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth import login as _login, logout as _logout, authenticate

from django.conf import settings
from py2neo import Graph

from webapp.const import NodeLabel
from webapp.models import ThreatenHit
from webapp.neo4j_conf.attack_manage.neo4j_web import showNode
from webapp.neo4j_conf.home_page.home import node_count, show_node_property_value, show_hit_branch
from webapp.neo4j_conf.threaten_hit.count_number import log_hit_num
from webapp.shortcuts.ajax import ajax_error, ajax_success


@never_cache
def login(request, template_name):
    """登录"""
    if request.method == "GET":
        form = AuthenticationForm(request)
        return TemplateResponse(request, template_name, {'form': form})
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            print(user)
            if not user:
                return ajax_error("dsf")
            _login(request, user)
            return ajax_success()
        except:
            return ajax_error("dsf")


@login_required
def logout(request):
    """登出"""
    _logout(request)
    return HttpResponseRedirect("/logout/")


@login_required
def index(request, template_name):
    """首页"""

    return render(request, template_name)


@login_required
def home(request, template_name):
    """
    home 页面
    """
    dic = showNode()

    return render(request, template_name, dic)


@login_required
def home_data(request):
    """
    home ATT&CK图谱数据
    """
    try:
        graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
        data = graph.run('call db.schema.visualization').data()
        nodes = []
        nodes1 = data[0]['nodes']
        for n in nodes1:
            dic = dict(n)
            dic['id'] = str(n.identity)
            dic['label'] = dic['name']
            dic['x'] = 100
            dic['y'] = 200
            nodes.append(dic)
        relationships = data[0]['relationships']
        edges = []
        for i in relationships:
            edges_dic = {}
            start_node = str(i.start_node.identity)
            type = ''.join(list(i.types()))
            end_node = str(i.end_node.identity)
            edges_dic['source'] = start_node
            edges_dic['label'] = type
            edges_dic['target'] = end_node
            edges.append(edges_dic)
        data = {
            'nodes': nodes,
            'edges': edges,
        }
        return ajax_success(data=data)
    except Exception as e:
        return ajax_error("数据加载失败")


@login_required
def home_data_line(request):
    """
    home 日志与命中数量统计图数据
    """
    try:
        logs_list = []
        hits_list = []
        for i in range(30):
            log_today_list = []
            hit_today_list = []
            start_date = datetime.date.today() + datetime.timedelta(-i)
            start_date_str = start_date.strftime('%Y-%m-%d')
            start_date_str1 = start_date.strftime("%Y-%m-%d %H:%M:%S")
            start = start_date.strftime('%Y-%m-%dT00:00:00.000Z')
            end = start_date.strftime('%Y-%m-%dT23:59:59.999Z')
            log_count = node_count(start, end)
            info_list = log_hit_num(start_date_str1)
            # 威胁命中方法
            # try:
            #     hit_obj = ThreatenHit.objects.filter(log_date=start_date_str).first()
            #     if hit_obj:
            #         hit_obj.hit_count += 1
            #         hit_obj.save()
            #     else:
            #         ThreatenHit.objects.create(log_date=start_date_str, hit_count=1)
            # except Exception as e:
            #     print(e)

            # 数据顺序要对应
            log_today_list.append(start_date_str)
            log_today_list.append(log_count)
            logs_list.append(log_today_list)

            # hit_obj = ThreatenHit.objects.filter(log_date=start_date_str).first()
            # hit_today_list.append(start_date_str)
            # hit_today_list.append(hit_obj.hit_count)
            hits_list.append(info_list)

        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logs_list[0][0] = now_str
        hits_list[0][0] = now_str

        data = {'logs_num': logs_list, 'hits_num': hits_list}
        return ajax_success(data=data)
    except Exception as e:
        return ajax_error("数据加载失败")


@login_required
def home_data_radar(request):
    """
    home 命中规则在战术中的分布雷达图数据
    """
    try:
        node_property = 'name'
        # # 战术标签列表
        # tactics = show_node_property_value(NodeLabel.TACTICS, node_property)
        # 命中规则在战术中的分布雷达图占比数据
        proportion, tactics = show_hit_branch(NodeLabel.TACTICS, node_property)
        data = {'tactics': tactics, 'proportion': proportion}
        return ajax_success(data=data)
    except Exception as e:
        return ajax_error("数据加载失败")

