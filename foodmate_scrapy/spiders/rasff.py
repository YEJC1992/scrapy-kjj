import configparser
import scrapy
import json


class RasffSpider(scrapy.Spider):
    name = 'rasff'
    start_urls = [
        'https://webgate.ec.europa.eu/rasff-window/backend/public/notification/search/consolidated/']

    def __init__(self, *args, **kwargs): 
        self.test = '====test'
        super(RasffSpider, self).__init__(*args, **kwargs)
        print("====RasffSpider Init=====")
        self.config = kwargs.get('config')

    # for post
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, method="POST", headers={'Content-Type': 'application/json', 'Origin': 'https://webgate.ec.europa.eu', 'Referer': 'https://webgate.ec.europa.eu/rasff-window/screen/list', 'Host': 'webgate.ec.europa.eu', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'}, body=json.dumps(self.config['post']), callback=self.parse)

    def parse(self, response):
        repJson = json.loads(response.text)
        notifications = repJson['notifications']
        totalPages = repJson['totalPages']
        totalElements = repJson['totalElements']
        print("Rasff total page:"+str(totalPages)+",total element:"+str(totalElements)+",search page num:" + str(self.config['post']['parameters']['pageNumber']))
        
        for notification in notifications:
            item = {}
            item['信息来源'] = self.config['信息来源']
            item['发布单位'] = self.config['信息来源']
            item['发布单位'] = "国外预警("+str(item['发布单位'])+")"
            item['搜索条件'] = self.config['搜索条件']
            item['判定'] = notification['riskDecision']['description']
            item['发布日期'] = notification['ecValidationDate']
            detailUrl = "https://webgate.ec.europa.eu/rasff-window/backend/public/notification/view/id/" + \
                str(notification['notifId'])+"/"
            yield scrapy.Request(url=detailUrl, meta=item, method="GET", headers={'Origin': 'https://webgate.ec.europa.eu', 'Referer': 'https://webgate.ec.europa.eu/rasff-window/screen/list', 'Host': 'webgate.ec.europa.eu', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'}, callback=self.parseDetail)
        self.config['post']['parameters']['pageNumber'] = self.config['post']['parameters']['pageNumber'] +1
        if self.config['post']['parameters']['pageNumber'] <= totalPages:
            yield scrapy.Request(url='https://webgate.ec.europa.eu/rasff-window/backend/public/notification/search/consolidated/', method="POST", headers={'Content-Type': 'application/json', 'Origin': 'https://webgate.ec.europa.eu', 'Referer': 'https://webgate.ec.europa.eu/rasff-window/screen/list', 'Host': 'webgate.ec.europa.eu', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'}, body=json.dumps(self.config['post']), callback=self.parse)

    def parseDetail(self, response):
        item = response.meta
        repJson = json.loads(response.text)
        item['批号'] = repJson['reference']
        item['产品分类'] = repJson['product']['productCategory']['description']
        if 'description' in repJson['product']:
            item['物料名称'] = repJson['product']['description']
        if 'hazards' in repJson['product']:
            hazards = repJson['product']['hazards']
            for hazardsItem in hazards:
                item['项目分类'] = hazardsItem['hazardCategory']['description']
                item['检测项目'] = hazardsItem['name']
                if 'analyticalResult' in hazardsItem:
                    item['检测结果'] = hazardsItem['analyticalResult']
                if 'unit' in hazardsItem:
                    item['单位'] = hazardsItem['unit']
                if 'maxPermittedLvl' in hazardsItem:
                    item['限量值'] = hazardsItem['maxPermittedLvl']
                yield item
        else:
            yield item