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


def create_twitch_clip(streamer_name, stream_date, stream_time):
    base_url = 'https://www.twitch.tv/'
    base_url = "".join((base_url, streamer_name))
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override",
                           "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0")

    # headless is needed here because we do not have a GUI version of firefox
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    browser.get(base_url)
    browser.implicitly_wait(3)

    ##Checking that username exists
    try:
        # Wait for page to load
        WebDriverWait(browser, 20).until(lambda browser: browser.execute_script(
            "return document.readyState;") == "complete")

        #Get website information
        element = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div/div/div[2]/p')
        print(element.text)
        if (element.text == "Sorry. Unless you’ve got a time machine, that content is unavailable."):
            raise Exception('No account was found by this username')
    except Exception as e:
        exception_thrown = str(e)
        exception_checker = "Unable to locate element: /html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div/div/div[2]/p" in exception_thrown
        if(exception_checker == True):
            print("Username was found")
        else:
            #Will throw 'No account was found by this username'
            sys.exit(e)
    
    ##Finding all videos on the page and finding the video link for the date
    video_url = 'https://www.twitch.tv/{}/videos?filter=archives&sort=time'.format(streamer_name)
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override",
                           "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0")

    # headless is needed here because we do not have a GUI version of firefox
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    browser.get(video_url)
    browser.implicitly_wait(3)

    try:
        # Wait for page to load
        WebDriverWait(browser, 20).until(lambda browser: browser.execute_script(
            "return document.readyState;") == "complete")
        sleep(5)
        page_source = browser.page_source

        # Soup it
        soup = bs4.BeautifulSoup(page_source, 'html.parser')
        videos_found = soup.findAll("div",{"class":"tw-hover-accent-effect__children"})
        print("Videos found:",str(len(videos_found)))
        video_start_url = "https://www.twitch.tv"
        for video in videos_found:
            get_video_info = video.find('img', alt=True)
            get_href = video.find("a",{"class":"tw-interactive tw-link"})

            video_title = get_video_info["alt"]
            video_date = get_video_info['title']
            video_url = video_start_url+get_href['href']
            print("Title:",video_title,"Video Date:",video_date,"Video URL:",video_url)
        
        stream_date_day = stream_date[:2]
        stream_date_month = stream_date[3:5]
        datetime_object = datetime.datetime.strptime(stream_date_month, "%m")
        stream_month_name = datetime_object.strftime("%b")
        stream_date_year = stream_date[6:10]
        formatted_stream_date_input = '{} {}, {}'.format(stream_date_day, stream_month_name, stream_date_year)
        print(formatted_stream_date_input)

        
    except Exception as e:
        print("Error",e)
        
    #browser.close()
    browser.quit()



if __name__ == '__main__':
    create_twitch_clip("summit1g", "05/11-2020", "test")
