import requests
import bs4
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sys
from datetime import datetime

import imaplib, email 


class twitch_app:
    def __init__(self, streamer_name, stream_date, stream_time):
        self.base_url = 'https://www.twitch.tv/'
        self.base_url = "".join((self.base_url, streamer_name))
        self.vod_found = ""

        self.TWITCH_USERNAME = "sem4_python2020"
        self.TWITCH_PASSWORD = "sem4pythonpasswordforTwitch."

        self.GMAIL_USERNAME = 'sem4python2020@gmail.com'
        self.GMAIL_PASSWORD = 'sem4pythonpasswordforGmail.'

        self.failed_attempt_count = 0

        stream_date_day = stream_date[:2]
        stream_date_month = stream_date[3:5]
        datetime_object = datetime.strptime(stream_date_month, "%m")
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

        PATH = 'C:\\Program Files (x86)\\chromedriver.exe'
        self.browser = webdriver.Chrome(PATH)

        self.browser.get(self.base_url)
        self.browser.implicitly_wait(3)
        WebDriverWait(self.browser, 20).until(lambda browser: browser.execute_script("return document.readyState;") == "complete")

    def check_username_exists(self):
        try:
        #Get website information
            element = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div/div/div[2]/p')
            print(element.text)
            if (element.text == "Sorry. Unless you’ve got a time machine, that content is unavailable."):
                raise Exception('No account was found by this username')
        except Exception as e:
            exception_thrown = str(e)
            exception_checker = "no such element: Unable to locate element:" in exception_thrown
            if(exception_checker == True):
                print("Username was found")
            else:
                print("Username was not found")
                self.close_browser()
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
            videos_found = soup.find_all("div",{"class":"tw-hover-accent-effect"})

            print("Videos found:",str(len(videos_found)))
            if (len(videos_found) == 0):
                print('This user has no videos')
                self.close_browser()
                sys.exit()

            video_start_url = "https://www.twitch.tv"
            for video in videos_found:
                get_video_info = video.find('img', alt=True)
                get_href = video.find("a",{"class":"tw-link"})

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
            if (video['date'] == self.stream_date):
                print("WE FOUND A MATCH", video['url'])
                self.vod_found = video['url']
                return video['url']
        if (self.vod_found == ""):
            print('NO VIDEO MATCH WAS FOUND')
            self.close_browser()
            sys.exit()


    def login_to_account(self):
        try:
            ##Click login button
            login_button = self.browser.find_element_by_css_selector('#root > div > div.tw-flex.tw-flex-column.tw-flex-nowrap.tw-full-height > nav > div > div.tw-align-items-center.tw-flex.tw-flex-grow-1.tw-flex-shrink-1.tw-full-width.tw-justify-content-end > div.tw-flex.tw-full-height.tw-mg-r-1.tw-pd-y-1 > div > div.anon-user.tw-flex.tw-flex-nowrap > div:nth-child(1)')
            print('Login Button', login_button)
            login_button.click()

            ##Fill information
            username_field = self.browser.find_element_by_id('login-username')
            if(username_field):
                print('Username Field',username_field)
            username_field.send_keys(self.TWITCH_USERNAME)
            
            password_field = self.browser.find_element_by_id('password-input')
            if(password_field):
                print('Password Field',password_field)
            password_field.send_keys(self.TWITCH_PASSWORD)
            
            ##Login
            login_button2 = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div.tw-mg-b-1 > form > div > div:nth-child(3) > button')
            print('Login Button2 clicked', login_button2)
            login_button2.click()

            #Manually overwriting
            sleep(15)

            ##Checking for verification
            verification_form = self.browser.find_element_by_css_selector('#modal-root-header')
            print(verification_form.text)
            if(verification_form.text == 'Verify login code'):
                print('There is a verification box.')
                verification_button = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div.tw-mg-b-1 > div:nth-child(2) > div > div:nth-child(1) > div')

                verification_button.click()

                #Fix for input as the loop no longer works.
                verification_input1 = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div.tw-mg-b-1 > div:nth-child(2) > div > div:nth-child(1) > div > input')
                verification_input2 = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div.tw-mg-b-1 > div:nth-child(2) > div > div:nth-child(2) > div > input')
                verification_input3 = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div.tw-mg-b-1 > div:nth-child(2) > div > div:nth-child(3) > div > input')
                verification_input4 = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div.tw-mg-b-1 > div:nth-child(2) > div > div:nth-child(4) > div > input')
                verification_input5 = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div.tw-mg-b-1 > div:nth-child(2) > div > div:nth-child(5) > div > input')
                verification_input6 = self.browser.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div > div > div.tw-border-radius-medium.tw-flex.tw-overflow-hidden > div > div > div.tw-mg-b-1 > div:nth-child(2) > div > div.tw-pd-r-0 > div > input')

                self.twitch_pincode = self.get_pincode()
                verification_input1.send_keys(self.twitch_pincode[0])
                verification_input2.send_keys(self.twitch_pincode[1])
                verification_input3.send_keys(self.twitch_pincode[2])
                verification_input4.send_keys(self.twitch_pincode[3])
                verification_input5.send_keys(self.twitch_pincode[4])
                verification_input6.send_keys(self.twitch_pincode[5])

        except Exception as e:
            print("Error",e)

    def login_checker(self):
        #Clicking on the profile to be able to find a username
        sleep(5)
        login_picture = self.browser.find_element_by_css_selector('#root > div > div.tw-flex.tw-flex-column.tw-flex-nowrap.tw-full-height > nav > div > div.tw-align-items-center.tw-flex.tw-flex-grow-1.tw-flex-shrink-1.tw-full-width.tw-justify-content-end > div.tw-flex.tw-full-height.tw-mg-r-1.tw-pd-y-1 > div > div > div > div > button')
        print("login_picture",login_picture)
        login_picture.click()
        #Souping to read the username
        soup = bs4.BeautifulSoup(self.browser.page_source, 'html.parser')
        find_username = soup.find_all('h6')
        username_loggedin = find_username[0].text
        print('User logged in:',username_loggedin)
    
    def get_pincode(self):
        imap_url = 'imap.gmail.com'

        # this is done to make SSL connnection with GMAIL 
        con = imaplib.IMAP4_SSL(imap_url) 

        # logging the user in 
        con.login(self.GMAIL_USERNAME, self.GMAIL_PASSWORD)  
        
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
                    twitch_pincode = res[:6]
                    print('PIN:',twitch_pincode)
                    return twitch_pincode
        
                except Exception as e:
                    print("Error",e)

    def search(self, key, value, con):  
        _, data = con.search(None, key, '"{}"'.format(value)) 
        return data 

    # Function to get the list of emails under this label 
    def get_emails(self, result_bytes, con): 
        msgs = [] # all the email data are pushed inside an array 
        for num in result_bytes[0].split(): 
            _, data = con.fetch(num, '(RFC822)') 
            msgs.append(data) 
        return msgs 

    def go_to_create_clip(self):
        print("Starting to create clip")
        clean_url = self.vod_found.replace('?filter=archives&sort=time', '')
        stream_vod_hour = self.stream_time[:2]
        steam_vod_minute = self.stream_time[3:5]
        stream_vod_seconds = self.stream_time[6:9]
        new_timestamp_url = '{}?t={}h{}m{}s'.format(clean_url, stream_vod_hour, steam_vod_minute, stream_vod_seconds)

        self.browser.get(new_timestamp_url)

        #Todo should check for mature blocker#

        #Clicking the CLIP button
        sleep(5)
        element=self.browser.find_element_by_xpath("//body")
        element.send_keys(Keys.ALT, 'x')
        sleep(5)

    def publish_clip(self):
        #Add title and publish
        try:
            self.browser.switch_to.window(self.browser.window_handles[1])
            print(self.browser.current_url)
            title_field = self.browser.find_element_by_id('cmgr-title-input')
            title_field.send_keys("SEM4 Python")
            
            publish_button = self.browser.find_element_by_css_selector('#root > div > div > div > div.simplebar-scroll-content > div > div > main > div > div > div.tw-animation.tw-animation--duration-extra-long.tw-animation--fill-mode-both.tw-animation--slide-in-bottom.tw-animation--timing-ease-in-out > div > div:nth-child(2) > div:nth-child(2) > div.tw-align-items-center.tw-flex.tw-justify-content-between.tw-pd-t-1 > div > div > div > button')
            print("publish button",publish_button)
            publish_button.click()
            sleep(5)
            soup = bs4.BeautifulSoup(self.browser.page_source, 'html.parser')
            find_published_link = soup.find('input', {'class':'tw-block tw-border-bottom-left-radius-medium tw-border-bottom-right-radius-medium tw-border-top-left-radius-medium tw-border-top-right-radius-medium tw-font-size-6 tw-full-width tw-input tw-pd-l-3 tw-pd-r-1 tw-pd-y-05'})['value']
            print('PUBLISHED LINK:',find_published_link)
            now = datetime.now()
            dt_string = now.strftime("%d-%m-%Y_%HH%MM")
            filename = 'clips/{}.txt'.format(dt_string)
            with open(filename, 'w') as file_object:
                file_object.write('Username: ' + self.streamer_name + '\n')
                file_object.write('Date: ' + self.stream_date + '\n')
                file_object.write('VOD URL: ' + self.vod_found + '\n')
                file_object.write('Clip link: ' + find_published_link)

        #except Exception as e:
        except NoSuchElementException as e:
            exception_thrown = str(e)
            exception_checker = "no such element: Unable to locate element:" in exception_thrown
            if(exception_checker == True):
                self.failed_attempt_count += 1
                if self.failed_attempt_count > 5:
                    print('Something went wrong loading the publish page')
                    sys.exit(e)
                print('Refreshing page and trying again',self.failed_attempt_count)
                self.browser.refresh()
                sleep(5)
                self.publish_clip()
            else:
                print("Error",e)
                sys.exit(e)

    def close_browser(self):
        self.browser.quit()
        print("Browser closed")


if __name__ == '__main__':
    #twitch = twitch_app("summit1g", "05/11-2020", "00:15:30")
    twitch = twitch_app("kanathras", "21/12-2020", "00:15:30")
    twitch.check_username_exists()
    twitch.find_videos()
    twitch.match_date_to_vod()
    twitch.login_to_account()
    twitch.login_checker()
    twitch.go_to_create_clip()
    twitch.publish_clip()
    #twitch.close_browser()