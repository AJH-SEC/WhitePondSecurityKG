# from py2neo import Graph, Node, Relationship, NodeMatcher
# from . import dataanalysis
#
# class Rule_Correlation_Attck:
#     def __init__(self, neo4j_profile, user_name, user_password):
#         self.graph = Graph(neo4j_profile, auth=(user_name, user_password))
#         self.matcher = NodeMatcher(self.graph)
#         self.dmdataanalysis = dataanalysis.Data_Processing(neo4j_profile, user_name, user_password)
#
#     def rule_relevancy_attck(self):
#         FatherID, sonname, sonID = self.dmdataanalysis.The_son_technology()
#         FatherID, Fathertechnology, sonID = self.dmdataanalysis.Father_technology()
#         tactics_id, tactics_name, tactics_brief = self.dmdataanalysis.Tactics_Technology()
#
#         for son_name in sonname:
#             Tempnode1 = self.matcher.match('子技术').where("_.名字=~'" + son_name + "'").first()
#             Tem1 = self.matcher.match('rule_match').where("_.name=~'" + son_name + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_description').where("_.name=~'" + son_name + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_id').where("_.name=~'" + son_name + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('relu_regex').where("_.name=~'" + son_name + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_url').where("_.name=~'" + son_name + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#
#         for son_ID in sonID:
#             Tempnode1 = self.matcher.match('子技术').where("_.ID=~'" + son_ID + "'").first()
#             Tem1 = self.matcher.match('rule_match').where("_.name=~'" + son_ID + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_description').where("_.name=~'" + son_ID + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_id').where("_.name=~'" + son_ID + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('relu_regex').where("_.name=~'" + son_ID + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_url').where("_.name=~'" + son_ID + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#
#         for Father_ID in FatherID:
#             Tempnode1 = self.matcher.match('技术').where("_.名字=~'" + Father_ID + "'").first()
#             Tem1 = self.matcher.match('rule_match').where("_.name=~'" + Father_ID + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_description').where("_.name=~'" + Father_ID + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_id').where("_.name=~'" + Father_ID + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('relu_regex').where("_.name=~'" + Father_ID + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_url').where("_.name=~'" + Father_ID + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#
#         for Fathertechnology_name in Fathertechnology:
#             Tempnode1 = self.matcher.match('技术').where("_.名字=~'" + Fathertechnology_name + "'").first()
#             Tem1 = self.matcher.match('rule_match').where("_.name=~'" + Fathertechnology_name + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_description').where("_.name=~'" + Fathertechnology_name + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_id').where("_.name=~'" + Fathertechnology_name + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('relu_regex').where("_.name=~'" + Fathertechnology_name + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_url').where("_.name=~'" + Fathertechnology_name + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#
#         for tacticsid in tactics_id:
#             Tempnode1 = self.matcher.match('战术').where("_.名字=~'" + tacticsid + "'").first()
#             Tem1 = self.matcher.match('rule_match').where("_.name=~'" + tacticsid + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_description').where("_.name=~'" + tacticsid + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_id').where("_.name=~'" + tacticsid + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('relu_regex').where("_.name=~'" + tacticsid + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_url').where("_.name=~'" + tacticsid + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#
#         for tacticsname in tactics_name:
#             Tempnode1 = self.matcher.match('战术').where("_.ID=~'" + tacticsname + "'").first()
#             Tem1 = self.matcher.match('rule_match').where("_.name=~'" + tacticsname + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_description').where("_.name=~'" + tacticsname + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_id').where("_.name=~'" + tacticsname + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('relu_regex').where("_.name=~'" + tacticsname + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#             Tem1 = self.matcher.match('rule_url').where("_.name=~'" + tacticsname + "'").first()
#             if Tem1 != None:
#                 rule1 = Relationship(Tempnode1, '规则attck关联', Tem1)
#                 self.graph.create(rule1)
#
#
# if __name__ == '__main__':
#     neo4j_profile = 'http://localhost:7474'
#     user_name = 'neo4j'
#     user_password = '123456'
#     dm = Rule_Correlation_Attck(neo4j_profile, user_name, user_password)