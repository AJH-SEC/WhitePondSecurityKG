from util.read_config import ConfigInstance
from kafka import KafkaConsumer,KafkaProducer
import logging


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
        for message in self.consumer:
            data = message.value.decode()
            topic_name = message.topic
            logging.debug("recv topic name {}, data: {}".format(topic_name, data))
            print(("recv topic name {}, data: {}".format(topic_name, data)))
            callback(data, topic_name)

    # 向topic写入数据
    def send_data_to_product(self, data):
        self.product = KafkaProducer(bootstrap_servers=self.kafka_server_host+":"+self.kafka_server_port,)
        self.product.send(self.kafka_topic_name,data)
    
    # kakfa关闭函数
    def close_kafka(self):
        self.consumer.close()
