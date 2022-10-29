import re
from py2neo import Graph, Node, Relationship, NodeMatcher
from model.govern_attck_log import dataanalysis


class Rule_Attck_Log_Relevancy:
    def __init__(self, neo4j_profile, user_name, user_password):
        self.graph = Graph(neo4j_profile, auth=(user_name, user_password))
        self.matcher = NodeMatcher(self.graph)
        self.dmdataanalysis = dataanalysis.Data_Processing(neo4j_profile, user_name, user_password)
        # self.dmrule_relevance_attck = rule_relevance_attck.Rule_Correlation_Attck(neo4j_profile, user_name, user_password)

    def Rule_Nercreate_Attck_Log(self, N1, values_kt,  dirlist):

        category, rulematch, ruletechnologyid, rulegroup, ruledescription, ruleregex, rulerulelevel, ruleruleid, \
        ruleif_sid, ruleoptions, ruleif_matched_sid, ruleignore, rulecheck_if_ignored, ruleurl, ruleinfo, rulefield = self.dmdataanalysis.The_rules_call(dirlist)

        for value in values_kt.values():
            valuestr = self.dmdataanalysis.replace(str(value))

            for matchlist in rulematch:
                if valuestr == matchlist:
                    n2 = Node('rule_match', name=matchlist)
                    self.graph.create(n2)
                    rule1 = Relationship(N1, 'match规则匹配', n2)
                    self.graph.create(rule1)

            for descriptionlist in ruledescription:
                if descriptionlist == valuestr:
                    n3 = Node('rule_description', name=descriptionlist)
                    self.graph.create(n3)
                    rule2 = Relationship(N1, 'description规则匹配', n3)
                    self.graph.create(rule2)

            for ruletechnologyidlist in ruletechnologyid:
                if ruletechnologyidlist == valuestr:
                    n4 = Node('rule_id', name=ruletechnologyidlist)
                    self.graph.create(n4)
                    rule3 = Relationship(N1, 'id规则匹配', n4)
                    self.graph.create(rule3)

            for ruleregexlist in ruleregex:
                regant = ruleregexlist.replace("'", '').replace('"', '')
                ret = re.match(regant, str(valuestr))
                if ret != None and ret.group() != '':
                    n5 = Node('rule_regex', name=ret.group())
                    self.graph.create(n5)
                    rule4 = Relationship(N1, 'regex规则匹配', n5)
                    self.graph.create(rule4)

            for rulerullist in ruleurl:
                if rulerullist == valuestr:
                    n6 = Node('rule_url', name=rulerullist)
                    self.graph.create(n6)
                    rule5 = Relationship(N1, 'rule_url规则匹配', n6)
                    self.graph.create(rule5)

    def Attck_Rule_Log_Relevancy(self, N1, values_kt):
        for value in values_kt.values():
            valuestr = self.dmdataanalysis.replace(str(value))

            Tempnode1 = self.matcher.match('战术').where("_.名字=~'" + valuestr + "'").first()
            Tem1 = self.matcher.match('战术').where("_.ID=~'" + valuestr + "'").first()

            if Tempnode1 != None:
                relation1 = Relationship(N1, 'Log_Attck_Tactics_Name', Tempnode1)
                self.graph.create(relation1)
            if Tem1 != None:
                relation1 = Relationship(N1, 'Log_Attck_Tactics_ID', Tem1)
                self.graph.create(relation1)

            Tempnode2 = self.matcher.match('技术').where("_.名字=~'" + valuestr + "'").first()
            Tem2 = self.matcher.match('技术').where("_.ID=~'" + valuestr + "'").first()

            if Tempnode2 != None:
                relation2 = Relationship(N1, 'Log_Attck_Technology_Father_Name', Tempnode2)
                self.graph.create(relation2)
            if Tem2 != None:
                relation2 = Relationship(N1, 'Log_Attck_Technology_Father_ID', Tem2)
                self.graph.create(relation2)

            Tempnode3 = self.matcher.match('子技术').where("_.名字=~'" + valuestr + "'").first()
            Tem3 = self.matcher.match('子技术').where("_.ID=~'" + valuestr + "'").first()

            if Tempnode3 != None:
                relation3 = Relationship(N1, 'Log_Attck_Technology_Son_Name', Tempnode3)
                self.graph.create(relation3)
            if Tem3 != None:
                relation3 = Relationship(N1, 'Log_Attck_Technology_Son_ID', Tem3)
                self.graph.create(relation3)
    def Rule_Relevancy_Attck(self, N1, values_kt):
        for value in values_kt.values():
            valuestr = self.dmdataanalysis.replace(str(value))

            Tempnode1 = self.matcher.match('战术').where("_.名字=~'" + valuestr + "'").first()
            Tem1 = self.matcher.match('战术').where("_.ID=~'" + valuestr + "'").first()

            Tempnode2 = self.matcher.match('技术').where("_.名字=~'" + valuestr + "'").first()
            Tem2 = self.matcher.match('技术').where("_.ID=~'" + valuestr + "'").first()

            Tempnode3 = self.matcher.match('子技术').where("_.名字=~'" + valuestr + "'").first()
            Tem3 = self.matcher.match('子技术').where("_.ID=~'" + valuestr + "'").first()

            Trule_match = self.matcher.match('rule_match').where("_.name=~'" + valuestr + "'").first()
            Trule_description = self.matcher.match('rule_description').where("_.name=~'" + valuestr + "'").first()
            Trule_id = self.matcher.match('rule_id').where("_.name=~'" + valuestr + "'").first()
            Trule_regex = self.matcher.match('relu_regex').where("_.name=~'" + valuestr + "'").first()
            Trule_url = self.matcher.match('rule_url').where("_.name=~'" + valuestr + "'").first()

            if Tempnode1 != None and Trule_match != None:
                relation1 = Relationship(Trule_match, 'Rule_Relevancy_Attck_Name', Tempnode1)
                self.graph.create(relation1)
            elif Tempnode2 != None and Trule_match != None:
                relation2 = Relationship(Trule_match, 'Rule_Relevancy_Attck_Name', Tempnode2)
                self.graph.create(relation2)
            elif Tempnode3 != None and Trule_match != None:
                relation3 = Relationship(Trule_match, 'Rule_Relevancy_Attck_Name', Tempnode3)
                self.graph.create(relation3)

            if Tempnode1 != None and Trule_description != None:
                relation1 = Relationship(Trule_description, 'Rule_Relevancy_Attck_Name', Tempnode1)
                self.graph.create(relation1)
            elif Tempnode2 != None and Trule_description != None:
                relation2 = Relationship(Trule_description, 'Rule_Relevancy_Attck_Name', Tempnode2)
                self.graph.create(relation2)
            elif Tempnode3 != None and Trule_description != None:
                relation3 = Relationship(Trule_description, 'Rule_Relevancy_Attck_Name', Tempnode3)
                self.graph.create(relation3)

            if Tempnode1 != None and Trule_id != None:
                relation1 = Relationship(Trule_id, 'Rule_Relevancy_Attck_Name', Tempnode1)
                self.graph.create(relation1)
            elif Tempnode2 != None and Trule_id != None:
                relation2 = Relationship(Trule_id, 'Rule_Relevancy_Attck_Name', Tempnode2)
                self.graph.create(relation2)
            elif Tempnode3 != None and Trule_id != None:
                relation3 = Relationship(Trule_id, 'Rule_Relevancy_Attck_Name', Tempnode3)
                self.graph.create(relation3)

            if Tempnode1 != None and Trule_regex != None:
                relation1 = Relationship(Trule_regex, 'Rule_Relevancy_Attck_Name', Tempnode1)
                self.graph.create(relation1)
            elif Tempnode2 != None and Trule_regex != None:
                relation2 = Relationship(Trule_regex, 'Rule_Relevancy_Attck_Name', Tempnode2)
                self.graph.create(relation2)
            elif Tempnode3 != None and Trule_regex != None:
                relation3 = Relationship(Trule_regex, 'Rule_Relevancy_Attck_Name', Tempnode3)
                self.graph.create(relation3)

            if Tempnode1 != None and Trule_url != None:
                relation1 = Relationship(Trule_url, 'Rule_Relevancy_Attck_Name', Tempnode1)
                self.graph.create(relation1)
            elif Tempnode2 != None and Trule_url != None:
                relation2 = Relationship(Trule_url, 'Rule_Relevancy_Attck_Name', Tempnode2)
                self.graph.create(relation2)
            elif Tempnode3 != None and Trule_url != None:
                relation3 = Relationship(Trule_url, 'Rule_Relevancy_Attck_Name', Tempnode3)
                self.graph.create(relation3)

            if Tem1 != None and Trule_match != None:
                relation1 = Relationship(Trule_match, 'Rule_Relevancy_Attck_ID', Tem1)
                self.graph.create(relation1)
            elif Tem2 != None and Trule_match != None:
                relation2 = Relationship(Trule_match, 'Rule_Relevancy_Attck_ID', Tem2)
                self.graph.create(relation2)
            elif Tem3 != None and Trule_match != None:
                relation3 = Relationship(Trule_match, 'Rule_Relevancy_Attck_ID', Tem3)
                self.graph.create(relation3)

            if Tem1 != None and Trule_description != None:
                relation1 = Relationship(Trule_description, 'Rule_Relevancy_Attck_ID', Tem1)
                self.graph.create(relation1)
            elif Tem2 != None and Trule_description != None:
                relation2 = Relationship(Trule_description, 'Rule_Relevancy_Attck_ID', Tem2)
                self.graph.create(relation2)
            elif Tem3 != None and Trule_description != None:
                relation3 = Relationship(Trule_description, 'Rule_Relevancy_Attck_ID', Tem3)
                self.graph.create(relation3)

            if Tem1 != None and Trule_id != None:
                relation1 = Relationship(Trule_id, 'Rule_Relevancy_Attck_ID', Tem1)
                self.graph.create(relation1)
            elif Tem2 != None and Trule_id != None:
                relation2 = Relationship(Trule_id, 'Rule_Relevancy_Attck_ID', Tem2)
                self.graph.create(relation2)
            elif Tem3 != None and Trule_id != None:
                relation3 = Relationship(Trule_id, 'Rule_Relevancy_Attck_ID', Tem3)
                self.graph.create(relation3)

            if Tem1 != None and Trule_regex != None:
                relation1 = Relationship(Trule_regex, 'Rule_Relevancy_Attck_ID', Tem1)
                self.graph.create(relation1)
            elif Tem2 != None and Trule_regex != None:
                relation2 = Relationship(Trule_regex, 'Rule_Relevancy_Attck_ID', Tem2)
                self.graph.create(relation2)
            elif Tem3 != None and Trule_regex != None:
                relation3 = Relationship(Trule_regex, 'Rule_Relevancy_Attck_ID', Tem3)
                self.graph.create(relation3)

            if Tem1 != None and Trule_url != None:
                relation1 = Relationship(Trule_url, 'Rule_Relevancy_Attck_ID', Tem1)
                self.graph.create(relation1)
            elif Tem2 != None and Trule_url != None:
                relation2 = Relationship(Trule_url, 'Rule_Relevancy_Attck_ID', Tem2)
                self.graph.create(relation2)
            elif Tem3 != None and Trule_url != None:
                relation3 = Relationship(Trule_url, 'Rule_Relevancy_Attck_ID', Tem3)
                self.graph.create(relation3)