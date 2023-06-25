from selenium import webdriver
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pymysql
import time


def login_and_scrape_flight_data(db_manager):  # 登陆上网站
    driver_path = '/Users/bunnylu/Desktop/chromedriver_mac_arm64/chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path)
    url = 'https://flightadsb.variflight.com/'
    driver.get(url)
    driver.maximize_window()
    driver.find_element('xpath', '//*[@id="app"]/div/div[2]/div[1]/i').click()
    driver.find_element('xpath', '//*[@id="app"]/div/div[2]/div/ul[2]/li[4]/div/span').click()
    time.sleep(30)
    print('login success')
    driver.switch_to.window(driver.window_handles[-1]) # 切换到最新打开的窗口
    print('1')
    tds=driver.find_elements('xpath',
                             '//*[@id="app"]/div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div/div[3]/table/tbody/tr/td[1]/div')
    print('2')
    # count = 0  # 计数器变量
    for td in tds:
        driver.execute_script("arguments[0].scrollIntoView();", td)
        print('3')
        td.click()
        print('4')
        time.sleep(10)
        parsed_data = parse_data(driver.page_source)
        db_manager.insert_data(parsed_data)
        # count += 1  # 计数器加一
        # if count == 1:  # 当计数器达到2时跳出循环
        #     break
        time.sleep(10)
        driver.find_element('xpath', '//*[@id="app"]/div/div[4]/div[2]/div/div[1]/i').click()
        time.sleep(10)
        driver.find_element('xpath', '//*[@id="icon-container"]/i').click()
        time.sleep(10)


def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    try:
        data = {
            'country': soup.select_one(
                '#app div:nth-child(4) div:nth-child(2) div div:nth-child(2) div:nth-child(4) div:nth-child(2) div:nth-child(2) div:nth-child(2)').text.replace(
                '\n', '').replace(' ', ''),
            'aircraft_model': soup.select_one(
                '#app div:nth-child(4) div:nth-child(2) div div:nth-child(2) div:nth-child(4) div:nth-child(2) div:nth-child(4) div:nth-child(2)').text.replace(
                '\n', '').replace(' ', ''),
            'longitude': soup.select_one(
                '#app div:nth-child(4) div:nth-child(2) div div:nth-child(2) div:nth-child(5) div:nth-child(2) div:nth-child(2) div:nth-child(2)').text,
            'latitude': soup.select_one(
                '#app div:nth-child(4) div:nth-child(2) div div:nth-child(2) div:nth-child(5) div:nth-child(2) div:nth-child(3) div:nth-child(2)').text,
            'altitude': soup.select_one(
                '#app div:nth-child(4) div:nth-child(2) div div:nth-child(2) div:nth-child(5) div:nth-child(2) div:nth-child(4) div:nth-child(2)').text,
            'horizontal_speed': soup.select_one(
                '#app div:nth-child(4) div:nth-child(2) div div:nth-child(2) div:nth-child(5) div:nth-child(2) div:nth-child(5) div:nth-child(2)').text,
            'heading': soup.select_one(
                '#app div:nth-child(4) div:nth-child(2) div div:nth-child(2) div:nth-child(5) div:nth-child(2) div:nth-child(7) div:nth-child(2)').text,
            'vertical_speed': soup.select_one(
                '#app div:nth-child(4) div:nth-child(2) div div:nth-child(2) div:nth-child(5) div:nth-child(2) div:nth-child(6) div:nth-child(2)').text,
        }

        print(data)

        return data
    except AttributeError:
        print('Error: Unable to parse data from HTML')
        return None


class DatabaseManager:
    insert_query = """
        INSERT INTO flight_data (country, aircraft_model, longitude, latitude, altitude, horizontal_speed, heading, vertical_speed)
        VALUES (%(country)s, %(aircraft_model)s, %(longitude)s, %(latitude)s, %(altitude)s, %(horizontal_speed)s, %(heading)s, %(vertical_speed)s)
    """

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def create_database(self):
        conn = pymysql.connect(
            host="localhost",
            user=self.user,
            password=self.password
        )

        cursor = conn.cursor()

        create_database_query = f"CREATE DATABASE IF NOT EXISTS {self.database}"

        cursor.execute(create_database_query)

        cursor.close()
        conn.close()
        print(f"数据库创建成功: {self.database}")

    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        conn = pymysql.connect(
            host="localhost",
            user=self.user,
            password=self.password,
            database=self.database
        )

        cursor = conn.cursor()

        create_table_query = """
            CREATE TABLE IF NOT EXISTS flight_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                country VARCHAR(255),
                aircraft_model VARCHAR(255),
                longitude VARCHAR(255),
                latitude VARCHAR(255),
                altitude VARCHAR(255),
                horizontal_speed VARCHAR(255),
                heading VARCHAR(255),
                vertical_speed VARCHAR(255)
            )
        """

        cursor.execute(create_table_query)
        conn.commit()

        cursor.close()
        conn.close()

        print("数据表格创建成功: flight_data")

    def insert_data(self, data):
        conn = pymysql.connect(
            host="localhost",
            user=self.user,
            password=self.password,
            database=self.database
        )

        cursor = conn.cursor()

        insert_query = """
            INSERT INTO flight_data(country, aircraft_model, longitude, latitude, altitude, horizontal_speed, heading, vertical_speed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(DatabaseManager.insert_query, data)

        data1 = (data['country'], data['aircraft_model'], data['longitude'], data['latitude'], data['altitude'], data['horizontal_speed'], data['heading'], data['vertical_speed'])

        cursor.execute(insert_query, data1)

        conn.commit()
        cursor.close()
        conn.close()

        print("数据插入成功！！！")

    def visualize_horizontal_speed(self):
        # 连接到数据库
        self.connect()

        # 获取游标对象
        cursor = self.conn.cursor()

        # 查询水平速度和键数据
        query = "SELECT horizontal_speed, id FROM flight_data"
        cursor.execute(query)

        # 获取查询结果
        result = cursor.fetchall()

        # 提取水平速度和键数据
        horizontal_speeds = []
        keys = []
        for row in result:
            if row[0]:
                horizontal_speeds.append(float(row[0].split()[0]))
                keys.append(row[1])

        # 关闭游标
        cursor.close()

        # 关闭数据库连接
        self.disconnect()

        # 绘制水平速度和键的条形图
        plt.bar(keys, horizontal_speeds)
        plt.xlabel('Keys')
        plt.ylabel('Horizontal Speed')
        plt.title('Bar Chart of Horizontal Speed by Keys')
        plt.show()


def show_table_data(host, user, password, database, table_name):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor()

    # 执行查询语句
    cursor.execute(f"SELECT * FROM {table_name}")

    # 获取查询结果
    rows = cursor.fetchall()

    # 打印每行数据
    for row in rows:
        print(row)

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


if __name__ == '__main__':
    # 创建 DatabaseManager 实例
    db_manager = DatabaseManager('localhost', "root", "Lxy001100!", "flight_data")

    # 创建数据库
    db_manager.create_database()

    # 创建表格
    db_manager.create_table()

    # 调用函数，并传入数据库连接信息和表名
    show_table_data("localhost", "root", "Lxy001100!", "flight_data", "flight_data")

    # 要插入的数据
    login_and_scrape_flight_data(db_manager)

    # 可视化垂直数据
    # db_manager.visualize_horizontal_speed()
    db_manager.visualize_horizontal_speed()
    # visualize_horizontal_speed(db_manager)







