import time

import pymysql
from lxml import etree

import requests

from u17.agent_helper import get_random_agent

ua = get_random_agent()
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '1107'
MYSQL_DATABASE = 'uyq'
total = 0


def get_db():
    db = pymysql.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE, charset='utf8',
                         port=MYSQL_PORT)
    return db


def get_cursor(db):
    cursor = db.cursor()
    return cursor


def close_spider(db):
    # 关闭数据库连接
    db.close()


def insert_sql(tags, click_num, monthly_ticket, desc, col_num, comic_id):
    global total
    sql = 'insert into info(tags,click_num,monthly_ticket,`desc`,col_num,comic_id) values (%s,%s,%s,%s,%s,%s)'
    db = get_db()
    cursor = get_cursor(db)
    cursor.execute(sql, (tags, click_num, monthly_ticket, desc, col_num, comic_id))
    db.commit()
    time.sleep(0.2)
    close_spider(db)
    time.sleep(0.2)
    total += 1
    print(f'插入成功！当前是第{total}条数据,comic_id是:::{comic_id}')


def get_comic_ids():
    sql = 'select comic_id from u'
    db = get_db()
    cursor = get_cursor(db)
    cursor.execute(sql)
    lis = [i[0] for i in cursor.fetchall()]
    close_spider(db)
    return lis


def requests_html(url, comic_id):
    response = requests.get(url=url, headers={"User-Agent": ua})
    if response.status_code == 200:
        etree_html = etree.HTML(response.text)
        tags = '|'.join([x.strip() for x in etree_html.xpath('.//div[@class="line1"]/a//text()')])
        num_all = etree_html.xpath('.//div[@class="cf line2"]/div//span[@class="color_red"]')
        # 点击量
        click_num = ''.join([x.strip() for x in num_all[0].xpath('.//text()')])
        # 总月票
        monthly_ticket = ''.join([x.strip() for x in num_all[1].xpath('.//text()')])
        desc = ''.join(etree_html.xpath('.//p[@class="ti2"]//text()'))
        col_num = etree_html.xpath('.//span[@id="bookrack"]//text()')[2]
        insert_sql(tags, click_num, monthly_ticket, desc, col_num, comic_id)


def get_last_data():
    sql = 'select comic_id from info order by id DESC limit 1'
    db = get_db()
    cursor = get_cursor(db)
    cursor.execute(sql)
    lis = [i[0] for i in cursor.fetchall()]
    close_spider(db)
    return lis[0]


def main():
    lis = get_comic_ids()
    for index, i in enumerate(lis, 0):
        # 断点续传
        get_last_index = lis.index(get_last_data())
        if index > get_last_index:
            requests_html(f'http://www.u17.com/comic/{i}.html', i)


if __name__ == '__main__':
    main()
