# -*- coding: utf-8 -*-
import scrapy
import foodmate_scrapy.settings as settings
import logging
import datetime


class FootmateSpider(scrapy.Spider):
    name = 'footmate'
    #allowed_domains = ['footmate']
    start_urls = ['http://db.foodmate.net/choujian']

    def __init__(self, *args, **kwargs):
        super(FootmateSpider, self).__init__(*args, **kwargs)
        self.config = kwargs.get('config')

        dt = datetime.datetime.strptime(
            self.config['params']['timebegin'], "%Y-%m-%d")
        self.timeend = (dt + datetime.timedelta(days=(self.config['params']['addDay']-1))).strftime("%Y-%m-%d")
        self.url = 'http://db.foodmate.net/choujian/?kw={}&catidname={}&hege={}&xmfl1={}&shangbiao=&scname=&cyname=&jibie={}&zfid=&timebegin={}&timeend={}&submit1=%E6%9F%A5%E8%AF%A2&&page={}'
        self.targetUrl = self.url.format(self.config['params']['kw'], self.config['params']['catidname'], self.config['params']['hege'], self.config['params']
                                         ['xmfl1'], self.config['params']['jibie'], self.config['params']['timebegin'], self.timeend, self.config['params']['page'])
        self.start_urls = [self.targetUrl]

    def parse(self, response):
        totalPage = 1
        try:
            # // 全局 ./当前节点
            table = response.xpath('//table[@bordercolordark]')[0]
            #最后一个<b>标签的内容
            totalPage = response.xpath('//b[last()]/text()').extract_first()
            # totalPage = last_td[-1].xpath('./b[2]/text()').extract_first()
            tr_list = table.xpath('./tr')
            logging.info("Reponse totalPage:"+str(totalPage)+" ,reponse page:" + str(self.config['params']['page'])+", data size:"+str(len(tr_list)-1) + " in condition,catidname:" +
                         self.config['params']['catidname'] + ",hege=" + self.config['params']['hege'] + ",time:" + self.config['params']['timebegin'] + "-" + self.timeend)
            header = []
            count = 1
            for tr_ele in tr_list:
                if count > 1:
                    item = {}
                    item['信息来源'] = self.config['信息来源']
                    # item['网站'] = 'http://db.foodmate.net' + \
                    # tr_ele.xpath('td[7]/a/@href').extract_first()
                    item['搜索条件'] = self.config['搜索条件']
                    # 产品名称
                    item['物料名称'] = tr_ele.xpath(
                        'td[2]/text()').extract_first()
                    # 产品分类
                    item['产品分类'] = tr_ele.xpath(
                        'td[1]/text()').extract_first()
                    # 生产日期/通报编号/Reference
                    item['生产日期'] = tr_ele.xpath(
                        'td[6]/text()').extract_first()
                    # 生产企业/Subject
                    item['生产商'] = tr_ele.xpath(
                        'td[3]/text()').extract_first()
                    # 通报单位
                    item['发布单位'] = tr_ele.xpath(
                        'td[4]/text()').extract_first()
                    item['发布单位'] = "国内监督抽查("+str(item['发布单位'])+")"
                    # # 抽检结果
                    # item['抽检结果'] = tr_ele.xpath(
                    #     'td[5]/text()').extract_first()
                    # # 具体链接
                    item['网站'] = 'http://db.foodmate.net' + \
                        tr_ele.xpath('td[7]/a/@href').extract_first()

                    # 单位需要提取
                    item['单位'] = ''
                    item['批号'] = ''
                    item['项目分类'] = ''
                    item['备注'] = ''
                    yield scrapy.Request(item['网站'], self.parseDetail, meta=item)
                count = count + 1
        except Exception as e:
            print(e)
            print('行号', e.__traceback__.tb_lineno)
        self.config['params']['page'] = self.config['params']['page'] + 1
        if self.config['params']['page'] <= int(totalPage):
            targetUrl = self.url.format(
                self.config['params']['kw'], self.config['params']['catidname'], self.config['params']['hege'], self.config['params']['xmfl1'], self.config['params']['jibie'], self.config['params']['timebegin'], self.timeend, self.config['params']['page'])
            yield scrapy.Request(targetUrl, self.parse)
        else:
            dt = datetime.datetime.strptime(self.timeend, "%Y-%m-%d")
            dt_end = datetime.datetime.strptime(
                self.config['params']['scrapy_end_time'], "%Y-%m-%d")
            if(dt < dt_end):
                self.config['params']['timebegin'] = (
                    dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                self.timeend = (dt + datetime.timedelta(days=(self.config['params']['addDay']))
                                ).strftime("%Y-%m-%d")
                self.config['params']['page'] = 1
                targetUrl = self.url.format(
                    self.config['params']['kw'], self.config['params']['catidname'], self.config['params']['hege'], self.config['params']['xmfl1'], self.config['params']['jibie'], self.config['params']['timebegin'], self.timeend, self.config['params']['page'])
                yield scrapy.Request(targetUrl, self.parse)

    def parseDetail(self, response):
        item = response.meta
        table = response.xpath('//table')[0]
        tr_list = table.xpath('./tr')
        for tr_ele in tr_list:
            label = tr_ele.xpath('td[1]/text()').extract_first()
            value = tr_ele.xpath('td[2]/text()').extract_first()
            if label == '伙伴网链接':
                value = tr_ele.xpath('td[2]/a/@href').extract_first()

            if label == '产品分类':
                item[label] = value

            if label == '产品名称':
                item['物料名称'] = value

            if label == '通报文号':
                item[label] = value

            if label == '规格':
                item['规格型号'] = value

            if label == '商标':
                item[label] = value

            if label == '生产企业名称':
                item['生产商'] = value

            if label == '生产企业地址':
                item[label] = value

            if label == '被抽样企业名称':
                item['供应商'] = value

            if label == '被抽样企业地址':
                item[label] = value

            if label == '通报单位':
                item[label] = value

            if label == '通报省份':
                item[label] = value

            if label == '通报时间':
                item['发布日期'] = value

            if label == '不合格原因':
                item['检测项目'] = value

            if label == '检测结果':
                item[label] = value
                # 截取单位
                item['单位'] = ''

            if label == '标准/法规限值':
                item['限量值'] = value

            if label == '措施':
                item[label] = value

            if label == '判定结果':
                item['判定'] = value

            if label == '备注':
                item[label] = value

            if label == '伙伴网链接':
                item[label] = value

            if label == '抽检层级':
                item[label] = value
        # 返回给pipelines.py 处理 需要判断是哪个item
        yield item
