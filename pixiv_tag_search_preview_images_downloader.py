from selenium import webdriver
from bs4 import BeautifulSoup
import time
import urllib.request
import getpass
import os

phantompath = r'C:\Users\Einsbon\Documents\Python_Projects\python_window\crawler\pixiv_low_quality_image_crawler\phantomjs.exe'
chromepath = 'C:\\Users\\Einsbon\\Documents\\Python Scripts\\crawler\\pixiv_low_quality_image_crawler\\chromedriver.exe'
urlVocaloid = r"https://www.pixiv.net/search.php?s_mode=s_tag_full&word=VOCALOID&type=illust&blt=100&mode=safe"
urlMiku = r'https://www.pixiv.net/search.php?s_mode=s_tag_full&word=%E5%88%9D%E9%9F%B3%E3%83%9F%E3%82%AF&type=illust&blt=100&mode=safe'
urlLogin = 'https://accounts.pixiv.net/login?lang=ko&source=pc&view_type=page&ref=wwwtop_accounts_index'


def driverSetup(web, userId, userpd, urlFirst):
    web.get(urlFirst)
    web.implicitly_wait(10)
    web.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div/form/div[1]/div[1]/input').send_keys(
        userId)
    web.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div/form/div[1]/div[2]/input').send_keys(
        userpd)
    web.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div/form/button').click()
    web.set_window_size(1020, 960)


def scrollUpToDown(web):
    web.execute_script("window.scrollTo(0, 400);")
    time.sleep(0.15)
    web.execute_script("window.scrollTo(0, 800);")
    time.sleep(0.15)
    web.execute_script("window.scrollTo(0, 1200);")
    time.sleep(0.15)
    web.execute_script("window.scrollTo(0, 1600);")
    time.sleep(0.15)
    web.execute_script("window.scrollTo(0, 2000);")
    time.sleep(0.15)
    web.execute_script("window.scrollTo(0, 2400);")
    time.sleep(0.15)
    web.execute_script("window.scrollTo(0, 2800);")
    time.sleep(0.15)
    web.execute_script("window.scrollTo(0, 3200);")


def crawling(web, repeatNum, savePath):
    while repeatNum > 0:
        print('\n\nNumber of pages remaining: ' + str(repeatNum))
        print('Current_url:' + str(web.current_url))
        scrollUpToDown(web)
        web.implicitly_wait(20)

        html = web.page_source
        soup = BeautifulSoup(html, 'html.parser')

        count = 0
        while len(soup.find_all('div', {'class': '_309ad3C js-lazyload'})) + len(soup.find_all('div', {'class': '_309ad3C lazyloaded'})) > 0:
            print('waiting')
            time.sleep(0.8)
            html = web.page_source
            soup = BeautifulSoup(html, 'html.parser')
            if count == 5:
                scrollUpToDown(web)
            if count > 12:
                web.refresh()
                scrollUpToDown(web)
                count = 0
                continue
            count += 1
        time.sleep(1)
        elements = soup.find_all('div', {'class': '_309ad3C'})
        urlList = []
        downloadedWell = True
        downloadcount = 0
        for element in elements:
            # print(element)
            est = str(element)
            if (est.find('(') != -1 & est.find(')') != -1) & (est.find('lazyload') == -1):
                est = est[est.find('(')+2: est.find(')')-1]
                urlList.append(est)
                filename = savePath + "\\" + est.split('/')[-1]
                print(est)
                # print(filename)
                try:
                    if os.path.isfile(filename):
                        print(': already')
                    else:
                        urllib.request.urlretrieve(est, filename)
                        print(': downloaded')
                        downloadcount += 1
                except:
                    print('error, refrestart this page')
                    downloadedWell = False
                    break
        if downloadedWell == False:
            continue
        print('Downloaded images in this page: ' + str(downloadcount))
        web.find_element_by_xpath(
            '//*[@id="wrapper"]/div[1]/div/nav/div/span[2]/a').click()
        repeatNum -= 1


def main():
    # print("launch path" + os.getcwd())
    # print('phantom path' + phantompath)
    print(' ')
    userId = input('Id:')
    userPd = getpass.getpass('Password:')
    web = webdriver.Chrome(os.getcwd() + '\\chromedriver.exe')
    driverSetup(web, userId, userPd, urlLogin)
    startUrl = input('Start url:')
    savePath = input('Path to save:')
    pageNumber = int(input('Number of pages to download:'))
    web.get(startUrl)
    crawling(web, pageNumber, savePath)


if __name__ == "__main__":
    main()
