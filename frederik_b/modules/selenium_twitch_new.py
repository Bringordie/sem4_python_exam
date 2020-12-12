import requests
import bs4
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import datetime

import imaplib, email 


class twitch_app:
    def __init__(self, streamer_name, stream_date, stream_time):
        self.base_url = 'https://www.twitch.tv/'
        self.vod_found = ""

        stream_date_day = stream_date[:2]
        stream_date_month = stream_date[3:5]
        datetime_object = datetime.datetime.strptime(stream_date_month, "%m")
        stream_month_name = datetime_object.strftime("%b")
        stream_date_year = stream_date[6:10]
        formatted_stream_date_input = '{} {}, {}'.format(stream_month_name, stream_date_day, stream_date_year)
        print(formatted_stream_date_input)

        self.streamer_name = streamer_name
        print(self.streamer_name)
        self.stream_date = formatted_stream_date_input
        self.stream_time = stream_time
        self.vod_video_list = []
        self.twitch_pincode = ""

        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("general.useragent.override",
                           "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0")

        # headless is needed here because we do not have a GUI version of firefox
        self.options = Options()
        self.options.headless = True
        self.browser = webdriver.Firefox(options=self.options)

        self.browser.get(self.base_url)
        self.browser.implicitly_wait(3)
        WebDriverWait(self.browser, 20).until(lambda browser: browser.execute_script("return document.readyState;") == "complete")

    def check_username_exists(self):
        try:
        # Wait for page to load
            #WebDriverWait(self.browser, 20).until(lambda browser: browser.execute_script("return document.readyState;") == "complete")
            sleep(10)
        #Get website information
            element = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div/div/div[2]/p')
            print(element.text)
            if (element.text == "Sorry. Unless you’ve got a time machine, that content is unavailable."):
                raise Exception('No account was found by this username')
        except Exception as e:
            exception_thrown = str(e)
            exception_checker = "Unable to locate element: /html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div/div/div[2]/p" in exception_thrown
            if(exception_checker == True):
                ####NEED TO FIX SOMETHING HERE, WORKS ON OTHER.
                print("Username was found")
            else:
                #Will throw 'No account was found by this username'
                #Gracefully close the browser before
                sys.exit(e)

    def find_videos(self):
        ##Finding all videos on the page and finding the video link for the date
        video_url = 'https://www.twitch.tv/{}/videos?filter=archives&sort=time'.format(self.streamer_name)

        self.browser.get(video_url)
        self.browser.implicitly_wait(3)

        try:
            # Wait for page to load
            WebDriverWait(self.browser, 20).until(lambda browser: browser.execute_script(
                "return document.readyState;") == "complete")
            sleep(5)
            page_source = self.browser.page_source

            # Soup it
            soup = bs4.BeautifulSoup(page_source, 'html.parser')
            videos_found = soup.findAll("div",{"class":"tw-hover-accent-effect__children"})
            ## If len is 0 we should stop the program or run it again somehow as the sleep might not be enough
            print("Videos found:",str(len(videos_found)))
            video_start_url = "https://www.twitch.tv"
            for video in videos_found:
                get_video_info = video.find('img', alt=True)
                get_href = video.find("a",{"class":"tw-interactive tw-link"})

                video_title = get_video_info["alt"]
                video_date = get_video_info['title']
                video_url = video_start_url+get_href['href']
                if (len(video_date) != 12):
                    video_date = video_date[:4] + '0' + video_date[4:]

                vod_info = {"title": video_title, "date": video_date, "url": video_url}
                self.vod_video_list.append(vod_info)
                print("Title:",video_title,"Video Date:",video_date,"Video URL:",video_url)
            

        except Exception as e:
            print("Error",e)

    def match_date_to_vod(self):
        for video in self.vod_video_list:
            #print(video['date']," VS ",self.stream_date)
            if (video['date'] == self.stream_date):
                print("WE FOUND A MATCH", video['url'])
                self.vod_found = video['url']
                return video['url']
            else:
                print('NO MATCH WAS FOUND')

    def login_to_account(self):
        #Remove this
        sleep(10)
        #
        username = ""
        password = ""
        try:
            ##Click login button
            login_button = self.browser.find_element_by_css_selector('#root > div > div.tw-flex.tw-flex-column.tw-flex-nowrap.tw-full-height > nav > div > div.tw-align-items-center.tw-flex.tw-flex-grow-1.tw-flex-shrink-1.tw-full-width.tw-justify-content-end > div.tw-flex.tw-full-height.tw-mg-r-1.tw-pd-y-1 > div > div.anon-user.tw-flex.tw-flex-nowrap > div:nth-child(1)')
            print('Login Button', login_button)
            login_button.click()

            ##Fill information
            sleep(5)

            username_field = self.browser.find_element_by_id('login-username')
            if(username_field):
                print('Username Field',username_field)
            username_field.send_keys(username)
            
            password_field = self.browser.find_element_by_id('password-input')
            if(password_field):
                print('Password Field',password_field)
            password_field.send_keys(password)
            
            ##Login
            #password_field.send_keys(Keys.ENTER)
            #Might not work
            #print('before login',self.browser.get_cookies())
            login_button2 = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div.tw-mg-b-1 > form > div > div:nth-child(3) > button')
            print('Login Button2 clicked', login_button2)
            login_button2.click()

            ##Checking for verification
            sleep(5)
            #verification_form = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div:nth-child(2) > div > div > div')
            verification_form = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div.tw-mg-b-1 > div:nth-child(2) > div > div:nth-child(1)')
            if(verification_form):
                #element=self.browser.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div/div[1]/div/div")
                element=self.browser.find_element_by_xpath("//body")
                print('There is a verification box.')
                element.send_keys(Keys.TAB, Keys.TAB, Keys.TAB)
                sleep(15)
                self.twitch_pincode = self.get_pincode()
                for pincode_key in self.twitch_pincode:
                    element.send_keys(pincode_key)
                element.send_keys(Keys.ENTER)
            
            #sleep(15)
            # verytestsuchtwitch = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div:nth-child(2) > div > div > div')
            # if(verytestsuchtwitch):
            #     print("WE SHOULD NOT SEE THE THIS")
            #     print(verytestsuchtwitch)
            print("We might be logged in now")


            #sleep(30)
            #print('after login',self.browser.get_cookies())
        except Exception as e:
            print("Error",e)
    
    def get_pincode(self):
        user = ''
        password = '.'
        imap_url = 'imap.gmail.com'


        # this is done to make SSL connnection with GMAIL 
        con = imaplib.IMAP4_SSL(imap_url) 

        # logging the user in 
        con.login(user, password)  
        
        # calling function to check for email under this label 
        con.select('Inbox')  
        
        # fetching emails from this user "account@twitch.tv" 
        msgs = self.get_emails(self.search('FROM', 'account@twitch.tv', con), con) 
        
        # Getting the latest recived email
        ###### TODO Should be a verify on when the email was recieved and check that to the current time.
        for sent in msgs[-1]: 
            if type(sent) is tuple:  
        
                # encoding set as utf-8 
                content = str(sent[1], 'utf-8')  
                data = str(content) 

                try:  
                    indexstart = data.find("ltr") 
                    data2 = data[indexstart + 5: len(data)] 
                    indexend = data2.find("</div>") 

                    #print(data2[0: indexend]) 
                    pin_data = data2[0: indexend]
                    split_word = 'overflow: hidden;">'
                    res = pin_data.partition(split_word)[2] 
                    #print(res[:6])
                    twitch_pincode = res[:6]
                    print('PIN:',twitch_pincode)
                    return twitch_pincode
        
                except Exception as e:
                    print("Error",e)

    def search(self, key, value, con):  
        result, data = con.search(None, key, '"{}"'.format(value)) 
        return data 
  
    # Function to get the list of emails under this label 
    def get_emails(self, result_bytes, con): 
        msgs = [] # all the email data are pushed inside an array 
        for num in result_bytes[0].split(): 
            typ, data = con.fetch(num, '(RFC822)') 
            msgs.append(data) 
    
        return msgs 

    def create_clip(self):
        ##Remember to remove this
        self.vod_found = "https://www.twitch.tv/videos/832580881?filter=archives&sort=time"
        #
        clean_url = self.vod_found.replace('?filter=archives&sort=time', '')
        stream_vod_hour = self.stream_time[:2]
        steam_vod_minute = self.stream_time[3:5]
        stream_vod_seconds = self.stream_time[6:9]
        new_timestamp_url = '{}?t={}h{}m{}s'.format(clean_url, stream_vod_hour, steam_vod_minute, stream_vod_seconds)

        self.browser.get(new_timestamp_url)
        self.browser.implicitly_wait(3)
        sleep(5)
        print('CURRENT URL',self.browser.current_url)
        

        #Todo should check for mature blocker#
        try:
            #Click create clip button - NOT WORKING, Might not be logged in?
            create_clip_button = self.browser.find_element_by_css_selector('#root > div > div.tw-flex.tw-flex-column.tw-flex-nowrap.tw-full-height > div.tw-flex.tw-flex-nowrap.tw-full-height.tw-overflow-hidden.tw-relative > main > div.root-scrollable.scrollable-area.scrollable-area--suppress-scroll-x > div.simplebar-scroll-content > div > div > div.persistent-player.tw-elevation-0 > div > div.video-player > div > div > div > div:nth-child(6) > div > div.tw-flex.tw-mg-b-1.tw-mg-l-1.tw-mg-r-1 > div.player-controls__right-control-group.tw-align-items-center.tw-flex.tw-flex-grow-1.tw-justify-content-end > div:nth-child(1) > div:nth-child(2) > div > button > span > div > div > div')
            print('Clip Button', create_clip_button)
            create_clip_button.click()

            #Doesn't seem to work
            # print('CURRENT URL',self.browser.current_url)
            # element=self.browser.find_element_by_xpath("//body")
            # element.send_keys(Keys.ALT, 'x')
            
        except Exception as e:
            print("Error",e)
            sleep(5)
        # self.browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 
        # print('CURRENT URL',self.browser.current_url)

        
        #Add title and publish
        # try:
        #     title_field = self.browser.find_element_by_id('cmgr-title-input')
        #     if(title_field):
        #         print('Title Field',title_field)
        #         title_field.send_keys("SEM4 Python")

        #     publish_button = self.browser.find_element_by_css_selector('#root > div > div > div > div.simplebar-scroll-content > div > div > main > div > div > div.tw-animation.tw-animation--duration-extra-long.tw-animation--fill-mode-both.tw-animation--slide-in-bottom.tw-animation--timing-ease-in-out > div > div:nth-child(2) > div:nth-child(2) > div.tw-align-items-center.tw-flex.tw-justify-content-between.tw-pd-t-1 > div > div')
        #     if(publish_button):
        #         print('Publish Button', publish_button)
        #         publish_button.click()
        # except Exception as e:
        #     print("Error",e)


    def close_browser(self):
        self.browser.quit()
        print("Browser closed")

    

    

if __name__ == '__main__':
    #twitch = twitch_app("summit1g", "05/11-2020", "00:15:30")
    twitch = twitch_app("kanathras", "10/12-2020", "00:15:30")
    #twitch.check_username_exists()
    #twitch.find_videos()
    #twitch.match_date_to_vod()
    twitch.login_to_account()
    ####print(twitch.get_pincode())
    twitch.create_clip()
    twitch.close_browser()

