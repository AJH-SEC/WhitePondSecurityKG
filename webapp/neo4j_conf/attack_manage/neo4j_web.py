# -*-coding:utf-8-*-
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, Subgraph
from django.conf import settings
from json import dumps, dump

graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

def createNode(node_label, node_properties):
    """
    增加节点，同时进行判断数据库中是否有此数据
    @param node_label: 节点标签
    @param node_properties: 节点属性
    @return: 判断是否增加节点。有，返回“此节点已存在”；无，增加节点
    """
    result = NodeMatcher(graph).match(node_label).where(**node_properties).exists()
    if result == False:
        node = Node(node_label, **node_properties)
        graph.create(node)
    else:
        # node = NodeMatcher(graph).match(node_label).where(**node_properties).all()
        return "此节点已经存在"


def createRelationships(node1_label, node1,
                        node2_label, node2,
                        relation_type, relation_properties=None,
                        relation_direction=True):
    """
    关系管理，建立关系，判断节点信息是否在当前数据库中
    @param node1_label: 节点1的标签
    @param node1: 节点1的信息【名字/ID】
    @param node2_label: 节点2的标签
    @param node2: 节点2的信息【名字/ID】
    @param relation_type: 两节点要创建的关系类型
    @param relation_properties: 关系属性，默认不添加关系属性
    @param relation_direction: 关系方向，默认为True:（）->（），False:（）<-（）
    @return:
    """
    matcher = NodeMatcher(graph)
    node1_info = matcher.match(node1_label).where(**node1).first()
    node2_info = matcher.match(node2_label).where(**node2).first()

    if node1_info != None and node2_info != None:
        if relation_direction == True:
            relationship = Relationship(node1_info, relation_type, node2_info)
        if relation_direction == False:
            relationship = Relationship(node2_info, relation_type, node1_info)

        if relation_properties == None:
            # graph.create(relationship)
            pass
        if relation_properties != None:
            for info in relation_properties:
                relationship.setdefault(key=info, default=relation_properties[info])
        return graph.create(relationship)


    # if node1_info == None or node2_info == None:
    #     # print("请检查当前节点是否存在")
    #     return "请检查当前节点信息是否正确输入，若没有节点信息，请先创建节点"


def deleteNode(node_label, node_name):
    """
    删除节点以及这个节点的关系
    @param node_label: 节点标签
    @param node_name: 节点名字/ID
    @return:
    """
    # return graph.run(f"MATCH (n:`{node_label}`) WHERE n.name='{node_name}' DETACH DELETE n")
    info = NodeMatcher(graph).match(node_label).where(**node_name).first()
    graph.delete(info)


def deleteRelationships(node1_label, node1, node2_label, node2, relation_type):
    """
    关系管理，删除两个节点之间的关系
    @param node1_label: 节点1的标签
    @param node1: 节点1的信息【名字/ID】
    @param node2_label: 节点2的标签
    @param node2: 节点2的信息【名字/ID】
    @param relation_type: 关系类型
    @return:
    """
    start_node = NodeMatcher(graph).match(node1_label).where(**node1).first()
    end_node = NodeMatcher(graph).match(node2_label).where(**node2).first()

    result = RelationshipMatcher(graph).match({start_node, end_node}, r_type=relation_type).all()
    for r_info in result:
        if r_info.start_node == start_node and r_info.end_node == end_node:
            graph.separate(r_info)


def modifyNode(node_label, node_info, modify_info):
    """
    修改节点信息
    @param node_label: 节点标签
    @param node_info: 节点信息【ID/name】
    @param modify_info: 要修改的的具体信息
    """
    node = NodeMatcher(graph).match(node_label).where(**node_info).first()
    node.update(**modify_info)
    graph.push(node)


