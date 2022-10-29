from sys import api_version
from util.read_config import ConfigInstance

# 获取模板文件接口
class GetTemplateDataInterface:
    def __init__(self, config_file_name) -> None:
        self.config_instance = ConfigInstance()
        self.config_instance.set_config(config_file_name)
    
    def get_type_list(self):
        pass
    
    def get_template_flow_file_path(self):
        pass

    def get_template_flow_data(self, type_val):
        '''
        param type_val: 日志的类型
        '''
        pass

    def get_type_dict(self):
        # TODO:该处将需要优化为数据库存储
        pass
