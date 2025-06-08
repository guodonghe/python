#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import base64
import time
import httplib
import json
##是否需要重新调整默认分片数量：True代表调整，False代表依照老索引配置，
SET_SHARDS_NUM_YOUSELF = False
DEFAULT_PRIMARY = 3    ##节点数量的倍数，每个索引size不大于20G-50G
DEFAULT_REPLICAS = 1

## 源集群host。
oldClusterHost = "100.66.44.200:8200"
## 源集群用户名，可为空。
oldClusterUserName = "superuser"
## 源集群密码，可为空。
oldClusterPassword = "xxxxx"
## 目标集群host，可在Elasticsearch实例的基本信息页面获取。
newClusterHost = "100.66.56.140:8200"
## 目标集群用户名。
newClusterUser = "superuser"
## 目标集群密码。
newClusterPassword = "xxxxx"

def httpRequest(method, host, endpoint, params="", username="", password=""):
    conn = httplib.HTTPConnection(host)
    headers = {}
    if (username != "") :
        'Hello {name}, your age is {age} !'.format(name = 'Tom', age = '20')
        base64string = base64.encodestring('{username}:{password}'.format(username = username, password = password)).replace('\n', '')
        headers["Authorization"] = "Basic %s" % base64string;
    if "GET" == method:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        conn.request(method=method, url=endpoint, headers=headers)
    else :
        headers["Content-Type"] = "application/json"
        conn.request(method=method, url=endpoint, body=params, headers=headers)
    response = conn.getresponse()
    res = response.read()
    return res
def httpGet(host, endpoint, username="", password=""):
    return httpRequest("GET", host, endpoint, "", username, password)
def httpPost(host, endpoint, params, username="", password=""):
    return httpRequest("POST", host, endpoint, params, username, password)
def httpPut(host, endpoint, params, username="", password=""):
    return httpRequest("PUT", host, endpoint, params, username, password)

def getTemplatesName(host, username="", password=""):
    endpoint = "/_cat/templates"
    TemplateResult = httpGet(oldClusterHost, endpoint, oldClusterUserName, oldClusterPassword)
    print("原始模版数据：" + TemplateResult)
    TemplateList = TemplateResult.split("\n")
    indexList = []
    for template in TemplateList:
        if template.split(" ")[0] != "":
            oldTemplateName = template.split(" ")[0]
            if getTemplate(oldTemplateName, oldClusterHost, oldClusterUserName, oldClusterPassword) != "wrong":
                indexList.append(template.split(" ")[0])
                print("获取到的模版名称是：" + template.split(" ")[0] + "\n")
            else:
                print("获取到的模版：是空模版，进行忽略操作！")
    return indexList
def getTemplate(templatename, host, username="", password=""):
    endpoint = "/_template/" + templatename
    TemplateContent = httpGet(host, endpoint, username, password)
    print (templatename + " 原始mapping如下：\n" + TemplateContent)
    if TemplateContent != '{}':
        TemplateMapping = json.loads(TemplateContent)
        if "lifecycle" in TemplateMapping[templatename]["settings"]["index"]: 
            del TemplateMapping[templatename]["settings"]["index"]["lifecycle"]
        mappings = json.dumps(TemplateMapping[templatename])
        print (templatename + " 处理后的mapping如下：\n" + mappings)
        return mappings
    print("空数据，直接反馈wrong!")
    return "wrong"
def createTemplate(oldTemplateName, newTemplateName=""):
    if (newTemplateName == "") :
        newTemplateName = oldTemplateName
    endpoint = "/_template/" + newTemplateName
    createstatement = getTemplate(oldTemplateName, oldClusterHost, oldClusterUserName, oldClusterPassword)
    print ("设置新集群的模版名字：" + newTemplateName + " 模版内容如下：\n" + createstatement)
    createTemplateResult = httpPut(newClusterHost, endpoint, createstatement, newClusterUser, newClusterPassword)
    print ("新集群模版创建完成：" + newTemplateName + " 创建结果：" + createTemplateResult)
    ctreatRep = json.loads(createTemplateResult)
    if "status" in ctreatRep : 
        return ctreatRep["status"]
    else:
        return 200


