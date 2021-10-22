# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import csv
import foodmate_scrapy.csv_helper as csv_helper
from google_trans_new import google_translator
import pandas as pd
import numpy as np
import time
import os
import datetime
import json
import re


class FoodmateScrapyPipeline(object):
    """ 
        功能：保存item数据 
    """

    def __init__(self):
        logging.info("Pipeline init...")

        json_f = open('config.json', 'r')
        config = json.load(json_f)

        print("Scrapt source output csv:"+config['csv_source']+",format csv:"+config['csv_format'])

        self.filename = config['csv_source']
        self.filename_format = config['csv_format']
        self.header = ["信息来源","搜索条件", "物料名称", "产品分类", "生产商", "供应商", "生产日期",
                       "批号", "项目分类", "检测项目", "单位", "检测结果", "限量值", "判定", "发布单位", "发布日期", "备注"]
        if os.path.exists(self.filename) == False:
            csv_helper.createCsv(self.filename, self.header)
        if os.path.exists(self.filename_format) == False:
            csv_helper.createCsv(self.filename_format, self.header)
        self.jy_file = open(self.filename, 'a+', encoding='utf-8', newline='')
        self.jy_file_format = open(self.filename_format, 'a+', encoding='utf-8', newline='')
        self.csv_writer = csv.writer(self.jy_file)
        self.csv_writer_format = csv.writer(self.jy_file_format)
        self.translate = google_translator(timeout=10)

    def process_item(self, item, spider):
        logging.info("Pipeline process_item...")
        #原始
        row = []
        #清洗后
        row_format = []
        needTransf = False
        if item['信息来源'] == 'RASFF':
            needTransf = True
        index = 0
        for col in self.header:
            if col in item:
                text = item[col]
                row.append(text)
                #需要翻译的字段
                if needTransf and text != None and text != '':
                   
                    if(col in ['物料名称','判定', '产品分类', '项目分类', '检测项目']):
                        errCount = 0
                        while(errCount < 10):
                            try:
                                text = self.translate.translate(text, lang_tgt='zh-CN')
                                break
                            except:
                                errCount = errCount + 1
                                print("Transfer "+col+":["+text+"] error")
                if item['信息来源'] == '食品伙伴网':
                    if col == '检测结果' and text != None and text != '':
                        num = re.findall(r'\d+\.*\d*',text)
                        if len(num) > 0:
                            orginalText = text
                            text = num[0]
                            #单位
                            row_format[len(row_format)-1] = orginalText.replace(num[0],'')
                if col == '发布日期':
                    text = text.split(" ")[0]

                row_format.append(text)
            else:
                row.append("")
                row_format.append("")
        index = index + 1
        self.csv_writer.writerow(row)
        self.csv_writer_format.writerow(row_format)
        return item

    def close_spider(self, spider):
        logging.info("Pipeline close...")
        self.jy_file.close
        self.jy_file_format.close
        # time.sleep(5)
        # csvf = pd.read_csv('调味品.csv', encoding='utf-8')
        # if os.path.isfile('调味品.xlsx') == True:
        #     os.remove('调味品.xlsx')
        # time.sleep(1)
        # csvf.to_excel('调味品.xlsx', sheet_name='data')
