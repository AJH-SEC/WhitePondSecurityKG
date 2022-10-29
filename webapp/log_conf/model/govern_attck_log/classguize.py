# -*- coding: UTF-8 -*-
from .getpath_data import data_path
import re

'''
循环接受初始化解析的信息
并提取其中的字段信息
'''
class rule_consciousness:
    '''
    循环接受信息
    这个其中每一个方法代表一个规则文件中的一个字段
    读取其中每一个字段并获得信息保存返回等待下一阶段的调用
    '''
    def __init__(self, path):
        self.dmdata_path = data_path(path)
        self.root_list, self.groupstr_list = self.dmdata_path.initially()

    def category(self):
        self.categorylist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookcategory = self.root.getElementsByTagName('category')
            for i in range(len(self.bookcategory)):
                self.bookcategorylist = self.bookcategory[i].firstChild.data
                self.categorylist.append(self.bookcategorylist)
        self.categorylist = set(self.categorylist)
        return self.categorylist

    def rulematch(self):
        self.matchlist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookmatch = self.root.getElementsByTagName('match')
            for i in range(len(self.bookmatch)):
                self.bookmatchlist = self.bookmatch[i].firstChild.data
                self.matchlist.append(self.bookmatchlist)
        self.matchlist = set(self.matchlist)
        return  self.matchlist

    def ruletechnologyid(self):
        self.idlist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookid = self.root.getElementsByTagName('id')
            for i in range(len(self.bookid)):
                self.bookidlist = self.bookid[i].firstChild.data
                self.ret = re.match('[A-Z][1-9]?[0-9]\S*', str(self.bookidlist))
                if self.ret != None:
                    self.bookidlistre = self.ret.group()
                    self.idlist.append(self.bookidlistre)
        self.idlist = set(self.idlist)
        return  self.idlist

    def rulegroup(self):
        self.grouplist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookgroup = self.root.getElementsByTagName('group')
            for i in range(len(self.bookgroup)):
                self.bookgrouplisty = self.bookgroup[i].firstChild.data
                self.grouplist.append(self.bookgrouplisty)
        self.grouplist = set(self.grouplist)
        return self.grouplist

    def ruledescription(self):
        self.descriptionlist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.booktdescription = self.root.getElementsByTagName('description')
            for i in range(len(self.booktdescription)):
                self.booktdescriplist = self.booktdescription[i].firstChild.data
                self.descriptionlist.append(self.booktdescriplist)
        self.descriptionlist = set(self.descriptionlist)
        return self.descriptionlist

    def ruleregex(self):
        self.regexlist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookregex = self.root.getElementsByTagName('regex')
            for i in range(len(self.bookregex)):
                self.bookregexlist = self.bookregex[i].firstChild.data
                self.regexlist.append(self.bookregexlist)
        self.regexlist = set(self.regexlist)
        return self.regexlist

    def ruleruleid(self):
        self.ruleidlist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookrule = self.root.getElementsByTagName('rule')
            for i in range(len(self.bookrule)):
                self.bookrulelist = self.bookrule[i].getAttribute('id')
                self.ruleidlist.append(self.bookrulelist)
        self.rulelist = set(self.ruleidlist)
        return self.rulelist

    def rulerulelevel(self):
        self.rulelevellist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookrule = self.root.getElementsByTagName('rule')
            for i in range(len(self.bookrule)):
                self.bookrulelist = self.bookrule[i].getAttribute('level')
                self.rulelevellist.append(self.bookrulelist)
        self.rulelist = set(self.rulelevellist)
        return self.rulelist

    def ruleif_sid(self):
        self.if_sidlist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookif_sid = self.root.getElementsByTagName('if_sid')
            for i in range(len(self.bookif_sid)):
                self.bookif_sidlist = self.bookif_sid[i].firstChild.data
                self.if_sidlist.append(self.bookif_sidlist)
        self.if_sidlist = set(self.if_sidlist)
        return self.if_sidlist

    def ruleoptions(self):
        self.optionslist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookoptions = self.root.getElementsByTagName('options')
            for i in range(len(self.bookoptions)):
                self.bookoptionslist = self.bookoptions[i].firstChild.data
                self.optionslist.append(self.bookoptionslist)
        self.optionslist = set(self.optionslist)
        return self.optionslist

    def ruleif_matched_sid(self):
        self.if_matched_sidlist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookif_matched_sid = self.root.getElementsByTagName('if_matched_sid')
            for i in range(len(self.bookif_matched_sid)):
                self.bookif_matched_sidlist = self.bookif_matched_sid[i].firstChild.data
                self.if_matched_sidlist.append(self.bookif_matched_sidlist)
        self.if_matched_sidlist = set(self.if_matched_sidlist)
        return self.if_matched_sidlist

    def ruleignore(self):
        self.ignorelist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookignore = self.root.getElementsByTagName('ignore')
            for i in range(len(self.bookignore)):
                self.bookignorelist = self.bookignore[i].firstChild.data
                self.ignorelist.append(self.bookignorelist)
        self.ignorelist = set(self.ignorelist)
        return self.ignorelist

    def rulecheck_if_ignored(self):
        self.check_if_ignoredlist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookcheck_if_ignored = self.root.getElementsByTagName('check_if_ignored')
            for i in range(len(self.bookcheck_if_ignored)):
                self.bookcheck_if_ignoredlist = self.bookcheck_if_ignored[i].firstChild.data
                self.check_if_ignoredlist.append(self.bookcheck_if_ignoredlist)
        self.check_if_ignoredlist = set(self.check_if_ignoredlist)
        return self.check_if_ignoredlist

    def ruleurl(self):
        self.urllist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookurl = self.root.getElementsByTagName('url')
            for i in range(len(self.bookurl)):
                self.bookurllist = self.bookurl[i].firstChild.data
                self.urllist.append(self.bookurllist)
        self.urllist = set(self.urllist)
        return self.urllist

    def ruleinfo(self):
        self.infolist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookinfo = self.root.getElementsByTagName('info')
            for i in range(len(self.bookinfo)):
                self.bookinfolist = self.bookinfo[i].firstChild.data
                self.infolist.append(self.bookinfolist)
        self.infolist = set(self.infolist)
        return self.infolist

    def rulefield(self):
        self.fieldlist = []
        # self.root_list, self.groupstr_list = self.data_initially()
        for self.root in self.root_list:
            self.bookfield = self.root.getElementsByTagName('field')
            for i in range(len(self.bookfield)):
                self.bookfieldlist = self.bookfield[i].firstChild.data
                self.fieldlist.append(self.bookfieldlist)
        self.fieldlist = set(self.fieldlist)
        return self.fieldlist