def getIndices(host, username="", password=""):
    endpoint = "/_cat/indices"
    indicesResult = httpGet(oldClusterHost, endpoint, oldClusterUserName, oldClusterPassword)
    indicesList = indicesResult.split("\n")
    indexList = []
    for indices in indicesList:
        if (indices.find("open") > 0):
            indexList.append(indices.split()[2])
    return indexList

    ## 分开去取seting和mapping数据不全面，一起取回相关数据，如果需要手动调整分片、副本
def getIndexMetaData(index, host, username="", password=""):
    endpoint = "/" + index
    indexSettings = httpGet(host, endpoint, username, password)
    print (index + "  原始索引的配置信息如下：\n" + indexSettings)
    FullsettingsDict = json.loads(indexSettings)
    settingsDict = FullsettingsDict[index]
    del settingsDict["settings"]["index"]["creation_date"]
    del settingsDict["settings"]["index"]["provided_name"]
    del settingsDict["settings"]["index"]["uuid"]
    del settingsDict["settings"]["index"]["version"]
    if "lifecycle" in settingsDict["settings"]["index"]: 
        del settingsDict["settings"]["index"]["lifecycle"]
    if SET_SHARDS_NUM_YOUSELF :
        settingsDict["settings"]["index"]["number_of_shards"] = DEFAULT_PRIMARY
        settingsDict["settings"]["index"]["number_of_replicas"] = DEFAULT_REPLICAS
    SettingsAndMapping = json.dumps(settingsDict)
    print (index + "  处理后的索引配置信息如下：\n" + SettingsAndMapping)
    return SettingsAndMapping
def createIndex(oldIndexName, newIndexName=""):
    if (newIndexName == "") :
        newIndexName = oldIndexName
    createstatement = getIndexMetaData(oldIndexName, oldClusterHost, oldClusterUserName, oldClusterPassword)
    print ("老索引 " + newIndexName + " 的setting和mapping如下：\n" + createstatement)
    endpoint = "/" + newIndexName
    createResult = httpPut(newClusterHost, endpoint, createstatement, newClusterUser, newClusterPassword)
    print ("新索引 " + newIndexName + " 创建结果：" + createResult)
    ctreatRep = json.loads(createResult)
    if "acknowledged" in ctreatRep:
        return 200
    else:
        return ctreatRep["status"]

def main1_MigIndexMeta():
    successNum = 0
    failureNum = 0
    indexList = getIndices(oldClusterHost, oldClusterUserName, oldClusterPassword)
    systemIndex = []
    for index in indexList:
        if (index.startswith(".")):
            systemIndex.append(index)
        else :
            if createIndex(index, index) == 200:
                successNum = successNum + 1 
            else:
                failureNum = failureNum + 1
    if (len(systemIndex) > 0) :
        for index in systemIndex:
            print (index + " 或许是系统索引，不会重新创建，如有需要，请单独处理～")
    print("\n迁移成功索引数量： " + str(successNum) + "\n迁移失败索引数量： " + str(failureNum))   

def main2_MigTemplates():
    successNum = 0
    failureNum = 0
    templatesList = getTemplatesName(oldClusterHost, oldClusterUserName, oldClusterPassword)
    systemTemplates = []
    for template in templatesList:
        if (template.startswith(".")):
            systemTemplates.append(template)
        else:
            if createTemplate(template, template) == 200:
                successNum = successNum + 1
            else:
                failureNum = failureNum + 1
    if (len(systemTemplates) > 0) :
        for template2 in systemTemplates:
            print (template2 + " 或许是系统模版，不会重新创建模版，如有需要，请单独处理～") 
    print("\n迁移成功模版数量： " + str(successNum) + "\n迁移失败模版数量： " + str(failureNum))
            
## main1
main1_MigIndexMeta() # 迁移索引meta数据：包括setting、mapping、allias，并创建空索引；默认.开头的索引是系统索引，不做迁移

## main2
main2_MigTemplates() # 迁移模版；默认.开头的模版是系统模版，不做迁移
