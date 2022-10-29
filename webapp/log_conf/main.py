from re import A
from dao.recv_netfow import RecvNet
from dao.initdb import Neo4jDb
from dao.recv_security_equipment import RecvSecurityEquipment
from dao.recv_wazuh import RecvWazuhAlert
from dao.task_manage import RecvLogTaskManage
from util.read_config import ConfigInstance

from multiprocessing import Pool
import asyncio
import threading

import logging

conf = ConfigInstance()
conf.set_config("config.json")

logging.basicConfig(filename='niso.log', level=conf.get_log_level_config(),
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def recursion_map_value(map_value, pre_key):
    key_value_map = {}
    for key, value in map_value.items():
        key = pre_key + "__" + key
        if type(value) == type(dict()):
            dat_emp = recursion_map_value(value, key)
            key_value_map.update(dat_emp)
        elif type(value) == type([]):
            key_value_map[key] = ",".join([i for i in value])
        else:
            key_value_map[key] = value
    return key_value_map


# async def start_net():
#     recv_netflow_instance = RecvNet("config.json")
#     netflowtask = asyncio.create_task(recv_netflow_instance.recv_net_packet_by_kafka())
#     await netflowtask

# async def start_security_fw():
#     recv_security_instance = RecvSecurityEquipment("config.json")
#     fwtask = asyncio.create_task(recv_security_instance.recv_fw_to_deal())
#     await fwtask

# async def start_security_apt():
#     recv_security_instance = RecvSecurityEquipment("config.json")
#     fwtask = asyncio.create_task(recv_security_instance.recv_apt_to_deal())
#     await fwtask

# async def start_security_waf():
#     recv_security_instance = RecvSecurityEquipment("config.json")
#     fwtask = asyncio.create_task(recv_security_instance.recv_waf_to_deal())
#     await fwtask

# async def main():
#     # asyncio.create_task(start_net())
#     asyncio.create_task(start_security_fw())
#     asyncio.create_task(start_security_apt())
#     asyncio.create_task(start_security_waf())
    # recv_security_instance = RecvSecurityEquipment("config.json")
    # recv_wazuh_instance = RecvWazuhAlert("config.json")

    
    # await netflowtask
    # fwtask = asyncio.create_task(recv_security_instance.recv_fw_to_deal())
    # apttask = asyncio.create_task(recv_security_instance.recv_apt_to_deal())
    # waftask = asyncio.create_task(recv_security_instance.recv_waf_to_deal())
    # ipstask = asyncio.create_task(recv_security_instance.recv_ips_to_deal())
    # honeytask = asyncio.create_task(recv_security_instance.recv_honey_to_deal())
    # wazuhtask = asyncio.create_task(recv_wazuh_instance.recv_wazuh_to_deal())

    
    # await fwtask
    # await apttask
    # await waftask
    # await ipstask
    # await honeytask
    # await wazuhtask

def start_run_net_task():
    recv_netflow_instance = RecvNet("config.json")
    start_net_task = threading.Thread(target=recv_netflow_instance.recv_net_packet_by_kafka, args=())
    start_net_task.start()

def start_run_fw_task():
    recv_security_instance = RecvSecurityEquipment("config.json")
    fwtask = threading.Thread(target=recv_security_instance.recv_fw_to_deal)
    fwtask.start()

def start_run_ips_task():
    recv_security_instance = RecvSecurityEquipment("config.json")
    fwtask = threading.Thread(target=recv_security_instance.recv_ips_to_deal)
    fwtask.start()

def start_run_waf_task():
    recv_security_instance = RecvSecurityEquipment("config.json")
    fwtask = threading.Thread(target=recv_security_instance.recv_waf_to_deal)
    fwtask.start()

def start_run_apt_web_task():
    recv_security_instance = RecvSecurityEquipment("config.json")
    fwtask = threading.Thread(target=recv_security_instance.recv_apt_web_to_deal)
    fwtask.start()

def start_run_apt_net_task():
    recv_security_instance = RecvSecurityEquipment("config.json")
    fwtask = threading.Thread(target=recv_security_instance.recv_apt_net_to_deal)
    fwtask.start()

def start_run_apt_mail_task():
    recv_security_instance = RecvSecurityEquipment("config.json")
    fwtask = threading.Thread(target=recv_security_instance.recv_apt_mail_to_deal)
    fwtask.start()

def start_run_honey_task():
    recv_security_instance = RecvSecurityEquipment("config.json")
    fwtask = threading.Thread(target=recv_security_instance.recv_honey_to_deal)
    fwtask.start()


if __name__ == "__main__":
#     task = RecvLogTaskManage()
#     task.start_all_task_security_netflow()
    RecvLogTaskManage().start_all_task_security_netflow()
    # task.start_wauzh_normal_log()
    # task.super_visitor()


    