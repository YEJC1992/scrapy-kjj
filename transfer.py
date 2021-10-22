import foodmate_scrapy.csv_helper as csv_helper
import csv
import os
# https://github.com/lushan88a/google_trans_new
from google_trans_new import google_translator

aim_lang = 'zh-CN'


def transferToZhCn(originalCsvPath, transferCsvPath):
    if os.path.exists(transferCsvPath):
        os.remove(transferCsvPath)

    translate = google_translator(timeout=10)
    header = ["搜索条件", "物料名称", "产品分类", "生产商", "供应商", "生产日期",
              "批号", "项目分类", "检测项目", "单位", "检测结果", "限量值", "判定", "发布单位", "发布日期", "备注"]
    csv_helper.createCsv(transferCsvPath, header)
    f_new = open(transferCsvPath, 'a+', encoding='utf-8', newline='')
    csv_writer = csv.writer(f_new)

    f = open(originalCsvPath, "r", encoding='utf-8')
    reader = csv.reader(f)
    i = 0
    for row in reader:
        if i > 0:
            new_row = []
            # ['判定', '产品分类', '项目分类', '检测项目'] [13,3,8,9]
            for i in range(0, 17):
                text = row[i]
                if i in [13, 3, 8, 9] and row[0] == 'RASFF':
                    if(text != None and text != ''):
                        targetText = translate.translate(text, aim_lang)
                        print(text+"=>"+targetText)
                        text = targetText
                new_row.append(text)
            csv_writer.writerow(new_row)
        i = i + 1

    f_new.close
    f.close


# text = 'undecided'
# # #text = "Zaatar"
# translate = google_translator(timeout=10)
# translate_text = translate.translate(text,  lang_tgt='zh-CN')
# print(translate_text)

# transferToZhCn('20210729160343.csv','20210729160343_trans.csv')
# print("Finish")
