import scrapy
import foodmate_scrapy.settings as settings
import math
import datetime


class EshianSpider(scrapy.Spider):
    name = 'eshian'
    #allowed_domains = ['eshian.com']

    #endTime = settings.releaseTime1

    start_urls = ['http://www.eshian.com/sat/foodsampling']

    def __init__(self, *args, **kwargs):
        super(EshianSpider, self).__init__(*args, **kwargs)
        self.config = kwargs.get('config')
        self.endTime = self.config['post']['releaseTime1']
        self.config["post"]["releaseTime1"] = (datetime.datetime.strptime(
            self.config["post"]["releaseTime"], "%Y-%m-%d") + datetime.timedelta(days=(int(self.config["post"]["addDay"])-1))).strftime("%Y-%m-%d")
        self.config["post"]["releaseTime1X"] = self.config["post"]["releaseTime1"]

    # for post
    def start_requests(self):
        for url in self.start_urls:
            print(self.config["post"])
            yield scrapy.FormRequest(url=url, formdata=self.config["post"], callback=self.parse)

    def parse(self, response):
        print(self.config["post"]["releaseTime"], self.config["post"]["releaseTimeX"],
              self.config["post"]["releaseTime1"], self.config["post"]["releaseTime1X"])
        allPage = 0
        presentPage = 1
        if(len(response.xpath('//em')) > 0):
            presentPage = int(response.xpath(
                '//em')[0].xpath('string(.)').extract()[0])
            totalRows = int(response.xpath('//em')
                            [1].xpath('string(.)').extract()[0])
            allPage = int(math.ceil(totalRows/20))
            table = response.xpath(
                '//table[@class="table table-data-show"]')[0]
            tbody = table.xpath('./tbody')[0]
            tr_list = tbody.xpath('./tr')
            for tr_ele in tr_list:
                item = {}
                item['信息来源'] = self.config['信息来源']
                item['搜索条件'] = self.config['搜索条件']
                item['物料名称'] = tr_ele.xpath(
                    './td')[0].xpath('string(.)').extract()[0]
                # item['规格型号'] = tr_ele.xpath(
                #     './td')[1].xpath('string(.)').extract()[0]
                item['生产日期'] = tr_ele.xpath(
                    './td')[2].xpath('string(.)').extract()[0]
                item['生产商'] = tr_ele.xpath(
                    './td')[3].xpath('string(.)').extract()[0]
                print("====>" + str(len(tr_ele.xpath('./td')[4].xpath('./table/tbody/tr'))))
                item['检测项目'] = ""
                item['检测结果'] = ""
                for tr2 in tr_ele.xpath('./td')[4].xpath('./table/tbody/tr'):
                    if item['检测项目'] == "":
                        item['检测项目'] = tr2.xpath('./td')[0].xpath('string(.)').extract()[0]
                    else:
                        item['检测项目'] = item['检测项目'] + ";" + tr2.xpath('./td')[0].xpath('string(.)').extract()[0]
                    if item['检测结果'] == "":
                        item['检测结果'] = tr2.xpath('./td')[1].xpath('string(.)').extract()[0]
                    else:
                        item['检测结果'] = item['检测结果'] + ";" + tr2.xpath('./td')[1].xpath('string(.)').extract()[0]
                #不合格项(标准值)
                # item['检测项目'] = tr_ele.xpath(
                #     './td')[4].xpath('./table/tbody/tr/td')[0].xpath('string(.)').extract()[0]
                #检验结果
                # item['检测结果'] = tr_ele.xpath(
                #     './td')[4].xpath('./table/tbody/tr/td')[1].xpath('string(.)').extract()[0]

                #限量值在 检测项目(不合格项(标准值))  提取
                item['限量值'] = ''
                
                #检查结果拆分单位
                item['单位'] = ''
                item['发布单位'] = tr_ele.xpath(
                    './td')[5].xpath('string(.)').extract()[0]
                item['判定'] = '不合格'
                item['发布单位'] = "国内监督抽查("+str(item['发布单位'])+")"
                item['发布日期'] = tr_ele.xpath(
                    './td')[6].xpath('string(.)').extract()[0]
                yield item
        if presentPage < allPage:
            self.config["post"]['pageNo'] = str(
                int(self.config["post"]['pageNo'])+1)
            yield scrapy.FormRequest(url=self.start_urls[0], formdata=self.config["post"], callback=self.parse)
        else:
            dt = datetime.datetime.strptime(
                self.config["post"]['releaseTime1'], "%Y-%m-%d")
            dt_end = datetime.datetime.strptime(
                self.endTime, "%Y-%m-%d")
            if(dt < dt_end):
                self.config["post"]["releaseTime"] = (
                    dt + datetime.timedelta(days=(1))).strftime("%Y-%m-%d")
                self.config["post"]["releaseTimeX"] = self.config["post"]["releaseTime"]
                self.config["post"]["releaseTime1"] = (
                    dt + datetime.timedelta(days=(int(self.config["post"]["addDay"])))).strftime("%Y-%m-%d")
                self.config["post"]["releaseTime1X"] = self.config["post"]["releaseTime1"]
                self.config["post"]['pageNo'] = "0"
                yield scrapy.FormRequest(url=self.start_urls[0], formdata=self.config["post"], callback=self.parse)
