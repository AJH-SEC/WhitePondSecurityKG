# -*- coding: UTF-8 -*-
from py2neo import Graph, NodeMatcher
from .classguize import rule_consciousness, Calling_conventions

'''
数据所有的解析方法和数据转格式转
'''

class Data_Processing:
    def __init__(self, neo4j_profile, user_name, user_password):
        self.graph = Graph(neo4j_profile,auth=(user_name, user_password))
        self.matcher = NodeMatcher(self.graph)

    def recursion_map_value(self, map_value, pre_key):
        key_value_map = {}
        if type(map_value) == dict:
            for key, value in map_value.items():
                key = pre_key + "__" + key
                if type(value) == type(dict()):
                    dat_emp =self.recursion_map_value(value, key)
                    key_value_map.update(dat_emp)
                elif type(value) == type([]):
                    key_value_map[key] = ",".join([i for i in value])
                else:
                    key_value_map[key] = value
        else:
            key = {pre_key: map_value}
            key_value_map.update(key)
        return key_value_map

    def The_rules_call(self, path):
        '''
        调用规则文件
        :param path:
        :return:
        '''
        rule = Calling_conventions(path)
        category, rulematch, ruletechnologyid, rulegroup, ruledescription, ruleregex, \
        rulerulelevel, ruleruleid, ruleif_sid, ruleoptions, ruleif_matched_sid, ruleignore, \
        rulecheck_if_ignored, ruleurl, ruleinfo, rulefield = rule.rule_universal_all()

        return category, rulematch, ruletechnologyid, rulegroup, ruledescription, ruleregex, rulerulelevel, ruleruleid, \
               ruleif_sid, ruleoptions, ruleif_matched_sid, ruleignore, rulecheck_if_ignored, ruleurl, ruleinfo, rulefield

    def The_son_technology(self):
        '''
        从数据库中获取子技术信息
        :return:
        '''
        FatherID = []
        sonname = []
        sonID = []
        c = self.graph.run('Match (n:子技术) return properties(n) AS properties,ID(n) as id, labels(n) AS label').data()
        for c1 in c:
            if type(c1) == dict:
                for k, v in c1.items():
                    if type(v) == dict:
                        Father_ID = v['父技术ID']
                        son_name = v['名字']
                        son_ID = v['ID']
                        FatherID.append(Father_ID)
                        sonname.append(son_name)
                        sonID.append(son_ID)
        return FatherID, sonname, sonID

    def Father_technology(self):
        '''
        从数据库中获取技术的信息
        :return:
        '''
        FatherID = []
        Fathertechnology = []
        sonID = []
        b = self.graph.run('Match (n:技术) return properties(n) AS properties,ID(n) as id, labels(n) AS label').data()
        for b1 in b:
            if type(b1) == dict:
                for k, v in b1.items():
                    if type(v) == dict:
                        technique_ID = v['ID']
                        technique_name = v['名字']
                        technique_son = v['子技术']
                        FatherID.append(technique_ID)
                        Fathertechnology.append(technique_name)
                        sonID.append(technique_son)
        return FatherID, Fathertechnology, sonID

    def Tactics_Technology(self):
        '''
        从数据库中获取战术信息
        :return:
        '''
        tactics_id = []
        tactics_name = []
        tactics_brief = []

        c = self.graph.run('Match (n:战术) return properties(n) AS properties,ID(n) as id, labels(n) AS label').data()
        for cc in c:
            if type(cc) == dict:
                for k, v in cc.items():
                    if type(v) == dict:
                        id = v['ID']
                        name = v['名字']
                        brief = v['简介']
                        tactics_id.append(id)
                        tactics_name.append(name)
                        tactics_brief.append(brief)
        return tactics_id, tactics_name, tactics_brief

    def replace(self, string):
        '''
        字符串切分
        :param string:
        :return:
        '''
        string = string.replace('-', '_')
        return string



    # def agent_data(self):
    #     '''
    #     从数据中获取agentid信息
    #     :return:
    #     '''
    #     agent_id = []
    #     a = self.graph.run('Match (n:Ordinary_Log) return properties(n) AS properties,ID(n) as id, labels(n) AS label').data()
    #     b = self.graph.run('Match (n:Caution_Log) return properties(n) AS properties,ID(n) as id, labels(n) AS label').data()
    #     c = self.graph.run('Match (n:Wazuhr_Log) return properties(n) AS properties,ID(n) as id, labels(n) AS label').data()
    #     # c = self.graph.run('Match (n:Log_notes) return properties(n) AS properties,ID(n) as id, labels(n) AS label').data()
    #     for c1 in c:
    #         if type(c1) == dict:
    #             for k, v in c1.items():
    #                 if type(v) == dict:
    #                     agent = v['agent__id']
    #                     agent_id.append(agent)
    #     return agent_id

    # def Common(self, js):
    #     '''
    #     对json数据进行详细的解析
    #     :param js:
    #     :return:
    #     '''
    #     values_kt = {}
    #     for k, v in js.items():
    #         if type(v) != dict:
    #             kt = {str(k): str(v).replace('-', '_')}
    #             values_kt.update(kt)
    #         if type(v) == dict:
    #             for k1, v1 in v.items():
    #                 if type(v1) != dict:
    #                     ktv = {str(k) + '__' + str(k1): str(v1).replace('-', '_')}
    #                     values_kt.update(ktv)
    #                 if type(v1) == dict:
    #                     for k2, v2 in v1.items():
    #                         if type(v2) != dict and type(v2) != list:
    #                             ktvv = {str(k) + '__' + str(k1) + '__' + str(k2): str(v2).replace('-', '_')}
    #                             values_kt.update(ktvv)
    #                         if type(v2) == list:
    #                             for v2i in v2:
    #                                 ktvvi = {str(k) + '__' + str(k1) + '__' + str(k2): str(v2i).replace('-', '_')}
    #                                 values_kt.update(ktvvi)
    #     return values_kt
    # def Skill_ID(self):
    #     '''
    #     从数据库中获取匹配的规则信息
    #     :return:
    #     '''
    #     skill = []
    #     f = self.graph.run('Match (n:technology) return properties(n) AS properties,ID(n) as id, labels(n) AS label').data()
    #     for f1 in f:
    #         if type(f1) == dict:
    #             for k, v in f1.items():
    #                 if type(v) == dict:
    #                     technologyID = v['name']
    #                     # print('technology',v['name'])
    #                     skill.append(technologyID)
    #     return skill

    # def Cread_Dict_one(self, dt):  # 字典，列表区分函数
    #     values = []
    #     # 存储值列表
    #     # print('dt',dt)
    #     if type(dt) is dict:  # 判断是否是字典   condation(一层字典)
    #         for k, v in dt.items():
    #             values.append((k, v))
    #         return values
    #     elif type(dt) is list:
    #         for i in dt:
    #             values.append(i)
    #         return values
    #     else:
    #         values.append(dt)
    #         return values
    # def Cread_Dict(self,dt):  # 字典，列表区分函数
    #     value = []  # 存储值列表
    #     if type(dt) is dict:  # 判断是否是字典   condation(一层字典)
    #         for k, v in dt.items():  # 循环字典
    #             if type(v) is dict:  # 判断是否是字典套字典 （二层字典）
    #                 for k1, v1 in v.items():  # 是字典套字典进行拆除
    #                     if type(v1) is dict:  # condation(三层字典)
    #                         for k2, v2 in v1.items():
    #                             if type(v2) is dict:
    #                                 for k3, v3 in v2.items():
    #                                     value.append(str(v3))
    #                             elif type(v2) is list:
    #                                 for i4 in v2:
    #                                     value.append(str(i4))
    #                             else:
    #                                 value.append(str(v2))
    #                     elif type(v1) is list:  # condation(三层列表)
    #                         for i3 in v1:
    #                             value.append(str(i3))
    #                     else:  # not dict and list
    #                         value.append(str(v1))
    #             elif type(v) is list:  # 判断是否是字典套列表（二层列表）
    #                 for i1 in v:  # 是进行拆除
    #                     value.append(str(i1))  # *
    #             else:  # 否则直接存储列表
    #                 value.append(str(v))
    #         return value
    #     elif type(dt) is list:  # 对列表操作 condation(一层列表)
    #         for i2 in dt:  # 是进行拆除
    #             value.append(str(i2))
    #     else:  # not dict or list
    #         value.append(str(dt))
    #     value.clear()

    # def Analyze(self, js):
    #     '''
    #     对json数据进行详细的解析
    #     :param js:
    #     :return:
    #     '''
    #     values_kt = {}
    #     for k, v in js.items():
    #         if type(v) != dict:
    #             kt = {str(k): str(v).replace('-', '_')}
    #             values_kt.update(kt)
    #         if type(v) == dict:
    #             for k1, v1 in v.items():
    #                 if type(v1) != dict:
    #                     ktv = {str(k) + '__' + str(k1): str(v1).replace('-', '_')}
    #                     values_kt.update(ktv)
    #                 if type(v1) == dict:
    #                     for k2, v2 in v1.items():
    #                         if type(v2) != dict and type(v2) != list:
    #                             ktvv = {str(k) + '__' + str(k1) + '__' + str(k2): str(v2).replace('-', '_')}
    #                             values_kt.update(ktvv)
    #                         if type(v2) == list:
    #                             for v2i in v2:
    #                                 ktvvi = {str(k) + '__' + str(k1) + '__' + str(k2): str(v2i).replace('-', '_')}
    #                                 values_kt.update(ktvvi)
    #     return values_kt
# if __name__ == '__main__':
#     dirlist = r'C:\Users\01\Desktop\python_log\pyhon-log-attck\rules'
#
#     neo4j_profile = 'http://localhost:7474'
#     user_name = 'neo4j'
#     user_password = '123456'
#     dm = Data_Processing(neo4j_profile, user_name, user_password)