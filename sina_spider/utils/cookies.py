import time
import pickle

from selenium import webdriver

from .user import UserSet


class Cookies(object):
    def __init__(self):
        self._cookies = dict()
        try:
            with open('.\sina_spider\data\cookies', 'rb') as f:
                self._cookies = pickle.load(f)
            if(time.time() - self._cookies['time']>3600*24):
                self._updateCookies()
        except:
            self._updateCookies()


    def _updateCookies(self):
        print('update cookies')
        for user in UserSet().user_set:
                self._getLoginCookies(*user)
        Cookiestime = time.time()
        self._cookies['time'] = Cookiestime
        self._SaveCookies()

    def getCookies(self, username):
        return self._cookies[username]


    def _getLoginCookies(self, username, password):
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
        driver = webdriver.PhantomJS(executable_path="phantomjs.exe", desired_capabilities=cap)
        driver.get("https://passport.weibo.cn/signin/login")
        time.sleep(2)
        #driver.get_screenshot_as_file('00.png')
        elem_user = driver.find_element_by_id('loginName')
        elem_user.send_keys(username)  # 用户名
        elem_pwd = driver.find_element_by_id("loginPassword")
        elem_pwd.send_keys(password)  # 密码
        #driver.get_screenshot_as_file('01.png')
        time.sleep(2)
        elem_sub = driver.find_element_by_id("loginAction")
        elem_sub.click()  # 点击登陆
        time.sleep(3)
        print(username+"'s cookies got")
        self._cookies[username] = driver.get_cookies()

    def _SaveCookies(self):
        with open('.\sina_spider\data\cookies', 'wb') as f:
            pickle.dump(self._cookies, f)

def main():
    ck = Cookies()

if __name__ == '__main__':
    main()

