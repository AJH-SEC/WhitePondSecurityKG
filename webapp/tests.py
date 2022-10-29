from django.test import TestCase

# Create your tests here.
import time
from datetime import datetime
# t = time.mktime(time.localtime())
# # now = datetime.utcfromtimestamp(t)
# now = datetime.utcfromtimestamp(t)
# end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
# print(t)
# print(now)
# print(end_time)
n = datetime.now()
now_str = n.strftime("%d %B %Y")
form_dic = {}
form_dic.update(created=now_str, last_modified=now_str)
print(form_dic)

res = {'Datasource': 38, 'DatasourceComponent': 109, 'Software': 583, 'Groups': 130, 'Mitigations': 43, 'Techniques': 191, 'SubTechniques': 385, 'Tactics': 14, 'overview': 4441}
res.pop('overview')
print(sum(res.values()))

# aodata = [{"name":"sEcho","value":2},{"name":"iColumns","value":9},{"name":"sColumns","value":",,,,,,,,"},{"name":"iDisplayStart","value":30},
#           {"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":"start_node label"},{"name":"sSearch_0","value":""},{"name":"bRegex_0","value":false},
#           {"name":"bSearchable_0","value":true},{"name":"bSortable_0","value":true},{"name":"mDataProp_1","value":"start_node id"},{"name":"sSearch_1","value":""},
#           {"name":"bRegex_1","value":false},{"name":"bSearchable_1","value":true},{"name":"bSortable_1","value":true},{"name":"mDataProp_2","value":"start_node name"},
#           {"name":"sSearch_2","value":""},{"name":"bRegex_2","value":false},{"name":"bSearchable_2","value":true},{"name":"bSortable_2","value":true},
#           {"name":"mDataProp_3","value":"relationship"},{"name":"sSearch_3","value":""},{"name":"bRegex_3","value":false},{"name":"bSearchable_3","value":true},
#           {"name":"bSortable_3","value":true},{"name":"mDataProp_4","value":"end_node label"},{"name":"sSearch_4","value":""},{"name":"bRegex_4","value":false},
#           {"name":"bSearchable_4","value":true},{"name":"bSortable_4","value":true},{"name":"mDataProp_5","value":"end_node id"},{"name":"sSearch_5","value":""},
#           {"name":"bRegex_5","value":false},{"name":"bSearchable_5","value":true},{"name":"bSortable_5","value":true},{"name":"mDataProp_6","value":"end_node name"},
#           {"name":"sSearch_6","value":""},{"name":"bRegex_6","value":false},{"name":"bSearchable_6","value":true},{"name":"bSortable_6","value":true},
#           {"name":"mDataProp_7","value":null},{"name":"sSearch_7","value":""},{"name":"bRegex_7","value":false},{"name":"bSearchable_7","value":true},
#           {"name":"bSortable_7","value":false},{"name":"mDataProp_8","value":null},{"name":"sSearch_8","value":""},{"name":"bRegex_8","value":false},
#           {"name":"bSearchable_8","value":true},{"name":"bSortable_8","value":true},{"name":"sSearch","value":""},{"name":"bRegex","value":false},
#           {"name":"iSortCol_0","value":0},{"name":"sSortDir_0","value":"asc"},{"name":"iSortingCols","value":1}]

# from datetime import date, timedelta
# log_list = []
# for i in range(30):
#     start_date = date.today() + timedelta(-i)
#     start = start_date.strftime('%Y-%m-%dT00:00:00.000Z')
#     end = start_date.strftime('%Y-%m-%dT23:59:59.999Z')
#     print(start)
#     print(end)
#     print(start_date)
#     log_list.append(start_date)
# print(len(log_list))
l = 'DatasourceComponent'
print(l.upper())


