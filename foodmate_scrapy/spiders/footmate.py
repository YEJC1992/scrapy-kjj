# -*- coding: utf-8 -*-
import scrapy
import foodmate_scrapy.settings as settings
import logging
import datetime


class FootmateSpider(scrapy.Spider):
    name = 'footmate'
    #allowed_domains = ['footmate']
    kw = settings.kw
    xmfl1 = settings.xmfl1
    jibie = settings.jibie
    catidname = settings.catidname
    hege = settings.hege
    timebegin = settings.timebegin
    dt = datetime.datetime.strptime(timebegin, "%Y-%m-%d")
    timeend = (dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    scrapy_end_time = settings.scrapy_end_time
    title = settings.title
    page = settings.page
    url = 'http://db.foodmate.net/choujian/?kw={}&catidname={}&hege={}&xmfl1={}&shangbiao=&scname=&cyname=&jibie={}&zfid=&timebegin={}&timeend={}&submit1=%E6%9F%A5%E8%AF%A2&&page={}'
    targetUrl = url.format(kw, catidname, hege, xmfl1, jibie, timebegin, timeend, page)
    start_urls = [targetUrl]

    def parse(self, response):
        totalPage = 1
        try:
            # // 全局 ./当前节点
            table = response.xpath('//table[@bordercolordark]')[0]
            last_td = response.xpath('//td[last()]')
            totalPage = last_td[-1].xpath('./b[2]/text()').extract_first()
            tr_list = table.xpath('./tr')
            logging.info("Reponse totalPage:"+str(totalPage)+" ,reponse page:" + str(self.page)+", data size:"+str(len(tr_list)-1) + " in condition,catidname:" +
                        self.catidname + ",hege=" + self.hege + ",time:" + self.timebegin + "-" + self.timeend)
            header = []
            count = 1
            for tr_ele in tr_list:
                if count > 1:
                    item = {}

                    item['信息来源'] = '中国监督抽查（食品伙伴网）'
                    item['网站'] = 'http://db.foodmate.net' + \
                    tr_ele.xpath('td[7]/a/@href').extract_first()
                    item['搜索条件']=self.title
                    # 产品名称
                    item['产品/Product'] = tr_ele.xpath(
                        'td[2]/text()').extract_first()
                    # 产品分类
                    item['产品分类/Product Category'] = tr_ele.xpath(
                        'td[1]/text()').extract_first()
                    item['规格型号'] = ''
                    # 生产日期/通报编号/Reference
                    item['生产日期/通报编号/Reference'] = tr_ele.xpath(
                        'td[6]/text()').extract_first()            
                    # 生产企业/Subject
                    item['生产企业/Subject'] = tr_ele.xpath(
                        'td[3]/text()').extract_first()
                    # 通报单位
                    item['发布单位/Notification from'] = tr_ele.xpath(
                        'td[4]/text()').extract_first()
                    # # 抽检结果
                    # item['抽检结果'] = tr_ele.xpath(
                    #     'td[5]/text()').extract_first()
                    # # 具体链接
                    # item['网站'] = 'http://db.foodmate.net' + \
                    #     tr_ele.xpath('td[7]/a/@href').extract_first()

                    #单位需要提取
                    item['单位/Unit'] = ''
                    # 返回给pipelines.py 处理 需要判断是哪个item
                    yield scrapy.Request(item['网站'], self.parseDetail, meta=item)
                count = count + 1
        except Exception as e:
            print(e)
            print('行号', e.__traceback__.tb_lineno)
        self.page = self.page + 1
        if self.page <= int(totalPage):
            targetUrl = self.url.format(
                self.kw, self.catidname, self.hege, self.xmfl1, self.jibie, self.timebegin, self.timeend, self.page)
            yield scrapy.Request(targetUrl, self.parse)
        else:
            dt = datetime.datetime.strptime(self.timeend, "%Y-%m-%d")
            dt_end = datetime.datetime.strptime(
                self.scrapy_end_time, "%Y-%m-%d")
            if(dt < dt_end):
                self.timebegin = (
                    dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                self.timeend = (dt + datetime.timedelta(days=2)
                                ).strftime("%Y-%m-%d")
                self.page = 1
                targetUrl = self.url.format(
                   self.kw, self.catidname, self.hege, self.xmfl1, self.jibie, self.timebegin, self.timeend, self.page)
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
                item[label] = value

            if label == '通报文号':
                item[label] = value

            if label == '规格':
                item['规格型号'] = value

            if label == '商标':
                item[label] = value

            if label == '生产企业名称':
                item[label] = value

            if label == '生产企业地址':
                item[label] = value

            if label == '被抽样企业名称':
                item[label] = value

            if label == '被抽样企业地址':
                item[label] = value

            if label == '通报单位':
                item[label] = value

            if label == '通报省份':
                item[label] = value

            if label == '通报时间':
                item['发布日期/Date of case'] = value

            if label == '不合格原因':
                item['不合格项（标准值）/Substance/Hazard'] = value

            if label == '检测结果':
                item['检验结果/Analytical Result'] = value

            if label == '标准/法规限值':
                item['标准值'] = value

            if label == '措施':
                item[label] = value

            if label == '判定结果':
                item[label] = value

            if label == '备注':
                item[label] = value

            if label == '伙伴网链接':
                item[label] = value

            if label == '抽检层级':
                item[label] = value
        yield item
