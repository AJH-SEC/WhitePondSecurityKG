from util.read_config import ConfigInstance
from dao.initdb import Neo4jDb


class DealLogInterface:
    config_file_name = ''
    def __init__(self, config_file_name) -> None:
        '''
        param config_file_name: 配置文件名称, str
        '''
        self.config_instance = ConfigInstance()
        self.config_instance.set_config(config_file_name)
        self.config_file_name = config_file_name
        self.neo4j_db = Neo4jDb(self.config_instance.get_neo4j_config()["host_url"], self.config_instance.get_neo4j_config()["username"], self.config_instance.get_neo4j_config()["password"])
    