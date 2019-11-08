# 读取mysql数据
import pandas as pd
import pymysql
import numpy as np
import matplotlib.pyplot as plt

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)

plt.rcParams['font.sans-serif'] = ['KaiTi']
plt.rcParams['font.serif'] = ['KaiTi']

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1107', db='uyq')
# 采用右连接，保证数据的完整性 select * from u a right outer join info b on a.comic_id = b.comic_id;
sql_str = 'select a.comic_id,a.name,a.category,a.cover,b.click_num,b.monthly_ticket,b.col_num from' \
          ' u a right outer join info b on a.comic_id = b.comic_id'
result = pd.io.sql.read_sql_query(sql_str, conn)
# print(type(result), '\n', result)

# ['comic_id', 'name', 'category', 'cover', 'click_num', 'monthly_ticket', 'col_num']
# 根据收藏量排序
sort_col_num = result.sort_values(by=['col_num', 'monthly_ticket'], ascending=(False, True))
print(sort_col_num)
# # 获取前10行数据
# lis10 = result.sort_values(by=['col_num', 'monthly_ticket'], ascending=(False, True))[:10]
# print(lis10)
#
# lis11 = lis10.drop(['category', 'comic_id', 'cover', 'click_num'], axis=1)
# print(lis11)
# lis11.set_index('name', inplace=True)
# print(lis11)
# lis11.plot(kind='bar')
# t = np.arange(0, 69, 1)
# plt.plot(t, t, 'r', t, t ** 2, 'b')
# plt.show()
# plt.savefig("temp.jpg")
sort_col_num.to_excel('test.xlsx')
