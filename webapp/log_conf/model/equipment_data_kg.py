# -*-coding:utf-8-*-
import json
import pandas as pd
from pandas import json_normalize
import ast
from itertools import groupby
from py2neo import Graph, Node, Relationship, NodeMatcher

# 防火墙日志数据
# 创建防火墙日志节点
class Create_FireWall_KG():

    def __init__(self, neo4j_profile, user_name, user_password):
        self.graph = Graph(neo4j_profile,auth=(user_name, user_password))
        self.matcher = NodeMatcher(self.graph)

    def FireWall(self, fire_data):
        """
        :param fire_data: 日志数据
        :return: Dict 每条日志信息
        """
        line_list = fire_data.strip().split(' ')
        # 直接有message信息的可以直接带有统计次数 建立节点
        if line_list[3] == 'message':
            generation_time = line_list[0]  # 日志生成时间
            count = line_list[5]            # 这条日志发生的次数
            receive_time = line_list[1] + " " + line_list[2] + line_list[7].strip("[")  # 日志接收时间
            apparatus_name = line_list[8]  # 设备名

            log_split = line_list[9].split(':')
            log_type = log_split[0].split('/')[0].replace("%%", "")  # LOG类型
            log_code = log_split[0].split('/')[1]                    # LOG代码
            log_name = log_split[0].split('/')[2]                    # LOG名字
            line_info = dict(i.strip().split('=') for i in log_split[1].split(','))

            log_all_info = {'日志发生次数': count, '日志生成时间': generation_time, '日志接收时间': receive_time,
                            '设备名': apparatus_name, 'LOG类型': log_type, '日志类型_Code': log_code,
                            '日志类型_Name': log_name}
            log_all_info.update(line_info)
            return log_all_info
        # 每一条日志数据都建立节点
        else:
            generation_time = line_list[0]                                   # 日志生成时间
            receive_time = line_list[1] + ' ' + line_list[2] + line_list[3]  # 日志接收时间
            apparatus_name = line_list[4]                                    # 设备名

            log_split = line_list[5].split(':')
            log_type = log_split[0].split('/')[0].replace("%%", "")  # LOG类型
            log_code = log_split[0].split('/')[1]                    # LOG代码
            log_name = log_split[0].split('/')[2]                    # LOG名字
            line_info = dict(i.strip().split('=') for i in log_split[1].split(','))

            log_all_info = {'日志生成时间': generation_time, '日志接收时间': receive_time,
                            '设备名': apparatus_name, 'LOG类型': log_type, '日志类型_Code': log_code,
                            '日志类型_Name': log_name}
            log_all_info.update(line_info)
            return log_all_info

    def create_FireWall(self, fire_data):
        """
        :param fire_data: 防火墙日志数据
        :return: 防火墙节点
        """
        log_all_info = self.FireWall(fire_data)
        fire_node = Node('防火墙', **log_all_info)
        self.graph.create(fire_node)

# 密罐日志数据
# 创建密罐日志节点，其与技术(子技术)的关系
class Create_Canister_KG():

    def __init__(self, neo4j_profile, user_name, user_password):
        self.graph = Graph(neo4j_profile,auth=(user_name, user_password))
        self.matcher = NodeMatcher(self.graph)

    def Canister(self, canister_data):
        """
        :param canister_data: 密罐日志数据
        :return: 字典(Type) 密罐日志数据
        """
        line_list = canister_data.strip().split('  ')

        generation_time = line_list[0].split(' ')[0]
        log_id = line_list[0].split(' ')[1]

        line_info = ast.literal_eval(line_list[1])  # 数据进行还原成字典 以便后续进行转换
        log_all_info = {'日志生成时间': generation_time, 'ID': log_id}
        log_all_info.update(line_info)

        # attack_ip_info 包含map类型数据，处理成dict类型
        aii_keys = list(log_all_info['attack_ip_info'].keys())
        log_all_info['attack_ip_info'] = list(log_all_info['attack_ip_info'].values())
        for num, item in enumerate(log_all_info['attack_ip_info']):
            log_all_info.update({'attack_ip_info' + '__' + str(aii_keys[num]): item})
        del log_all_info['attack_ip_info']

        # detail 包含map类型数据，处理成dict类型
        detail_keys = list(log_all_info['detail'].keys())
        log_all_info['detail'] = list(log_all_info['detail'].values())
        for num, item in enumerate(log_all_info['detail']):
            log_all_info.update({'detail' + '__' + str(detail_keys[num]): item})
        del log_all_info['detail']

        return log_all_info

    def create_Canister(self, canister_data, log_map_tec):
        """
        :param canister_data: 密罐日志数据
        :param log_map_tec: 字典(Type), 键【密罐日志中的关键字段(attack_type)】 : 值【所对应的技术点/子技术点】
        :return: 密罐日志节点、其与技术(子技术)之间的关系
        """
        # self.graph.run("match (标签:密罐) detach delete 标签")

        log_all_info = self.Canister(canister_data)
        canister_node = Node('密罐', **log_all_info)
        self.graph.create(canister_node)

        for log_code, tec in zip(list(log_map_tec.keys()), list(log_map_tec.values())):
            # 如果这条日志数据的关键字段在 自定义的字典映射表中，就建立关系
            # 否则就只建立节点
            if self.matcher.match('密罐').where("_.attack_type='" + log_code + "'").all() != []:
                tec_node = self.matcher.match('技术').where("_.ID=~'" + tec + "'").first()

                if tec_node == None:
                    sub_tec_node = self.matcher.match('子技术').where("_.ID=~'" + tec + "'").first()
                    if sub_tec_node != None:
                        relation = Relationship(canister_node, '密罐日志下使用的子技术', sub_tec_node)
                        self.graph.create(relation)

                if tec_node != None:
                    relation = Relationship(canister_node, '密罐日志下使用的技术', tec_node)
                    self.graph.create(relation)

