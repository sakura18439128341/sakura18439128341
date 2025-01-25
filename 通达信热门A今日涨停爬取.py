import playwright.async_api
import asyncio
from lxml import etree
import pymongo
#前置环境python3.10，playWright，pymongo，mongo数据库搭建，异步模块asynico
#导包
url2= 'https://pul.tdx.com.cn/site/app/gzhbd/tdx-topsearch/page-main.html?pageName=page_topsearch&tabClickIndex=0&subtabIndex=0'
#爬取网址
async def on_response(response):
    print(response.status)
#监听，可有可无
async def fetch(url):
    cilent1 = pymongo.MongoClient(host='localhost', port=27017)
    dp = cilent1.test
    collection = dp.money_scrapetest
    #导入mongo数据库，一般port都是27017，host因人而异
    number_list = [0,2,5]
    async with playwright.async_api.async_playwright() as session:
        fet =await session.firefox.launch()
        page = await fet.new_page()
        # page.on('response',on_response)
        await page.goto(url)
        await page.wait_for_load_state('networkidle')
        #等待页面完全响应
        response1 = await page.content()
        #爬取页面源代码
        html = etree.HTML(response1)
        for number in range(1,100):
            test_jige = {}
            base_mod = '/html/body/div[1]/div/div/div/div/div/div/div/div/div[2]/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div/div[{}]/div[3]/div[1]//text()'.format(number)
            #喜闻乐见的xpath解析
            result = html.xpath(base_mod)
            for i in number_list:
                # print(result[i])
                if i == 0:
                    test_jige["企业名称"] = result[i]
                elif i == 2:
                    test_jige["企业编号"] = result[i]
                elif i == 5:
                    test_jige["今日涨停"] = result[i]
            #剔除无关内容
            print(test_jige)
            result112 = collection.insert_one(test_jige)
            #导入mongo数据库，格式为dict
            print(result112)
loop =asyncio.get_event_loop()#异步运行ing
loop.run_until_complete(fetch(url2))
