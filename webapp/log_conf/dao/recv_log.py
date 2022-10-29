from interface.log_interface import LogDealController
from kafka import KafkaConsumer, KafkaProducer


class KafkaConsumerInstance(LogDealController):
    # 默认配置信息
    kafka_topic_name = "packetbeat_log_test" # 配置kafka消费主题
    kafka_server_ip = "192.168.1.110"  # 配置kafka的ip地址
    kafka_server_port = "9092"  # 配置kafka的端口

    def __init__(self):
        self.consumer = KafkaConsumer(self.kafka_topic_name, bootstrap_servers=self.kafka_server_ip+":"+self.kafka_server_port,)
        self.product = KafkaProducer(bootstrap_servers=self.kafka_server_ip+":"+self.kafka_server_port,)

    #设置主题名称
    def set_kafka_topic_name(self, topic_name):
        '''
        param topic_name: kafka主题名称
        '''
        self.kafka_topic_name = topic_name

    #设置ip地址
    def set_kafka_server_ip(self,ip):
        '''
        param ip: kafka服务地址
        '''
        self.kafka_server_ip = ip

    #设置端口号
    def set_kafka_server_port(self, port):
        '''
        param ip: kafka服务端口
        '''
        self.kafka_server_port = port

    # 从topic读取数据并进行处理，callback为回调函数
    def read_from_consumer_to_deal(self, callback):
        '''
        param callback: 回调函数
        '''
        for message in self.consumer:
            callback(message)

    # 向topic写入数据
    def send_data_to_product(self, data):
        self.product.send(self.kafka_topic_name,data)

    def recv_Mq_messages(self):
        pass

    def recv_syslog_messages(self):
        pass

    def storage_log_to_neo4j(self):
        pass

    def storage_log_to_nebulagraph(self):
        pass