def modifyRelationship(start_label: str, node1: dict,
                       end_label: str, node2: dict,
                       rel: str, new_rel: str):
    """
    修改关系，修改关系或者目标节点
    @param start_label: 源节点的label
    @param node1: 源节点信息【ID/NAME】
    @param end_label: 目标节点的label
    @param node2: 目标节点信息【ID/NAME】
    @param rel: 原有关系type
    @param new_rel: 新关系type
    @return:
    """
    # 为了前端页面统一展示，故将Citations中的citation表头设为name，在信息查找时需要将其改回来
    if start_label == 'Citations':
        node1['citation'] = node1.pop('name')
    if end_label == 'Citations':
        node2['citation'] = node2.pop('name')

    start_node = NodeMatcher(graph).match(start_label).where(**node1).first()
    end_node = NodeMatcher(graph).match(end_label).where(**node2).first()

    key_list, value_list = [], []
    for node in [node1, node2]:
        for i, (n_k, n_v) in enumerate(node.items(), start=1):
            key_list.append(n_k)
            value_list.append(n_v)


    label_list = ['SubTechniques', 'Techniques', 'DatasourceComponent', 'Citations']
    # 在关系查询时，展现的是当前节点的所有关系，
    # 但是在修改关系时需要确定关系方向，
    # ()<-[]-()
    if start_label in label_list:
        # ()-[]->()
        if end_label == 'Citations':
            # 关系属性查找，以便在修改关系类型（type）的时候，旧关系类型的属性继承到新关系类型
            query_1 = f"MATCH (n:{start_label}" + "{" + f"{''.join(key_list[0])}" + f":'{value_list[0]}'" + "}" + \
                      f")-[r:`{rel}`]->" \
                      f"(m: {end_label}" + "{" + f"{''.join(key_list[1])}" + f":'{value_list[1]}'" + "}) " \
                       "RETURN properties(r)"
            rel_pro_info = graph.run(query_1).data()
            rel_pro_old = [i for i in rel_pro_info[0].values()]

            # 关系修改
            query_2 = f"MATCH (n:{start_label}" + "{" + f"{''.join(key_list[0])}" + f":'{value_list[0]}'" + "}" + \
                      f")-[r:`{rel}`]->" \
                      f"(m: {end_label}" + "{" + f"{''.join(key_list[1])}" + f":'{value_list[1]}'" + "}) " + \
                      f"CREATE (n)-[r2:{new_rel}]->(m) SET r2 = r WITH r DELETE r"
            graph.run(query_2)

            # 新关系（type）属性的继承
            rel_pro_new = Relationship(start_node, new_rel, end_node, **rel_pro_old[0])
            graph.push(rel_pro_new)
        else:
            # 关系属性查找，以便在修改关系类型（type）的时候，旧关系类型的属性继承到新关系类型
            query_1 = f"MATCH (n:{start_label}" + "{" + f"{''.join(key_list[0])}" + f":'{value_list[0]}'" + "}" + \
                      f")<-[r:`{rel}`]-" \
                      f"(m: {end_label}" + "{" + f"{''.join(key_list[1])}" + f":'{value_list[1]}'" + "}) " \
                       "RETURN properties(r)"
            rel_pro_info = graph.run(query_1).data()
            rel_pro_old = [i for i in rel_pro_info[0].values()]

            query_2 = f"MATCH (n:{start_label}" + "{" + f"{''.join(key_list[0])}" + f":'{value_list[0]}'" + "}" + \
                      f")<-[r:`{rel}`]-" \
                      f"(m: {end_label}" + "{" + f"{''.join(key_list[1])}" + f":'{value_list[1]}'" + "}) " + \
                      f"CREATE (n)<-[r2:{new_rel}]-(m) SET r2 = r WITH r DELETE r"
            graph.run(query_2)

            # 新关系（type）属性的继承
            rel_pro_new = Relationship(end_node, new_rel, start_node, **rel_pro_old[0])
            graph.push(rel_pro_new)
    # ()-[]->()
    if end_label in label_list:
        # 关系属性查找，以便在修改关系类型（type）的时候，旧关系类型的属性继承到新关系类型
        query_1 = f"MATCH (n:{start_label}" + "{" + f"{''.join(key_list[0])}" + f":'{value_list[0]}'" + "}" + \
                  f")<-[r:`{rel}`]-" \
                  f"(m: {end_label}" + "{" + f"{''.join(key_list[1])}" + f":'{value_list[1]}'" + "}) " \
                   "RETURN properties(r)"
        rel_pro_info = graph.run(query_1).data()
        rel_pro_old = [i for i in rel_pro_info[0].values()]

        query_2 = f"MATCH (n:{start_label}" + "{" + f"{''.join(key_list[0])}" + f":'{value_list[0]}'" + "}" + \
                  f")-[r:`{rel}`]->" \
                  f"(m: {end_label}" + "{" + f"{''.join(key_list[1])}" + f":'{value_list[1]}'" + "}) " + \
                  f"CREATE (n)-[r2:`{new_rel}`]->(m) SET r2 = r WITH r DELETE r"
        graph.run(query_2)

        # 新关系（type）属性的继承
        rel_pro_new = Relationship(end_node, new_rel, start_node, **rel_pro_old[0])
        graph.push(rel_pro_new)



def searchNode(node_label, only_show=False):
    """
    查询某个标签下的所有节点名字【信息】
    @param node_label: 节点标签
    @param only_show: 是否节点信息只显示名字，默认为False：显示全部信息
    @return: 节点信息/名字
    """
    info = NodeMatcher(graph).match(node_label).all()
    info_list = []
    for text in info:
        if only_show == True:
            if node_label == 'Citations':
                info_list.append(dict(text)['citation'])
            else:
                info_list.append(dict(text)['name'])
        else:
            info_list.append(dict(text))
    return info_list
    # return dumps(info_list, ensure_ascii=False, indent=4)