class Calling_conventions:
    '''
    循环接受上一阶段的规则文件中所提取的出来的字段信息在一个阶段进行调用
    调用其中的每一个方法所进行配合下一阶段的使用
    '''
    def __init__(self,path):
        self.path = path

    def rule_universal_all(self):
        '''
        全部的规则字段调用
        :return:
        '''
        self.data_rule = rule_consciousness(self.path)
        self.category_fun = self.data_rule.category()
        self.rulematch_fun = self.data_rule.rulematch()
        self.ruletechnologyid_fun = self.data_rule.ruletechnologyid()
        self.rulegroup_fun = self.data_rule.rulegroup()
        self.ruledescription_fun = self.data_rule.ruledescription()
        self.ruleregex_fun = self.data_rule.ruleregex()
        self.rulerulelevel_fun = self.data_rule.rulerulelevel()
        self.ruleruleid_fun = self.data_rule.ruleruleid()
        self.ruleif_sid_fun = self.data_rule.ruleif_sid()
        self.ruleoptions_fun = self.data_rule.ruleoptions()
        self.ruleif_matched_sid_fun = self.data_rule.ruleif_matched_sid()
        self.ruleignore_fun = self.data_rule.ruleignore()
        self.rulecheck_if_ignored_fun = self.data_rule.rulecheck_if_ignored()
        self.ruleurl_fun = self.data_rule.ruleurl()
        self.ruleinfo_fun = self.data_rule.ruleinfo()
        self.rulefield_fun = self.data_rule.rulefield()

        return self.category_fun, self.rulematch_fun, self.ruletechnologyid_fun, self.rulegroup_fun, self.ruledescription_fun, \
               self.ruleregex_fun, self.rulerulelevel_fun, self.ruleruleid_fun, self.ruleif_sid_fun, self.ruleoptions_fun, self.ruleif_matched_sid_fun, \
               self.ruleignore_fun, self.rulecheck_if_ignored_fun, self.ruleurl_fun, self.ruleinfo_fun, self.rulefield_fun

    # def rule_regulation_syslog(self):
    #     '''
    #     syslog类型的
    #     :return:
    #     '''
    #     self.data_rule = rule_consciousness(self.path)
    #     self.categorymatch = self.data_rule.rulematch()
    #     self.categoryregex = self.data_rule.ruleregex()
    #     self.catedescrip = self.data_rule.ruledescription()
    #     self.categoryif_sid = self.data_rule.ruleif_sid()
    #     self.categorygroup = self.data_rule.rulegroup()
    #     self.categoryid = self.data_rule.ruletechnologyid()
    #     self.categoryruleid = self.data_rule.ruleruleid()
    #     self.categoryrulelevel = self.data_rule.rulerulelevel()
    #
    #     return self.categorymatch, self.categoryregex, self.catedescrip, self.categoryif_sid, self.categorygroup, \
    #            self.categoryid, self.categoryruleid, self.categoryrulelevel
    #
    # def rule_regulation_firewall(self):
    #     '''
    #     firewall类型的
    #     :return:
    #     '''
    #     self.data_rule = rule_consciousness(self.path)
    #     self.categoryif_sid = self.data_rule.ruleif_sid()
    #     self.categoryoptions = self.data_rule.ruleoptions()
    #     self.catedescrip = self.data_rule.ruledescription()
    #     self.cateif_matched_sid = self.data_rule.ruleif_matched_sid()
    #     self.categoryruleid = self.data_rule.ruleruleid()
    #     self.categoryrulelevel = self.data_rule.rulerulelevel()
    #     self.categoryid = self.data_rule.ruletechnologyid()
    #     self.categorygroup = self.data_rule.rulegroup()
    #
    #     return self.categoryif_sid, self.categoryoptions, self.catedescrip, self.cateif_matched_sid, \
    #            self.categoryruleid, self.categoryrulelevel, self.categoryid, self.categorygroup
    #
    # def rule_regulation_ids(self):
    #     '''
    #     ids类型的
    #     :return:
    #     '''
    #     self.categoryif_sid = self.data_rule.ruleif_sid()
    #     self.categoryruleid = self.data_rule.ruleruleid()
    #     self.categoryrulelevel = self.data_rule.rulerulelevel()
    #     self.categoryid = self.data_rule.ruletechnologyid()
    #     self.cateignore = self.data_rule.ruleignore()
    #     self.catedescrip = self.data_rule.ruledescription()
    #     self.catecheck_if_ignored = self.data_rule.rulecheck_if_ignored()
    #     self.cateif_matched_sid = self.data_rule.ruleif_matched_sid()
    #     self.categroup = self.data_rule.rulegroup()
    #
    #     return self.categoryif_sid, self.categoryruleid, self.categoryrulelevel, self.categoryid, \
    #            self.cateignore, self.catedescrip, self.catecheck_if_ignored, self.cateif_matched_sid, self.categroup
    #
    # def rule_regulation_weblog(self):
    #     '''
    #     weblog类型的
    #     :return:
    #     '''
    #     self.categoryif_sid = self.data_rule.ruleif_sid()
    #     self.catedescrip = self.data_rule.ruledescription()
    #     self.categoryruleid = self.data_rule.ruleruleid()
    #     self.categoryrulelevel = self.data_rule.rulerulelevel()
    #     self.categoryid = self.data_rule.ruletechnologyid()
    #     self.categoryurl = self.data_rule.ruleurl()
    #     self.categroup = self.data_rule.rulegroup()
    #
    #     return self.categoryif_sid, self.catedescrip, self.categoryruleid, self.categoryrulelevel, \
    #            self.categoryid, self.categoryurl, self.categroup
    #
    # def rule_regulation_squid(self):
    #     '''
    #     squid类型
    #     :return:
    #     '''
    #     self.categoryif_sid = self.data_rule.ruleif_sid()
    #     self.catedescrip = self.data_rule.ruledescription()
    #     self.categoryruleid = self.data_rule.ruleruleid()
    #     self.categoryrulelevel = self.data_rule.rulerulelevel()
    #     self.categoryid = self.data_rule.ruletechnologyid()
    #     self.categoryinfo = self.data_rule.ruleinfo()
    #     self.categoryurl = self.data_rule.ruleurl()
    #     self.categroup = self.data_rule.rulegroup()
    #
    #     return self.categoryif_sid, self.catedescrip, self.categoryrulelevel, self.categoryruleid, \
    #            self.categoryid, self.categoryinfo, self.categoryurl, self.categroup
    #
    # def rule_regulation_windows(self):
    #     '''
    #     windows类型
    #     :return:
    #     '''
    #     self.categoryif_sid = self.data_rule.ruleif_sid()
    #     self.catedescrip = self.data_rule.ruledescription()
    #     self.categoryruleid = self.data_rule.ruleruleid()
    #     self.categoryrulelevel = self.data_rule.rulerulelevel()
    #     self.categoryid = self.data_rule.ruletechnologyid()
    #     self.categroup = self.data_rule.rulegroup()
    #     self.cateoptions = self.data_rule.ruleoptions()
    #
    #     return self.categoryif_sid, self.catedescrip, self.categoryrulelevel, self.categoryruleid, \
    #            self.categoryid, self.cateoptions, self.categroup
    #
    # def rule_regulation_ossec(self):
    #     '''
    #     ossec类型
    #     :return:
    #     '''
    #     self.categoryif_sid = self.data_rule.ruleif_sid()
    #     self.categorymatch = self.data_rule.rulematch()
    #     self.catedescrip = self.data_rule.ruledescription()
    #     self.categoryruleid = self.data_rule.ruleruleid()
    #     self.categoryrulelevel = self.data_rule.rulerulelevel()
    #     self.categoryid = self.data_rule.ruletechnologyid()
    #     self.categroup = self.data_rule.rulegroup()
    #     self.cateoptions = self.data_rule.ruleoptions()
    #     self.cateif_matched_sid = self.data_rule.ruleif_matched_sid()
    #     self.categoryfield = self.data_rule.rulefield()
    #
    #     return self.categoryif_sid, self.categorymatch, self.catedescrip, self.categoryruleid, self.categoryrulelevel, \
    #            self.categoryid, self.cateoptions, self.categroup, self.cateif_matched_sid, self.categoryfield
    #
    # def reluall(self):
    #     '''
    #     调用使用类型的
    #     :return:
    #     '''
    #     self.rule_regulation_syslog()
    #     self.rule_regulation_firewall()
    #     self.rule_regulation_ids()
    #     self.rule_regulation_weblog()
    #     self.rule_regulation_squid()
    #     self.rule_regulation_windows()
    #     self.rule_regulation_ossec()

if __name__ == '__main__':
    dirlist = r'E:\Desktop\niso_server-main\rules'
    dm = Calling_conventions(dirlist)
    dm.rule_universal_all()