# WAF日志数据
# WAF目前还没有映射规则
# 创建WAF日志节点，其与技术(子技术)的关系
class Create_WafIntercept_KG():

    def __init__(self, neo4j_profile, user_name, user_password):
        self.graph = Graph(neo4j_profile,auth=(user_name, user_password))
        self.matcher = NodeMatcher(self.graph)

    def WafIntercept(self, waf_data):
        """
        :param waf_data: WAF原始日志数据
        :return: 字典(Type) WAF日志数据
        """
        line_list = waf_data.strip().split(' ')

        generation_time = line_list[0]
        apparatus_name = line_list[1]
        # receive_time = line_list[2] + " " + line_list[3]
        line_list[2] = line_list[2] + " " + line_list[3]

        # 对WAF日志数据中的WAF特殊数据处理
        if line_list[3] == 'WAF':
            del line_list[4]
            log_ip = line_list[4].strip('->')

            del line_list[-1]
            line_info = dict(i.strip().split('=') for i in (",".join(line_list[5:])).split(','))

            log_all_info = {'日志生成时间': generation_time, '设备名称': apparatus_name, '日志接收时间': line_list[2],
                            '安全模块': line_list[3], '源IP': log_ip}
            log_all_info.update(line_info)
            return log_all_info

        else:
            # sec_mod = line_list[4].split(':')[0]
            line_list[3] = line_list[4].split(':')[0]
            line_list[4] = line_list[4].split(':')[1]

            list_val = []
            for line_value in line_list[4:]:
                line_split_list = str(line_value).split("=")
                if len(line_split_list) == 2:
                    list_val.append(line_split_list)

            line_info = dict(list_val)
            log_all_info = {'日志生成时间': generation_time, '设备名称': apparatus_name, '日志接收时间': line_list[2],
                            '安全模块': line_list[3]}
            log_all_info.update(line_info)
            return log_all_info

    def create_WafIntercept(self, waf_data):
        """
        :param waf_data: WAF原始日志数据
        :return: WAF日志节点
        """
        log_all_info = self.WafIntercept(waf_data)
        waf_node = Node('WAF', **log_all_info)
        self.graph.create(waf_node)

        # WAF数据暂时没有映射表
        """
        for log_code, tec in zip(list(log_map_tec.keys()), list(log_map_tec.values())):
            if self.matcher.match('Web').where("_.事件代码='" + log_code + "'").all() != []:
                tec_node = self.matcher.match('技术').where("_.ID=~'" + tec + "'").first()
                print(tec_node)
                if tec_node == None:
                    sub_tec_node = self.matcher.match('子技术').where("_.ID=~'" + tec + "'").first()
                    if sub_tec_node != None:
                        relation = Relationship(waf_node, ' WAF日志下使用的子技术', sub_tec_node)
                        self.graph.create(relation)

                if tec_node != None:
                    relation = Relationship(waf_node, 'WAF日志下使用的技术', tec_node)
                    self.graph.create(relation)
        """

