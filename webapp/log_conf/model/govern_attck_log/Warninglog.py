# -*- coding: UTF-8 -*-
from py2neo import Graph, Node, Relationship, NodeMatcher
from timestamp import random_str
import dataanalysis
# from . import rule_relevance_attck
from attack.webapp.log_conf.model.govern_attck_log import relu_attck_relevancy

'''
The alarm log 
告警日志关联attck
'''
# neo4j_profile = 'http://localhost:7474'
# user_name = 'neo4j'
# user_password = '123456'


class Caution_Log:
    '''
    初始打开图谱
    '''
    def __init__(self, neo4j_profile, user_name, user_password):
        self.graph = Graph(neo4j_profile,auth=(user_name, user_password))
        self.matcher = NodeMatcher(self.graph)
        self.dmdataanalysis = dataanalysis.Data_Processing(neo4j_profile, user_name, user_password)
        # self.dmrule_relevance_attck = rule_relevance_attck.Rule_Correlation_Attck(neo4j_profile, user_name, user_password)
        self.dmrelu_attck_relevancy = relu_attck_relevancy.Rule_Attck_Log_Relevancy(neo4j_profile, user_name, user_password)

    def Nercreate(self, js, dirlist):
        values_kt = {}
        '''
        做规则匹配和attck匹配创建节点创建关系保存在图库里面
        :param js:
        :param dirlist:
        :return:
        '''
        category, rulematch, ruletechnologyid, rulegroup, ruledescription, ruleregex, rulerulelevel, ruleruleid, \
        ruleif_sid, ruleoptions, ruleif_matched_sid, ruleignore, rulecheck_if_ignored, ruleurl, ruleinfo, rulefield = self.dmdataanalysis.The_rules_call(dirlist)
        timestamp = random_str()
        for k, v in js.items():
            key_value_map = self.dmdataanalysis.recursion_map_value(v, k)
            values_kt.update(key_value_map)

        N1 = Node('Caution_Log', name=str(timestamp), **values_kt)
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

        self.dmrelu_attck_relevancy.Rule_Nercreate_Attck_Log(N1, values_kt, dirlist)
        self.dmrelu_attck_relevancy.Attck_Rule_Log_Relevancy(N1, values_kt)
        self.dmrelu_attck_relevancy.Rule_Relevancy_Attck(N1, values_kt)

        # for value in values_kt.values():
        #     valuestr = self.dmdataanalysis.replace(str(value))
        #
        #     for matchlist in rulematch:
        #         if matchlist == valuestr:
        #             n2 = Node('rule_match', name=matchlist)
        #             self.graph.create(n2)
        #             rule1 = Relationship(N1, 'match规则匹配', n2)
        #             self.graph.create(rule1)
        #
        #     for descriptionlist in ruledescription:
        #         if descriptionlist == valuestr:
        #             n3 = Node('rule_description', name=descriptionlist)
        #             self.graph.create(n3)
        #             rule2 = Relationship(N1, 'description规则匹配', n3)
        #             self.graph.create(rule2)
        #
        #     for ruletechnologyidlist in ruletechnologyid:
        #         if ruletechnologyidlist == valuestr:
        #             n4 = Node('rule_id', name=ruletechnologyidlist)
        #             self.graph.create(n4)
        #             rule3 = Relationship(N1, 'id规则匹配', n4)
        #             self.graph.create(rule3)
        #
        #     for ruleregexlist in ruleregex:
        #         regant = ruleregexlist.replace("'", '').replace('"', '')
        #         ret = re.match(regant, str(valuestr))
        #         if ret != None and ret.group() != '':
        #             n5 = Node('relu_regex', name=ret.group())
        #             self.graph.create(n5)
        #             rule4 = Relationship(N1, 'regex规则匹配', n5)
        #             self.graph.create(rule4)
        #
        #     for rulerullist in ruleurl:
        #         if rulerullist == valuestr:
        #             n6 = Node('rule_url', name=rulerullist)
        #             self.graph.create(n6)
        #             rule5 = Relationship(N1, 'rule_url规则匹配', n6)
        #             self.graph.create(rule5)
        #
        #     Tempnode1 = self.matcher.match('战术').where("_.名字=~'" + valuestr + "'").first()
        #     Tem1 = self.matcher.match('战术').where("_.ID=~'" + valuestr + "'").first()
        #     if Tem1 != None:
        #         relation1 = Relationship(N1, 'Log_attck_tactics_ID', Tem1)
        #         self.graph.create(relation1)
        #     if Tempnode1 != None:
        #         relation1 = Relationship(N1, 'Log_attck_tactics', Tempnode1)
        #         self.graph.create(relation1)
        #
        #     Tempnode2 = self.matcher.match('技术').where("_.名字=~'" + valuestr + "'").first()
        #     Tem2 = self.matcher.match('子技术').where("_.名字=~'" + valuestr + "'").first()
        #     if Tem2 != None:
        #         relation2 = Relationship(N1, 'Log_attck_technology_son', Tem2)
        #         self.graph.create(relation2)
        #     if Tempnode2 != None:
        #         relation2 = Relationship(N1, 'Log_attck_technology_father', Tempnode2)
        #         self.graph.create(relation2)
        #
        #     Tempnode3 = self.matcher.match('技术').where("_.ID=~'" + valuestr + "'").first()
        #     Tem3 = self.matcher.match('子技术').where("_.ID=~'" + valuestr + "'").first()
        #     if Tem3 != None:
        #         relation3 = Relationship(N1, 'Log_attck_technology_son_ID', Tem3)
        #         self.graph.create(relation3)
        #     if Tempnode3 != None:
        #         relation3 = Relationship(N1, 'Log_attck_technology_father_ID', Tempnode3)
        #         self.graph.create(relation3)

        # self.rule_attck = self.dmrule_relevance_attck.rule_relevancy_attck()


    # values_kt = self.dmdataanalysis.Analyze(js)
    # N1 = Node('Log_notes', name=str(timestamp), **values_kt)

    # def agent_data(self, js):
    #     values_kt, values_attck = self.dmdataanalysis.analyze(js)
    #     agent = values_kt['agent__id']
    #     N2 = Node('agent_id', name=agent)
    #     nodelist = list(self.matcher.match("agent_id", name=agent))
    #     if len(nodelist) > 0:
    #         N2 = nodelist[0]
    #     else:
    #         self.graph.create(N2)

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

    # data_dict = self.dmdataanalysis.Cread_Dict(js)
    # attck_dict = self.dmdataanalysis.Cread_Dict(js)
    # data_dict = self.dmdataanalysis.replacelist(data_dict)
    # for j in data_dict:
# if __name__ == '__main__':
#     dirlist = r'C:\Users\01\Desktop\niso_server-main (1)\rules'
#
#     neo4j_profile = 'http://localhost:7474'
#     user_name = 'neo4j'
#     user_password = '123456'
#     dm = Caution_Log(neo4j_profile, user_name, user_password)