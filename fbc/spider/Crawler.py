from fbc import Driver
import time

class Crawler():

    def __init__(self, id):
        self.timeout = 10
        self.driver = Driver.open()
        self.driver.get("https://fb.com/%s" % (id))
        self.hide_header_area()

    def __del__(self):
        Driver.close()
        print("Driver closed!")

    @staticmethod
    def __get_expand_btn(driver):
        container = driver.find_element_by_id("mainContainer")
        article = container.find_element_by_xpath(".//div[@role='article']")
        form = article.find_element_by_tag_name("form")
        return form.find_elements_by_xpath(".//a[@role='button'][@href='#']")[-1]

    def hide_header_area(self):
        script = "document.getElementById('headerArea').setAttribute('style', 'display: none')"
        self.driver.execute_script(script)

    def load_more_comments(self, form):
        Driver.wait_until(Crawler.__get_expand_btn)
        Crawler.__get_expand_btn(self.driver).click()

    def expand_comments(self, form):
        Driver.wait_until(lambda x: x.find_elements_by_xpath(".//a[@role='button']")[-1])
        expand_btn = form.find_elements_by_xpath(".//a[@role='button']")[-1]
        expand_btn.click()

    def extract_comments(self, form):
        comments = list()
        for elm in form.find_elements_by_xpath(".//div[@role='article']"):
            try:
                comments.append(elm.find_element_by_xpath('.//span[@class="_3l3x"]').text)
                comments.append(elm.find_element_by_xpath('.//span[@class="_3l3x _1n4g"]').text)
            except:
                pass
        return comments

    def all_cmt_not_loaded(self, form):
        try:
            form.find_element_by_xpath(".//span[@class='_3bu3 _7a93']")
        except:
            return False

        return True

    def crawl_comments(self):
        container = self.driver.find_element_by_id("mainContainer")
        article = container.find_element_by_xpath(".//div[@role='article']")
        form = article.find_element_by_tag_name("form")

        self.expand_comments(form)
        Driver.wait_until(lambda x : x.find_element_by_xpath(".//span[@class='_3bu3 _7a93']"))

        while (self.all_cmt_not_loaded(form)):
            self.load_more_comments(form)

        return self.extract_comments(form)
            
            
