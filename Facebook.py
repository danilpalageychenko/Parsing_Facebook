import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Facebook:
    count = 24
    countWindows = 0
    my_file = open("List_Id.txt", "w")
    idAuthorPostCount = 0

    def driver(self):
        url = 'https://www.facebook.com/'
        driver = webdriver.Chrome(executable_path='C:\drivers\chromedriver')
        # driver = webdriver.Chrome(chrome_options=webdriver.ChromeOptions)
        # driver.add_argument('headless')
        # binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
        # driver = webdriver.Firefox(firefox_binary=binary)
        # driver = webdriver.Firefox()
        # driver.maximize_window()
        # driver.implicitly_wait(10)
        driver.get(url)
        driver.add_cookie({'name': 'c_user','value': '...','domain': '.facebook.com','path': '/'})
        driver.add_cookie({'name': 'datr', 'value': '...', 'domain': '.facebook.com', 'path': '/'})
        driver.add_cookie({'name': 'fr', 'value': '...','domain': '.facebook.com', 'path': '/'})
        driver.add_cookie({'name': 'pl', 'value': '...', 'domain': '.facebook.com', 'path': '/'})
        driver.add_cookie({'name': 'presence','value': '...','domain': '.facebook.com', 'path': '/'})
        driver.add_cookie({'name': 'm_pixel_ratio', 'value': '...', 'domain': '.facebook.com', 'path': '/'})
        driver.add_cookie({'name': 'sb', 'value': '...', 'domain': '.facebook.com', 'path': '/'})
        driver.add_cookie({'name': 'wd', 'value': '...', 'domain': '.facebook.com', 'path': '/'})
        driver.add_cookie({'name': 'xs', 'value': '...', 'domain': '.facebook.com','path': '/'})
        return driver

    def findLikes(self, id):
        urlLikes = 'https://www.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier=%d' % int(id)
        my_file = open("List_Id.txt", "a+")
        self.countWindows = self.countWindows + 1
        self.switchWindows(driver, urlLikes)
        soup = BeautifulSoup(driver.page_source, "lxml")
        found = soup.select('li._5i_q a[data-gt]')
        i = found.__len__()
        j = 0
        for found in found:
            foundIdLike = re.findall(r'"eng_tid":"(\d*)', found.get('data-gt'))
            if j != i:
                my_file.write(foundIdLike[0] + ". ")
            else:
                my_file.write(foundIdLike[0] + ", ")
            j = j + 1
        my_file.write('\n')
        my_file.close()
        self.countWindows = self.countWindows - 1
        driver.close()
        driver.switch_to.window(driver.window_handles[self.countWindows])

    def write_id_to_file(self, url, driver, j=0):
        if self.countWindows > 0:
            self.switchWindows(driver, url)
        else:
            driver.get(url)

        id = url.split('=')[1].split('&')[0]

        if self.idAuthorPostCount == 0:
            soup = BeautifulSoup(driver.page_source, "lxml")
            found = soup.find('a', {'rel': 'theater'}).get('ajaxify')
            res = re.findall(r'/(.*)/.*/.*\.(\d*)/.*', found)
            if not res:
                res = re.findall(r'/(.*)/.*/(\d*)/.*', found)
            date = soup.select('div.hidden_elem abbr')[0].get('title')
            my_file = open("List_Id.txt", "a+")
            my_file.write(
                '\n' + '-' * 230 + '\n' + 'Author Post' + '\t' * 13 + 'Id Posts' + '\t' * 7 + 'Reposts' + '\t' * 13 + 'Date' + '\t' * 13 + 'Likes' '\n')
            my_file.write(str(res[0][0]) + ' : ' + str(res[0][1]) + '\t' * 6 + str(id) + '\t' * 20 + date + '\t' * 10)
            my_file.close()

            self.findLikes(id)
            self.idAuthorPostCount = 1

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            soup = BeautifulSoup(driver.page_source, "lxml")
            if not soup.select('#pagelet_scrolling_pager div'):
                self.fin_id(driver, BeautifulSoup, re, id, j)
                self.countWindows = self.countWindows - 1
                if self.countWindows >= 0:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[self.countWindows])
                break
        self.idAuthorPostCount = 1

    def fin_id(self, driver, BeautifulSoup, re, id, j=0):
        soup = BeautifulSoup(driver.page_source, "lxml")
        id_list = soup.find('div', {'id': 'view_shares_dialog_%s' % id})
        i = 1
        if id_list == None:
            return
        for id_list in id_list:
            for id_list in id_list:
                qwe = id_list.get('data-ft')
                res = re.findall(r'"actor_id":"(\d*)"', qwe)
                soup2 = BeautifulSoup(str(id_list), "lxml")
                link = soup2.find('a', {'class': 'UFIShareLink'})
                link2 = soup2.find('a', {'aria-live': 'polite'})
                my_file = open("List_Id.txt", "a+")
                if j == 1:
                    my_file.write('\t' * self.count + 'Pere ' + str(i) + ' ' + str(res[0] + '\t' * 30));
                else:
                    my_file.write('\t' * self.count + str(i) + ' ' + str(res[0] + '\t' * 30));

                # Search Likes!!!!
                # soup2 = BeautifulSoup(str(id_list), "lxml")
                # if soup2.select('div[direction=right] span'):
                #    print(str(res[0]))
                my_file.write('\n')
                # self.findLikes(str(res[0]))

                i = i + 1
                my_file.close()
                if link != None:
                    self.count = self.count + 1
                    self.countWindows = self.countWindows + 1
                    self.write_id_to_file(link.get('href'), driver)
                    self.count = self.count - 1
                if link2 != None:
                    self.count = self.count + 1
                    self.countWindows = self.countWindows + 1
                    self.write_id_to_file(link2.get('href'), driver, 1)
                    self.count = self.count - 1

    def switchWindows(self, driver, url):
        str = "window.open('" + url + "','_blank');"
        driver.execute_script(str)
        driver.switch_to.window(driver.window_handles[self.countWindows])


if __name__ == '__main__':

    list = [222314561690783,   # Мой
            1292828720851517]  # Порошенко

    driver = Facebook().driver()
    for i in list:
        url = 'https://www.facebook.com/shares/view?id=%d' % i
        Facebook().write_id_to_file(url, driver)
