from util.read_config import ConfigInstance
from common.myasync import run_task, main_run_task
from common.mythresd import deal_thread, deal_thread_async, start_thread_fuc,start_thread_pool
from common.mymultiprocessing import deal_process
from kafka import KafkaConsumer,KafkaProducer
import logging
import datetime
import threading
import asyncio
import time

class ReadLogDataByKafka:
    
    def __init__(self, host, port, topic_name) -> None:
        '''
        param host: kafka地址, str
        param port: kafka端口号, str
        param topic_name: kafka监听的主题名称, str
        '''
        self.kafka_server_host = host
        self.kafka_server_port = port
        self.kafka_topic_name = topic_name
        
        self.consumer = KafkaConsumer(self.kafka_topic_name, bootstrap_servers=self.kafka_server_host+":"+self.kafka_server_port,)
       
    #设置主题名称
    def set_kafka_topic_name(self, topic_name):
        '''
        param topic_name: kafka监听的主题名称, str
        '''
        self.kafka_topic_name = topic_name

    #设置ip地址
    def set_kafka_server_host(self,host):
        '''
        param host: kafka地址, str
        '''
        self.kafka_server_host = host

    #设置端口号
    def set_kafka_server_port(self,port):
        '''
        param port: kafka端口号, str
        '''
        self.kafka_server_port = port

    # 从topic读取数据并进行处理，callback为回调函数
    def read_from_consumer_to_deal(self, callback):
        '''
        param callback: 消息处理回调函数, func
        '''
        start_time = time.perf_counter()
        print("开始运行：", start_time)
        # asyncio.run(run_task(self.consumer, callback))
        # asyncio.run(main_run_task(self.consumer, callback))
        # deal_thread(self.consumer, callback)
        # deal_process(self.consumer, callback)
        # deal_thread_async(self.consumer, callback)
        # start_thread_fuc(self.consumer, callback)
        start_thread_pool(self.consumer, callback)
        print("代码运行时间为：", time.perf_counter() - start_time)

        # for message in self.consumer:
        #     data = message.value.decode()
        #     topic_name = message.topic
        #     logging.debug("recv topic name {}, data: {}".format(topic_name, data))
        #     print(("recv topic name {}, data: {}".format(topic_name, data, datetime.datetime.now())))

        #     threading.Thread(target=callback, args=(data, topic_name))
        #     callback(data, topic_name)

    # 向topic写入数据
    def send_data_to_product(self, data):
        self.product = KafkaProducer(bootstrap_servers=self.kafka_server_host+":"+self.kafka_server_port,)
        self.product.send(self.kafka_topic_name,data)
    
    # kakfa关闭函数
    def close_kafka(self):
        self.consumer.close()