def showNode(only_show=False):
    """
    对各类标签以及标签下的数据数量进行显示
    @param only_show: 是否只显示标签，默认为False:显示标签及其数量，True:只显示标签
    @return:
    """
    matcher = NodeMatcher(graph)
    query = "MATCH (n) RETURN DISTINCT(LABELS(n)) as label"

    info_all = graph.run(query).data()
    labels_set = {}
    labels_list = []
    if only_show == False:
        for info in info_all:
            label = "".join(info['label'])
            if label == 'Citations':
                pass
            else:
                labels_set.update({label: matcher.match(label).count()})
        all_node = matcher.match().count()
        labels_set.update({'overview': all_node})
        return labels_set
        # return dumps(labels_set, ensure_ascii=False, indent=4)
    if only_show == True:
        for info in info_all:
            label = "".join(info['label'])
            if label == 'Citations':
                pass
            else:
                labels_list.append(label)
        return labels_list


def showRelationships(node_label):
    """
    关系管理，显示关系
    @param node_label: 节点标签
    @return: 某个标签下的数据节点关系
    """
    query = f"MATCH p=(:`{node_label}`)-[]-() RETURN p"
    info = graph.run(query).data()

    info_all = []
    for text in info:
        start_set = {}
        end_set = {}
        info_set = {}
        for tk, tv in text.items():
            start_label = str(tv.start_node.labels).split(':')[1]
            start_message = dict(tv.start_node)

            end_label = str(tv.end_node.labels).split(':')[1]
            end_message = dict(tv.end_node)

            if start_label == 'Citations' or start_label == 'DatasourceComponent':
                """由于Citations数据里没有ID 故将reference设为ID，将citation设为name"""
                if start_label == 'Citations':
                    start_set.update({'label': start_label, 'ID': start_message['reference'],
                                      'name': start_message['citation']})

                """由于DatasourceComponent数据里没有ID，故将ID设为空值"""
                if start_label == 'DatasourceComponent':
                    start_set.update({'label': start_label, 'ID': '',
                                      'name': start_message['name']})
                end_set.update({'label': end_label, 'ID': end_message['ID'], 'name': end_message['name']})

            else:
                start_set.update({'label': start_label, 'ID': start_message['ID'],
                                  'name': start_message['name']})

                if end_label == 'DatasourceComponent' or end_label == 'Citations':
                    """由于DatasourceComponent数据里没有ID，故将ID设为空值"""
                    if end_label == 'DatasourceComponent':
                        end_set.update({'label': end_label, 'ID': '',
                                        'name': end_message['name']})

                    """由于Citations数据里没有ID 故将reference设为ID，将citation设为name"""
                    if end_label == 'Citations':
                        end_set.update({'label': end_label, 'ID': end_message['reference'],
                                        'name': end_message['citation']})
                else:
                    end_set.update({'label': end_label, 'ID': end_message['ID'],
                                    'name': end_message['name']})

            info_set.update({'start_node label': start_set['label'],
                             'start_node id': start_set['ID'],
                             'start_node name': start_set['name'],
                             'relationship': "".join(list(tv.types())),
                             'end_node label': end_set['label'],
                             'end_node id': end_set['ID'],
                             'end_node name': end_set['name']
                             })

        info_all.append(info_set)
    return info_all
    # return dumps(info_all, ensure_ascii=False, indent=4)


if __name__ == '__main__':
#     node_label = 'Person'
#     a_property = {'name': '张三', 'live_house': '北京', 'age': 39, 'hobby': ['dance', 'sing']}
#     b_property = {'name': '李四', 'live_house': '北京', 'age': 39, 'hobby': ['dance', 'sing']}
#     c_property = {'name': '王五', 'live_house': '北京', 'age': 39, 'hobby': ['dance', 'sing']}

    # createNode(node_label, a_property)
    # createNode(node_label, b_property)
    # createNode(node_label, c_property)
    #
    # searchNode('Techniques')
    # a = searchNode('Tactics')
    # print(a)
    # searchNodeName('Techniques')

    # deleteNode(node_label, {'name': '王五'})
    # deleteNode(node_label, {'name': '李四'})
    # deleteNode(node_label, {'name': '张三'})

    ac = searchNode('Citations', True)
    print(ac)

    # createRelationships(node_label, {'name': '王五'},
    #                     node_label, {'name': '李四'},
    #                     'likes', {'source type': '人', 'target type': 2022})
    # createRelationships(node_label, {'name': '王五'},
    #                     node_label, {'name': '李四'},
    #                     'likes', relation_direction=False)
    # a = showRelationships('Software')
    # a = showRelationships('DatasourceComponent')
    # print(a)
    # print(showNode(True))
    # modifyRelationship('DatasourceComponent', {'name': 'Active Directory Object Deletion'},
    #                    'Datasource', {'name': 'Active Directory'},
    #                    'qqq', 'yyy')

