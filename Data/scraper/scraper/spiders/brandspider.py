import scrapy
from scraper.items import ScraperItem

import json
import requests

class BrandSpider(scrapy.Spider):
  name = 'brandy'
  start_urls = ['https://firststop.sos.nd.gov/search/business']

  headers_2 = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "undefined",
    "cache-control": "no-cache",
    "cookie": "ASP.NET_SessionId=3l0aobjs2y0swvvtia5tew5n",
    "dnt": "1",
    "pragma": "no-cache",
    "referer": "https://firststop.sos.nd.gov/search/business",
    "sec-ch-ua": "'Not?A_Brand';v='8', 'Chromium';v='108', 'Google Chrome';v='108'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36:"
  }

  def parse(self, response):
    url_1 = 'https://firststop.sos.nd.gov/api/Records/businesssearch'
    formdata_1 = {"SEARCH_VALUE": "X", "STARTS_WITH_YN": "true", "ACTIVE_ONLY_YN": "false"}
    
    headers_1 = {
      "content-type": "application/json"
    }

    request = scrapy.Request(url=url_1,callback = self.parse_api, method = 'POST',headers = headers_1,body=json.dumps(formdata_1))

    yield request
  
  def parse_api(self, response):
    jsonResponse = json.loads(response.text)
    base_url = "https://firststop.sos.nd.gov/api/FilingDetail/business/"
    url_tail = "/false"
    data = jsonResponse['rows']

    #for loop iterating through the list of companies
    for company in data:
      item=ScraperItem()
      item['ID'] = company
      item['Name'] = data[company]['TITLE'][0]
      
      info_url = base_url + company + url_tail
      request = scrapy.Request(info_url, callback=self.parse_company, method = 'GET', headers=self.headers_2, meta={"item": item})
 
      yield request

  # Need to grab Commercial Registered Agent, Registered Agent, and/or Owners
  def parse_company(self, response):
    jsonResponse = json.loads(response.text)
    
    #set default values for Commercial Registered Agent, Registered Agent, and Owners
    CRA = 0
    RA = 0
    Owner = 0

    #loop through details for each company, and save value if a label is related to owner name or registered agent
    for detail in jsonResponse['DRAWER_DETAIL_LIST']:
      if detail['LABEL'] == "Owner Name":
        Owner = detail['VALUE']
      elif detail['LABEL'] == "Commercial Registered Agent":
        CRA = detail['VALUE']
      elif detail['LABEL'] == "Registered Agent":
        RA = detail['VALUE']


    #yield CRA, RA and Owner
    #return {
    item = response.meta["item"]
    item['Commercial_Registered_Agent'] = CRA
    item['Registered_Agent'] = RA
    item['Owner'] = Owner
    yield item
