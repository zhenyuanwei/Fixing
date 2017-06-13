from app.model import getCollection
from app.utils.util import getTimeStamp
from app.utils.util import getTime

'''
报修Plus的数据模型
issue_id             #报修问题编号
license_num          #版权编号  标记这个属于哪个公司
issue_name           #报修问题标题
issue_expect_time    #期待完成时间
issue_company        #报修单位
issue_address        #地址
tel_no               #联系方式
request_openId       #报修发起者openId
nickname             #报修发起者微信昵称
issue_description    #报修问题描述
issue_status         #状态 0 取消，9完成，1申请中
logs                 #处理log，List对象，每个元素都是字典类型
    openId           #处理者的openId
    nickname         #处理人微信昵称
    description      #处理方式
    create_time      #处理时间
create_time          #自动设定
update_time          #自动设定
'''
class IssueModel:
    __collectionName = 'issue_collection'
    __default_key = {'issue_status': {'$in': ['1']}}

    def insert(self, issue):
        issue_id = getTimeStamp()
        issue['issue_id'] = issue_id
        issue['create_time'] = getTime()
        issue['update_time'] = getTime()
        issue['issue_status'] = '1'
        issue['logs'] = [{'openId': issue['request_openId'],
                          'nickname': issue['nickname'],
                          'description': '发起申请',
                          'create_time': getTime()}]
        issue_collection = getCollection(collectionName=self.__collectionName)
        issue_collection.insert(issue)
        return issue_id

    def finds(self):
        issue_collection = getCollection(collectionName=self.__collectionName)
        issueList = issue_collection.find()
        return issueList

    def findByOpenId(self, request_openId):
        issue_collection = getCollection(collectionName=self.__collectionName)

        query_key = {'request_openId': request_openId}
        query_condition = {'$and': [self.__default_key, query_key]}
        issueList = issue_collection.find(query_condition)
        return issueList

    def findByLicense(self, license_num):
        issue_collection = getCollection(collectionName=self.__collectionName)

        query_key = {'license_num': license_num}
        query_condition = {'$and': [self.__default_key, query_key]}
        issueList = issue_collection.find(query_condition)
        return issueList

    def findByIssueId(self, issue_id):
        issue_collection = getCollection(collectionName=self.__collectionName)
        query_key = {'issue_id': issue_id}
        issue = issue_collection.find_one(query_key)
        return issue

    def update(self, issue):
        issue_collection = getCollection(collectionName=self.__collectionName)
        issue_id = issue['issue_id']
        issue['update_time'] = getTime()
        for key in issue:
            if key != 'issue_id' and key != '_id':
                issue_collection.update({'issue_id': issue_id}, {'$set': {key: issue[key]}})
        return issue
    def removeAll(self):
        issue_collection = getCollection(collectionName=self.__collectionName)
        issue_collection.remove()

'''
报修Plus工程师数据模型
openId               #工程师的openId
engineer_id          #工程师的Id
license_num          #版权编号  标记这个属于哪个公司
engineer_name        #工程师姓名
tel_no               #联系方式
type                 # 01 调度员， 02工程师
nickname             #工程师的微信昵称
flag                 # 1 有效，0 无效
create_time          #自动设定
update_time          #自动设定
'''
class EngineerModel:
    __collectionName = 'engineer_collection'
    default_key = {'flag': {'$in': ['1']}}

    def insert(self, engineer):
        engineer_id = getTimeStamp()
        engineer['engineer_id'] = engineer_id
        engineer['create_time'] = getTime()
        engineer['update_time'] = getTime()
        engineer['flag'] = '1'
        engineer['openId'] = ''
        engineer['nickname'] = ''
        engineer_collection = getCollection(collectionName=self.__collectionName)
        engineer_collection.insert(engineer)
        return engineer_id

    def findByEngineerId(self, engineer_id):
        engineer_collection = getCollection(collectionName=self.__collectionName)
        query_key = {'engineer_id': engineer_id}
        query_condition = {'$and': [self.default_key, query_key]}
        engineer = engineer_collection.find_one(query_condition)
        return engineer

    def findByOpenId(self, openId):
        engineer_collection = getCollection(collectionName=self.__collectionName)
        query_key = {'openId': openId}
        query_condition = {'$and': [self.default_key, query_key]}
        engineer = engineer_collection.find_one(query_condition)
        return engineer

    def findFocalByLicense(self, license_num):
        engineer_collection = getCollection(collectionName=self.__collectionName)
        license_key = {'license_num': license_num}
        type_key = {'type': '01'}
        query_condition = {'$and': [type_key, license_key, self.default_key]}
        engineer = engineer_collection.find_one(query_condition)
        return engineer

    def finds(self, license_num):
        engineer_collection = getCollection(collectionName=self.__collectionName)
        query_key = {'license_num': license_num}
        query_condition = {'$and': [self.default_key, query_key]}
        engineers = engineer_collection.find(query_condition)
        return engineers

    def removeAll(self):
        engineer_collection = getCollection(collectionName=self.__collectionName)
        engineer_collection.remove()

    def update(self, engineer):
        engineer_collection = getCollection(collectionName=self.__collectionName)
        engineer_id = engineer['engineer_id']
        engineer['update_time'] = getTime()
        for key in engineer:
            if key != 'engineer_id' and key != '_id' :
                engineer_collection.update({'engineer_id': engineer_id}, {'$set': {key: engineer[key]}})
        return self.findByEngineerId(engineer_id=engineer_id)