# WEB日志数据
# 创建Web日志节点，其与技术(子技术)的关系
class Create_Web_KG():

    def __init__(self, neo4j_profile, user_name, user_password):
        self.graph = Graph(neo4j_profile,auth=(user_name, user_password))
        self.matcher = NodeMatcher(self.graph)

    def Web(self, web_data):
        """
        :param web_data: web原始日志数据
        :return: 字典(Type) web日志数据
        """
        line_list = web_data.strip().split(" ")

        generation_time = line_list[0]              # 日志生成时间
        apparatus_name = line_list[1]               # 设备名字
        apparatus_ip = line_list[3]
        log_sender = line_list[4]

        columns = ['系统名字', '系统代码', '源IP', '源端口', '目的IP', '目的端口',
                   '传输层协议', '超文本传输协议', '事件代码', '事件名', '事件', '事件发生时间',
                   '事件级别', '溯源报告地址', '设备IP', '网络数据报告地址', 'URI', '提交方式']
        # 针对数据中`XXE 攻击`来判定
        if len(line_list) > 7:
            line_list_5 = line_list[5] + line_list[6] + ' ' + line_list[7]
            del line_list[7], line_list[6], line_list[5], line_list[2]

            line_list_5 = line_list_5.strip().split('|*')
            line_info = dict(zip(columns, line_list_5))
            log_all_info = {'日志生成时间': generation_time, '设备名字': apparatus_name, '设备IP': apparatus_ip,
                            '系统日志发送器': log_sender}
            log_all_info.update(line_info)
            return log_all_info

        else:
            line_list_5 = line_list[5] + ' ' + line_list[6]
            del line_list[6], line_list[5], line_list[2]
            line_list_5 = line_list_5.strip().split('|*')
            line_info = dict(zip(columns, line_list_5))
            log_all_info = {'日志生成时间': generation_time, '设备名字': apparatus_name, '设备IP': apparatus_ip,
                            '系统日志发送器': log_sender}
            log_all_info.update(line_info)
            return log_all_info

    def create_Web(self, web_data, log_map_tec):
        """
        :param web_data: WEB日志原始数据
        :param log_map_tec: 字典（Type），键【web日志中的关键字段(事件代码)】 : 值【所对应的技术点/子技术点】
        :return: WEB日志节点、其与技术(子技术)之间的关系
        """

        # self.graph.run("match (标签:Web) detach delete 标签")
        log_all_info = self.Web(web_data)
        web_node = Node('Web', **log_all_info)
        self.graph.create(web_node)

        for log_code, tec in zip(list(log_map_tec.keys()), list(log_map_tec.values())):
            if self.matcher.match('Web').where("_.事件代码='" + log_code + "'").all() != []:
                tec_node = self.matcher.match('技术').where("_.ID=~'" + tec + "'").first()
                print(tec_node)
                if tec_node == None:
                    sub_tec_node = self.matcher.match('子技术').where("_.ID=~'" + tec + "'").first()
                    if sub_tec_node != None:
                        relation = Relationship(web_node, ' WEB日志下使用的子技术', sub_tec_node)
                        self.graph.create(relation)

                if tec_node != None:
                    relation = Relationship(web_node, 'WEB日志下使用的技术', tec_node)
                    self.graph.create(relation)

# 网络日志数据
# 创建网络日志节点，其与技术(子技术)的关系
class Create_Internet_KG():

    def __init__(self, neo4j_profile, user_name, user_password):
        self.graph = Graph(neo4j_profile,auth=(user_name, user_password))
        self.matcher = NodeMatcher(self.graph)

    def Internet(self, internet_data):
        """
        :param internet_data: 网络日志原始数据
        :return: 字典(Type) 网络日志数据
        """
        line_list = internet_data.strip().split(' ')

        generation_time = line_list[0]          # 日志生成时间
        apparatus_ip = line_list[1]             # 设备ip
        log_sender = line_list[2]
        line_time = line_list[3] + " " + line_list[4]
        del line_list[4], line_list[3]
        line_list.insert(3, line_time)
        line_list_3 = ''.join(line_list[3:]).strip().split('|*')
        del line_list[3:]

        columns = ['系统名字', '系统代码', '源IP', '源端口', '目的IP', '目的端口',
                   '传输层协议', '超文本传输协议', '事件代码', '事件名', '事件', '事件发生时间',
                   '事件级别', '溯源报告地址', '设备IP', '网络数据报告地址', 'URl', '端口扫描方式',
                   '代号(1)', '代号(2)']
        line_info = dict(zip(columns, line_list_3))
        log_all_info = {'日志生成时间': generation_time, '设备IP': apparatus_ip, '系统日志发送器': log_sender}
        log_all_info.update(line_info)
        # print(log_all_info)
        return log_all_info

    def create_Internet(self, internet_data, log_map_tec):
        """
        :param internet_data: 网络版原始日志数据
        :param log_map_tec: 字典(Type) 键【网络日志中的关键字段(事件代码)】 : 值【所对应的技术点/子技术点】
        :return: web日志节点、其与技术(子技术)之间的关系
        """
        log_all_info = self.Internet(internet_data)
        internet_node = Node('网络', **log_all_info)
        self.graph.create(internet_node)
        for log_code, tec in zip(list(log_map_tec.keys()), list(log_map_tec.values())):
            if self.matcher.match('网络').where("_.事件代码='" + log_code + "'").all() != []:
                tec_node = self.matcher.match('技术').where("_.ID=~'" + tec + "'").first()
                if tec_node == None:
                    sub_tec_node = self.matcher.match('子技术').where("_.ID=~'" + tec + "'").first()
                    if sub_tec_node != None:
                        relation = Relationship(internet_node, '网络日志下使用的子技术', sub_tec_node)
                        self.graph.create(relation)

                if tec_node != None:
                    relation = Relationship(internet_node, '网络日志下使用的技术', tec_node)
                    self.graph.create(relation)

