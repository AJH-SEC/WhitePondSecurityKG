from dao.recv_netfow import RecvNet
from dao.recv_security_equipment import RecvSecurityEquipment
from dao.recv_wazuh import RecvWazuhAlert, RecvNormalLog

import threading
import time

class RecvLogTaskManage:
    def __init__(self) -> None:
        self.task_queue = []
    
    # 流量日志处理线程
    def start_run_net_task(self):
        recv_netflow_instance = RecvNet("config.json")
        self.start_net_task = threading.Thread(target=recv_netflow_instance.recv_net_packet_by_kafka, args=())
        self.start_net_task.start()
        self.task_queue.append(self.start_net_task)

    # 防火墙日志处理线程
    def start_run_fw_task(self):
        recv_security_instance = RecvSecurityEquipment("config.json")
        self.fwtask = threading.Thread(target=recv_security_instance.recv_fw_to_deal)
        self.fwtask.start()
        self.task_queue.append(self.fwtask)

    # ips日志处理线程
    def start_run_ips_task(self):
        recv_security_instance = RecvSecurityEquipment("config.json")
        self.fwtask = threading.Thread(target=recv_security_instance.recv_ips_to_deal)
        self.fwtask.start()
        self.task_queue.append(self.fwtask)

    # waf日志处理线程
    def start_run_waf_task(self):
        recv_security_instance = RecvSecurityEquipment("config.json")
        self.wafask = threading.Thread(target=recv_security_instance.recv_waf_to_deal)
        self.wafask.start()
        self.task_queue.append(self.wafask)

    # web版本溯源日志处理线程
    def start_run_apt_web_task(self):
        recv_security_instance = RecvSecurityEquipment("config.json")
        self.apt_web_task = threading.Thread(target=recv_security_instance.recv_apt_web_to_deal)
        self.apt_web_task.start()
        self.task_queue.append(self.apt_web_task)

    # 网络版本溯源日志处理线程
    def start_run_apt_net_task(self):
        recv_security_instance = RecvSecurityEquipment("config.json")
        self.apt_net_task = threading.Thread(target=recv_security_instance.recv_apt_net_to_deal)
        self.apt_net_task.start()
        self.task_queue.append(self.apt_net_task)

    # 邮件溯源
    # 日志处理线程
    def start_run_apt_mail_task(self):
        recv_security_instance = RecvSecurityEquipment("config.json")
        self.apt_mail_task = threading.Thread(target=recv_security_instance.recv_apt_mail_to_deal)
        self.apt_mail_task.start()
        self.task_queue.append(self.apt_mail_task)

    # 蜜罐日志处理线程
    def start_run_honey_task(self):
        recv_security_instance = RecvSecurityEquipment("config.json")
        self.honey_task = threading.Thread(target=recv_security_instance.recv_honey_to_deal)
        self.honey_task.start()
        self.task_queue.append(self.honey_task)
    
    # wauzh日志处理线程
    def start_run_wauzh_alert_task(self):
        recv_wauzh_alert_instance = RecvWazuhAlert("config.json")
        self.wauzh_task = threading.Thread(target=recv_wauzh_alert_instance.recv_wazuh_to_deal)
        self.wauzh_task.start()
        self.task_queue.append(self.wauzh_task)

    # 普通日志处理线程
    def start_run_normal_task(self):
        recv_noraml_log_instance = RecvNormalLog("config.json")
        recv_noraml_log_instance.recv_nomal_log_to_deal()
        # self.normal_log_task = threading.Thread(target=recv_noraml_log_instance.recv_nomal_log_to_deal)
        # self.normal_log_task.start()
        # self.task_queue.append(self.normal_log_task)
        print("test")

    # 开始安全事件和流量处理线程
    def start_all_task_security_netflow(self):
        self.start_run_net_task()
        # self.start_run_fw_task()
        # self.start_run_ips_task()
        # self.start_run_waf_task()
        # self.start_run_apt_web_task()
        # self.start_run_apt_net_task()
        # self.start_run_apt_mail_task()
        # self.start_run_honey_task()

    # 开始处理wauzh告警日志和普通事件日志（filebeat,auditbeat）
    def start_wauzh_normal_log(self):
        self.start_run_wauzh_alert_task()
        self.start_run_normal_task()

    # 进程观察
    def super_visitor(self):
        while True:
            if len(self.task_queue) > 0:
                for task in self.task_queue:
                    if task.is_alive():
                        continue
                    else:
                        task.run()
            time.sleep(5)
