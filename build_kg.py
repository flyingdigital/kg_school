import json
from py2neo import Graph, Node, NodeMatcher

import requests


class BuildKG:
    def __init__(self):
        self.con = Graph(
            "127.0.0.1:7474",
            auth=("neo4j", "mercury-chance-margo-door-leopard-6735")
        )
        self.matcher = NodeMatcher(self.con)
        self.specialDir = "./data/special"
        self.parsedSchoolCodeLocalPath = "./data/parsed/parsed_school_code.json"

    def createNode(self):
        data = []
        with open(self.parsedSchoolCodeLocalPath, 'r', encoding='utf-8') as file:
            data += json.load(file)

        specialInfoList = []

        for item in data:

            schoolCode = item['school_id']
            filePath = self.specialDir + '/' + str(schoolCode) + ".json"

            with open(filePath, 'r', encoding='utf-8') as f:
                temp = json.load(f)
            print(temp)
            try:
                specialDetailList = temp['data']['special_detail']['1']
                for specialDetail in specialDetailList:
                    specialInfo = {}
                    # 专业名称
                    specialInfo['special_name'] = specialDetail['special_name']
                    # 层次
                    specialInfo['type_name'] = specialDetail['type_name']
                    # 学科门类
                    specialInfo['level2_name'] = specialDetail['level2_name']
                    # 学制
                    specialInfo['limit_year'] = specialDetail['limit_year']
                    # 专业类别
                    specialInfoList.append(specialInfo)
            except:
                continue

            node = Node('学校', name=item['name'])
            self.con.create(node)

            for special in specialInfoList:
                if not self.matcher.match("专业名称", name=special['special_name']):
                    node = Node('专业名称', name=special['special_name'])
                    self.con.create(node)

                query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    '学校', '专业名称', item['name'], special['special_name'], '开放专业', 'open_professional')

                self.con.run(query)

            # break表示只构建一个
            # break

if __name__ == '__main__':
    b = BuildKG()
    b.createNode()
