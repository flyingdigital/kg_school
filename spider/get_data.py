import json
import os.path
import time
from hyper.contrib import HTTP20Adapter
import requests


class SchoolInfoSpider:
    def __init__(self):
        # school_code.json文件地址
        self.schoolCodeUrl = "https://static-data.gaokao.cn/www/2.0/school/school_code.json"

        # school_url.json 本地存储路径
        self.schoolCodeLocalPath = "../data/school_code.json"
        self.parsedSchoolCodeLocalPath = "../data/parsed/parsed_school_code.json"
        self.specialDir = "../data/special"
        self.parsedDir = "../data/parsed"

    def getSchoolCodeInfo(self):
        # 获取 school_code.json
        response = requests.get(url=self.schoolCodeUrl)

        print("获取school_code状态码" + str(response.status_code))
        if response.status_code == 200:
            # 查看 data目录存不存在 不存在就创建
            if not os.path.exists('../data'):
                os.mkdir('../data')

            with open(self.schoolCodeLocalPath, 'wb') as f:
                f.write(response.content)
                print("获取school_code.json文件成功")

    def parseSchoolCode(self):
        # 解析school_code.json文件  将解析出来的值存入 data/parse/parsed_school_code.json中
        school_code = []

        # 查看 data/parsed 目录存不存在 不存在就创建
        if not os.path.exists(self.parsedDir):
            os.mkdir(self.parsedDir)

        with open(self.schoolCodeLocalPath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for k, v in data['data'].items():
                school_code.append(v)

        # 将解析后的数据持久化
        with open(self.parsedSchoolCodeLocalPath, 'w', encoding='utf-8') as f:
            json.dump(school_code, f)

        return school_code

    def getSchoolSpecial(self):
        # 获取学校专业信息

        data = []
        with open(self.parsedSchoolCodeLocalPath, 'r', encoding='utf-8') as file:
            data += (json.load(file))

        # 查看 data/parsed 目录存不存在 不存在就创建
        if not os.path.exists(self.specialDir):
            os.mkdir(self.specialDir)

        # 循环遍历学校专业信息
        for item in data:
            print(item)
            fileName = '../data/special/{}.json'.format(item['school_id'])
            url = 'https://static-data.gaokao.cn/www/2.0/school/{}/pc_special.json'.format(item['school_id'])
            response = requests.get(url=url)

            with open(fileName, 'wb') as f:
                f.write(response.content)

            time.sleep(1)

    def getSchoolBaseInfoByHtml(self):
        # 通过界面解析获取学校基本信息
        data = []
        with open(self.parsedSchoolCodeLocalPath, 'r', encoding='utf-8') as file:
            data += (json.load(file))

        schoolInfoList = []
        # 循环遍历学校专业信息
        for item in data:
            print(item)
            schoolInfo = {"school_code": item['school_id'], "school_name": item['name']}
            url = "https://www.gaokao.cn/school/{}/introDetails".format(item['school_id'])
            response = requests.get(url)

            # 学校所在城市

            # 学校详细地址

            # 学校主管部门

            # 学校建校时间

            # 学校占地面积

            # 学校介绍

            # 学校招生电话

            # 学校官网地址

            # 学校电子邮箱

if __name__ == '__main__':

    pass