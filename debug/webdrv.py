#coding=utf-8

from selenium import webdriver
import time

#browser = webdriver.Chrome()
#browser = webdriver.Firefox("C:/Python27/")
browser = webdriver.Firefox()

browser.get('http://stock.qq.com/data/#lhb')


#print u"浏览器最大化"
#browser.maximize_window()  #将浏览器最大化显示
time.sleep(1)

browser.switch_to.frame('moduleIframe')
browser.find_element_by_id('beginDate').send_keys('2017-06-19')
browser.find_element_by_id('endDate').send_keys('2017-06-20')
browser.find_element_by_xpath('/html/body/div[3]/div[2]/input[6]').click()
time.sleep(2)
