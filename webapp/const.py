# coding: utf-8


class NodeLabel:
    """attack 标签类型"""
    TACTICS = 'Tactics'  # 战术
    TECHNIQUES = 'Techniques'  # 技术
    SUBTECHNIQUES = 'SubTechniques'  # 子技术
    MITIGATIONS = 'Mitigations'  # 缓解措施
    GROUPS = 'Groups'  # 组织
    SOFTWARE = 'Software'  # 软件
    DATASOURCE = 'Datasource'  # 数据资源
    CAMPAIGN = 'Campaign'  # 战役
    DATASOURCECOMPONENT = 'DatasourceComponent'  # 数据组件


LABEL_LIST = ['SubTechniques', 'Techniques', 'Tactics', 'Datasource', 'DatasourceComponent', 'Software', 'Groups',
                   'Mitigations', 'Citations', 'Campaign', 'NET_ASSERT', 'Rule']

ATTACK_LABEL_LIST = ['SubTechniques', 'Techniques', 'Tactics', 'Datasource', 'DatasourceComponent', 'Software', 'Groups',
                   'Mitigations', 'Citations', 'Campaign']
