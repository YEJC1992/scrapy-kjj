from foodmate_scrapy.spiders.footmate import FootmateSpider
from foodmate_scrapy.spiders.eshian import EshianSpider
from foodmate_scrapy.spiders.rasff import RasffSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import foodmate_scrapy.settings as settings
import datetime
import json
import transfer
import time
import foodmate_config
import eshian_config
import rasff_config

config = {
    'csv_source': "国内15年2月国外2020年2月"+datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".csv",
    'csv_format': "国内15年2月国外2020年2月"+datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "_format.csv",
}

with open('config.json', 'w') as f:
    json.dump(config, f)

time_str = "2015-02-01"
time_end = "2015-02-28"

time_str2 = "01-02-2020 00:00:00"
time_end2 = "28-02-2020 23:59:59"

process = CrawlerProcess(get_project_settings())


for config in foodmate_config.footmate_config:
    config['params']['timebegin'] = time_str
    config['params']['scrapy_end_time'] = time_end
    process.crawl(FootmateSpider, config=config)


for config in eshian_config.eshian_config:
    config['post']['releaseTime'] = time_str
    config['post']['releaseTime1'] = time_end
    config['post']['releaseTimeX'] = time_str
    config['post']['releaseTime1X'] = time_end
    process.crawl(EshianSpider, config=config)

for config in rasff_config.rasff_config:
    config['post']['ecValidDateFrom'] = time_str2
    config['post']['ecValidDateTo'] = time_end2
    process.crawl(RasffSpider, config=config)

# rasff_config.rasff_config[0]['post']['ecValidDateFrom'] = time_str2
# rasff_config.rasff_config[0]['ecValidDateTo'] = time_end2
# process.crawl(RasffSpider, config=rasff_config.rasff_config[0])

# process.crawl(EshianSpider, config=eshian_config.eshian_config2)
#process.crawl(RasffSpider, config=rasff_config.rasff_config_1)

process.start()

# 边爬边翻译 有缓存只能读到表头
# transfer.transferToZhCn(config['csv'],config['csv_transfer'])

print("Finish")
