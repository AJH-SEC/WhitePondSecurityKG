# -*-coding:utf-8-*-
import datetime
import json

from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, Subgraph
from django.conf import settings

graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
# graph = Graph("neo4j://localhost:7687", auth=('neo4j', '123456'))


def threaten_hit_rule(log_info: dict, label_list: list):
    """
    威胁命中规则 将命中的日志与规则之间建立关系 `log hit rule` 属性为日期
    @param log_info: 日志信息, eg: "日志字段值 {} key为日志任意能确定此日志的属性名 value为key所对应的值"
    @param label_list: 日志除外的节点label【为了排除一些节点，加快速度】,
                        eg: label_list = ['SubTechniques', 'Techniques', 'Tactics', 'Citations', 'Datasource',
                                        'DatasourceComponent', 'Software', 'Groups', 'Mitigations']
    @return:
    """
    # query = f"""MATCH (n) WHERE NONE(l IN LABELS(n) WHERE l IN {label_list}) AND n.name='{name}' RETURN n"""
    #
    # query_tec = f"""MATCH (tech)-[]-(log)
    #                 WHERE NONE(label_1 IN LABELS(log) WHERE label_1 IN {label_list})
    #                 AND log.`log value`='{name}'
    #                 RETURN tech.name AS techniques"""
    #
    # query_information = f"""MATCH (gs)-[]-(tech)-[rel_1]-(log)
    #                         WHERE NONE(label_1 IN LABELS(log) WHERE label_1 IN {label_list})
    #                         AND ANY(label_2 IN LABELS(gs) WHERE label_2 IN ['Groups', 'Software'])
    #                         AND log.`log value`='{name}'
    #                         RETURN gs.name"""

    # query_rule = f"""MATCH (n:`Rule`) WHERE n.`log value`='{name}'
    #                  RETURN n AS node"""

    "日志字段值 {} key为日志任意能确定此日志的属性名 value为key所对应的值"
    log_info_key = list(log_info.keys())[0]
    log_info_value = log_info.get(log_info_key)

    node_rule = NodeMatcher(graph).match('Rule').where(f"_.`log value`='{log_info_value}'").first()
    node_log = NodeMatcher(graph).match().where(f"NONE(label_1 IN LABELS(_) WHERE label_1 IN {label_list}) "
                                                f"AND _.`{log_info_key}`='{log_info_value}'").first()

    if node_rule == None:
        pass
    else:
        rule_log_relation = Relationship(node_log, 'log hit rule', node_rule,
                                         **{'create': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        graph.merge(rule_log_relation)


    # info = graph.run(query_rule).data()
    # now = datetime.date.today()
    # now_file = str(now) + '.csv'

    # for text in info:
    #     if text['node'] == None:
    #         pass
    #     else:

            # if not os.path.exists(now_file):
            #     pd.DataFrame([text['property']], index=None)\
            #         .to_csv(now_file, mode='a', index=False, index_label=False)
            # else:
            #     pd.DataFrame([text['property']], index=None)\
            #         .to_csv(now_file, mode='a', index=False, header=False, index_label=False)

def log_hit_num(date_time: str):
    """
    实时统计威胁命中的数量
    @param date_time: 当前时刻的日期, eg: '2022-10-24 16:20:12'
    @return:
    """

    now_date = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    d1 = datetime.timedelta(days=0, hours=now_date.hour, minutes=now_date.minute, seconds=now_date.second)
    start_time = now_date - d1
    d2 = datetime.timedelta(days=0, hours=23 - now_date.hour, minutes=59 - now_date.minute, seconds=59 - now_date.second)
    end_time = now_date + d2

    query = f"""MATCH p=()-[r:`log hit rule`]->() WHERE '{start_time}'< r.create<= '{end_time}' RETURN COUNT(r) AS count"""
    info = graph.run(query).data()
    info_list = []
    for text in info:
        info_list.append(text['count'])

    info_list.insert(0, str(now_date.date()))
    return info_list


def log_hit_info(iDisplayStart, iDisplayLength):
    """
    展现威胁命中数据信息 以及分页信息
    @param iDisplayStart: 分页开始数
    @param iDisplayLength: 分页数据长度
    @return:
    """
    query = f"""MATCH (log)-[r:`log hit rule`]->(rule:`Rule`)-[r2]->(tech) 
                RETURN DISTINCT log, rule, TYPE(r2) AS r2 SKIP {iDisplayStart} LIMIT {iDisplayLength}"""
    query_num = f"""MATCH (log)-[r:`log hit rule`]->(rule:`Rule`)-[r2]->(tech) 
                RETURN COUNT(DISTINCT log) AS count"""
    info = graph.run(query).data()
    info_num = graph.run(query_num).data()

    info_list = []
    info_number = []

    for text in info:
        every_text = {}
        every_text.update(dict(text['log']))
        every_text.update({'attack model': text['r2']})
        info_list.append(every_text)
    for text in info_num:
        info_number.append(text['count'])

    return info_list, sum(info_number)

def log_hit_search(node_properties: dict, iDisplayStart: int, iDisplayLength: int):
    """
    通过条件查询威胁命中数据
    @param node_properties: 节点属性 eg:{"log value": "c3f70729-6c65-4874-b521-f9d8d2220866", 'type': 'http', 'attack model': 'test'}
    @param iDisplayStart: 分页开始数
    @param iDisplayLength: 分页数据长度
    @return:
    """

    query_start = f"""MATCH (log)-[r]->(rule:`Rule`)-[r2]->(tech) WHERE TYPE(r)='log hit rule'"""
    query_end = f"""RETURN DISTINCT log, rule, TYPE(r2) AS r2 SKIP {iDisplayStart} LIMIT {iDisplayLength}"""
    query_end_num = f"""RETURN COUNT(DISTINCT log) AS count"""

    if node_properties.get('type'):
        log_type = f"""AND log.type="{node_properties.get('type')}" """
        query_start = query_start + log_type
    if node_properties.get('log value'):
        log_value = f"""AND rule.`log value`="{node_properties.get('log value')}" """
        query_start = query_start + log_value
    if node_properties.get('attack model'):
        log_model = f"""AND rule.`attack model`="{node_properties.get('attack model')}" """
        query_start = query_start + log_model

    query = query_start + query_end
    query_num = query_start + query_end_num
    info = graph.run(query).data()
    info_num = graph.run(query_num).data()

    info_list = []
    info_number = []

    if info == []:
        return [], 0
    else:
        for text in info:
            every_text = {}
            every_text.update(dict(text['log']))
            every_text.update({'attack model': text['r2']})
            info_list.append(every_text)
        # info_list.append(dict(info[0]['log']))
        # info_list.append(dict(info[2])['r2'])
        for text in info_num:
            info_number.append(text['count'])

        return info_list, sum(info_number)


if __name__ == '__main__':
    label_list = ['SubTechniques', 'Techniques', 'Tactics', 'Citations', 'Datasource',
                  'DatasourceComponent', 'Software', 'Groups', 'Mitigations']
    # log_info = {'name': 'c3f70729-6c65-4874-b521-f9d8d2220866'}
    # log_info = {'name': 'a7f25335-1cfe-4a2d-b74a-fc9954b127a6'}
    # threaten_hit_rule(log_info, label_list)
    #
    # log_hit_num('2022-10-24 16:20:12')

    # print(log_hit_info(0, 15))

    # log_hit_search({"log value": "c3f70729-6c65-4874-b521-f9d8d2220866", "techniques id": "T1111"})
    # log_hit_search({"log value": "c3f70729-6c65-4874-b521-f9d8d2220866", 'type': 'http', 'attack model': 'test'}, 0, 15)
    # log_hit_search({"log value": "c3f70729-6c65-4874-b521-f9d8d2220867"}, 0, 15)
    print(log_hit_search({'type': 'http'}, 0, 15))
    # log_hit_search({'attack model': 'test'}, 0, 15)
    # log_hit_search({'type': 'http'}, 0, 15)
    # log_hit_search({'name': 'a7f25335-1cfe-4a2d-b74a-fc9954b127a6'})
    # log_hit_search({'time': 2022})


"""
MATCH (g)-[]-(t)-[r]-(ll) 
WHERE NONE(l IN LABELS(ll) WHERE l IN ['SubTechniques', 'Techniques', 'Tactics', 'Citations', 'Datasource', 'DatasourceComponent', 'Software', 'Groups', 'Mitigations']) 
AND ll.`log value`='c3f70729-6c65-4874-b521-f9d8d2220866' 
AND any(label in labels(g) where label in ['Groups', 'Software']) 
return g
"""
'T1111'
'Multi-Factor Authentication Interception'











