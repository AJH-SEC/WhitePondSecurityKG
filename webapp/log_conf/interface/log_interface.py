from abc import ABCMeta,abstractmethod

# 日志接受处理接口
class LogDealController(metaclass=ABCMeta):
    # 从kafka消息队列中接受日志
    @abstractmethod
    def recv_kafka_messages(self):
        pass
    
    # 从mq消息队列中接受日志
    @abstractmethod
    def recv_Mq_messages(self):
        pass

    # 从syslog 中接受日志
    @abstractmethod
    def recv_syslog_messages(self):
        pass
    
    # 日志存储到neo4j图数据库中
    @abstractmethod
    def storage_log_to_neo4j(self):
        pass

    # 日志存储到nebula graph图数据库中
    @abstractmethod
    def storage_log_to_nebulagraph(self):
        pass

# 从数据库中查询
class MatchDataToDb(metaclass=ABCMeta):
    # 按告警信息中mitre字段进行查询
    @abstractmethod
    def match_by_technique(self):
        pass

    # 按告警信息中软件信息进行查询
    @abstractmethod
    def match_by_software(self):
        pass
