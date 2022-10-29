# -*- coding: UTF-8 -*-
from py2neo import Graph, Node, Relationship, NodeMatcher
from .timestamp import random_str
from . import dataanalysis
from . import relu_attck_relevancy

'''
The alarm log 
wazuhr告警日志关联attck
'''

# neo4j_profile = 'http://localhost:7474'
# user_name = 'neo4j'
# user_password = '123456'


class Wazhur_Log:
    '''
    初始打开图谱
    '''
    def __init__(self, neo4j_profile, user_name, user_password):
        self.graph = Graph(neo4j_profile,auth=(user_name, user_password))
        self.matcher = NodeMatcher(self.graph)
        self.dmdataanalysis = dataanalysis.Data_Processing(neo4j_profile, user_name, user_password)
        self.dmrelu_attck_relevancy = relu_attck_relevancy.Rule_Attck_Log_Relevancy(neo4j_profile, user_name, user_password)

    def Nercreate(self, js):
        '''
        做attck匹配创建节点关系保存在图库里面
        :param js:
        :return:
        '''
        values_kt = {}
        timestamp = random_str()
        for k, v in js.items():
            key_value_map = self.dmdataanalysis.recursion_map_value(v, k)
            values_kt.update(key_value_map)

        N1 = Node('Wazuhr_Log', name=str(timestamp), **values_kt)
        self.graph.create(N1)

        agent = self.dmdataanalysis.replace(values_kt['agent__id'])
        N2 = Node('agentid', name=agent)
        nodelist = list(self.matcher.match("agentid", name=agent))
        if len(nodelist) > 0:
            N2 = nodelist[0]
            Tem = self.matcher.match('agentid').where("_.name=~'" + agent + "'").first()
            if Tem != None:
                relation1 = Relationship(Tem, 'Logcluster', N1)
                self.graph.create(relation1)
        else:
            self.graph.create(N2)
        Tem = self.matcher.match('agentid').where("_.name=~'" + agent + "'").first()
        if Tem != None:
            relation1 = Relationship(Tem, 'Logcluster', N1)
            self.graph.create(relation1)

        self.dmrelu_attck_relevancy.Attck_Rule_Log_Relevancy(N1, values_kt)


        # for value in values_kt.values():
        #     valuestr = self.dmdataanalysis.replace(str(value))
        #
        #     Tempnode1 = self.matcher.match('战术').where("_.名字=~'" + valuestr + "'").first()
        #     Tem1 = self.matcher.match('战术').where("_.ID=~'" + valuestr + "'").first()
        #
        #     if Tem1 != None:
        #         print("Tem1战术", Tem1)
        #         relation1 = Relationship(N1, 'Log_attck_tactics_ID', Tem1)
        #         self.graph.create(relation1)
        #     if Tempnode1 != None:
        #         print("Tempnode1战术", Tempnode1)
        #         relation1 = Relationship(N1, 'Log_attck_tactics', Tempnode1)
        #         self.graph.create(relation1)
        #
        #     Tempnode2 = self.matcher.match('技术').where("_.名字=~'" + valuestr + "'").first()
        #     Tem2 = self.matcher.match('技术').where("_.ID=~'" + valuestr + "'").first()
        #
        #     if Tem2 != None:
        #         print("Tem2技术", Tem2)
        #         relation2 = Relationship(N1, 'Log_attck_technology_father_ID', Tem2)
        #         self.graph.create(relation2)
        #     if Tempnode2 != None:
        #         print("Tempnode2技术", Tempnode2)
        #         relation2 = Relationship(N1, 'Log_attck_technology_father', Tempnode2)
        #         self.graph.create(relation2)
        #
        #     Tempnode3 = self.matcher.match('子技术').where("_.名字=~'" + valuestr + "'").first()
        #     Tem3 = self.matcher.match('子技术').where("_.ID=~'" + valuestr + "'").first()
        #
        #     if Tem3 != None:
        #         print("Tem3子技术", Tem3)
        #         relation3 = Relationship(N1, 'Log_attck_technology_son_ID', Tem3)
        #         self.graph.create(relation3)
        #     if Tempnode3 != None:
        #         print("Tempnode3子技术", Tempnode3)
        #         relation3 = Relationship(N1, 'Log_attck_technology_son', Tempnode3)
        #         self.graph.create(relation3)

    # def agent_data(self, js):
    #     values_kt, values_attck = self.dmdataanalysis.analyze(js)
    #     agent = values_kt['agent__id']
    #     N2 = Node('agent_id', name=agent)
    #     nodelist = list(self.matcher.match("agent_id", name=agent))
    #     if len(nodelist) > 0:
    #         N2 = nodelist[0]
    #     else:
    #         self.graph.create(N2)

    # values_kt = self.dmdataanalysis.Analyze(js)

    # agent_id = self.dmdataanalysis.agent_data()
    # for agent in agent_id:
    #     N2 = Node('agent_id', name=agent)
    #     Tempnode1 = self.matcher.match('Log_notes').where("_.agent__id=~'" + agent + "'").first()
    #     nodelist = list(self.matcher.match("agent_id", name=agent))
    #     if len(nodelist) > 0:
    #         N2 = nodelist[0]
    #         relation1 = Relationship(N2, 'Logcluster', Tempnode1)
    #         self.graph.create(relation1)
    #         Tempnode1 = self.matcher.match('Log_notes').where("_.agent__id=~'" + agent + "'").first()
    #         relation1 = Relationship(N2, 'Logcluster', Tempnode1)
    #         self.graph.create(relation1)
    #     else:
    #         self.graph.create(N2)
    #         relation1 = Relationship(N2, 'Logcluster', Tempnode1)
    #         self.graph.create(relation1)
    #         Tempnode1 = self.matcher.match('Log_notes').where("_.agent__id=~'" + agent + "'").first()
    #         relation1 = Relationship(N2, 'Logcluster', Tempnode1)
    #         self.graph.create(relation1)
    #     Tempnode1 = self.matcher.match('Log_notes').where("_.agent__id=~'" + agent + "'").first()
    #     relation1 = Relationship(N2, 'Logcluster', Tempnode1)
    #     self.graph.create(relation1)
    # Tempnode1 = self.matcher.match('Log_notes').where("_.agent__id=~'" + agent + "'").first()
    # Tem = self.matcher.match('agent_id').where("_.name=~'" + agent + "'").first()
    # relation1 = Relationship(Tem, 'Logcluster', Tempnode1)
    # self.graph.create(relation1)

    # attck_dict = self.dmdataanalysis.Cread_Dict(js)

# if __name__ == '__main__':
#     neo4j_profile = 'http://localhost:7474'
#     user_name = 'neo4j'
#     user_password = '123456'
#     dm = Wazhur_Log(neo4j_profile, user_name, user_password)