# 邮件日志数据
# 创建邮件日志节点，其与技术(子技术)的关系
# 注意传进来的邮件原始日志数据的换行符，防止转义
class Create_Mail_KG():

    def __init__(self, neo4j_profile, user_name, user_password):
        self.graph = Graph(neo4j_profile,auth=(user_name, user_password))
        self.matcher = NodeMatcher(self.graph)

    def Mail(self, mail_data):
        """
        :param mail_data: 邮件原始日志数据
        :return: 字典(Type) 邮件日志数据
        """
        # print(r"{}".format(mail_data))
        line_list = mail_data.strip().split(' ')
        generation_time = line_list[0]
        apparatus_type = line_list[1]
        apparatus_name = line_list[2]

        line_info = ast.literal_eval("".join(line_list[3:]))
        log_all_info = {'日志生成时间': generation_time, '设备类型': apparatus_type, '设备名称': apparatus_name}
        log_all_info.update(line_info)

        tt_keys = [list(i.keys()) for i in log_all_info['tt']]
        log_all_info['tt'] = [list(i.values()) for i in log_all_info['tt']]
        for num, item in enumerate(log_all_info['tt']):
            for index in range(len(item)):
                log_all_info.update({'tt__list' + str(num) + '__' + str(tt_keys[num][index]): item[index]})
            log_all_info.update({'值' + '__' + str(num): item[1].split('：')[0]})     # 注意此处冒号为中文字符
        length = len(log_all_info['tt'])
        del log_all_info['tt']

        re_keys = [list(i.keys()) for i in log_all_info['re']]
        log_all_info['re'] = [list(i.values()) for i in log_all_info['re']]
        for num, item in enumerate(log_all_info['re']):
            for index in range(len(item)):
                log_all_info.update({'re__list' + str(num) + '__' + str(re_keys[num][index]): item[index]})
        del log_all_info['re']

        return log_all_info, length

    def create_Mail(self, mail_data, log_map_tec):
        """
        :param mail_data: 邮件原始日志数据
        :param log_map_tec: 字典（Type），键【邮件日志中的关键字段(tt.ty)】 : 值【所对应的技术点/子技术点】
        :return: 邮件日志节点、邮件日志节点与技术(子技术)之间的关系
        """
        # self.graph.run("match (标签:邮件) detach delete 标签")

        log_all_info, length = self.Mail(mail_data)
        mail_node = Node('邮件', **log_all_info)
        self.graph.create(mail_node)

        for num in range(length):
            for log_code, tec in zip(list(log_map_tec.keys()), list(log_map_tec.values())):
                if self.matcher.match('邮件').where("_.值__" + str(num) + "=~'" + log_code + "'").all() != []:
                    tec_node = self.matcher.match('技术').where("_.ID=~'" + tec + "'").first()
                    if tec_node == None:
                        sub_tec_node = self.matcher.match('子技术').where("_.ID=~'" + tec + "'").first()
                        if sub_tec_node != None:
                            relation = Relationship(mail_node, '邮件日志下' + log_code + '使用的子技术', sub_tec_node)
                            self.graph.create(relation)

                    if tec_node != None:
                        relation = Relationship(mail_node, '邮件日志' + log_code + '下使用的技术', tec_node)
                        self.graph.create(relation)



