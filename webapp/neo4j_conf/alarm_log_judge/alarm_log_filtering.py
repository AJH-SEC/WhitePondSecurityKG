# -*-coding:utf-8-*-
import datetime
import json
from webapp.const import LABEL_LIST
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, Subgraph
from django.conf import settings

graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
# graph = Graph("neo4j://localhost:7687", auth=('neo4j', '123456'))


def judge_log_filter(source__ip:str, target__ip:str):
    """
    判断告警日志是否在日志中
    @param source__ip: 源IP
    @param target__ip: 目的IP
    @return:
    """

    now = datetime.datetime.now()
    time_now = datetime.datetime.strftime(now, "%Y-%m-%dT%H:%M:%S.%fZ")
    interval = now + datetime.timedelta(seconds=30)                 # 间隔时间30秒
    interval = interval.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    query = f"""MATCH (n WHERE NONE(l in LABELS(n) WHERE l IN {LABEL_LIST}) AND
                        n.source__ip='{source__ip}' OR n.destination__ip='{target__ip}')
                WHERE n.event__start > '{time_now}' AND n.event__end < '{interval}'
                RETURN n AS node"""
    node_info = graph.run(query).data()         # list
    if node_info == []:
        # print('目前没有异常告警日志')
        return '目前没有异常告警日志'
    else:
        # return json.dumps(node_info, indent=4)
        return node_info



if __name__ == '__main__':
    source__ip = '192.168.1.140'
    target__ip = '192.168.1.0'
    judge_log_filter(source__ip, target__ip)

































