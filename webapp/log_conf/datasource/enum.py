from enum import Enum
class PacketEnum(Enum):
    NET_ASSERT = 'NET_ASSERT'
    FLOW_NODE = 'FLOW_NODE'
    FLOW_RELATE_LABEL = 'FLOW_RELATE_LABEL'

class NormalBeatsDealEnum(Enum):
    '''
    常规beat日志枚举
    '''
    NORMAL_LOG = "NormalLog"
    LOG_ID = "log_id"
