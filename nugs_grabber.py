from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
import re
import time
import wget
import os


username = 'email'
password = 'password'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--mute-audio')
chrome_options.add_argument('--disable-logging')


class Nugget:
    url = ''
    name = ''
    artist = ''
    length = ''
    show_id = ''


def nug_ripper(showIDs):
    # spin up chrome, login to nugs net, find username/pw text fields, submit
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("https://play.nugs.net/#/login")
    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.ID, "username"))
        )
        login_field = driver.find_element_by_id('username')
        login_field.clear()
        login_field.send_keys(username)
        pw_field = driver.find_element_by_id('pw')
        pw_field.clear()
        pw_field.send_keys(password)
        pw_field.submit()
    finally:
        print('logging in...')


    # on submit, page changes to latest releases, wait for page to load
    try:
        WebDriverWait(driver, 10).until(
            ec.url_matches('https://play.nugs.net/#/catalog/latest')
        )
        print('login successful')

    finally:
        if driver.current_url != 'https://play.nugs.net/#/catalog/latest':
            print('login failed')
            driver.quit()

    sanitized_urls = []

    # start iterating show ID's and loading the recording page
    for showID in showIDs:

        print('starting crawl of show: ' + showID)

        show_url = "https://play.nugs.net/#/catalog/recording/" + showID

        driver.get(show_url)

        # wait for all elements with the icon-play css class to load, then log song title and length if needed later
        try:
            WebDriverWait(driver, 10).until(
                ec.presence_of_all_elements_located((By.CSS_SELECTOR, "button.icon.ng-binding.icon-play"))
            )
            title_elements = driver.find_elements_by_css_selector('div.song-title.ng-binding')
            length_elements = driver.find_elements_by_css_selector('div.song-runtime.ng-binding')

            i = 0
            lengths = []
            song_names = []
            for element in title_elements:
                length_element = length_elements[i]
                song_names.append(element.text)
                lengths.append(length_element.text)
                i += 1

        finally:
            if driver.current_url != show_url:
                print('couldnt grab show page, make sure its a live show')
                driver.quit()

        # store all play button elements in an array
        all_button_elements = driver.find_elements_by_css_selector('button.icon.ng-binding.icon-play')

        # click on all play buttons one by one, waiting 1 second in between them and scrolling the page 125 pixels
        # each time, incase the show has lots of songs
        for x in range(0, len(all_button_elements), 1):
            element = all_button_elements[x]
            element.click()
            driver.execute_script("window.scrollBy(0,125)")
            time.sleep(1)

        # grab the browsers logs, which reveals the .m4a url of each clicked song
        browser_logs = driver.get_log('browser')

        # prepare the directory to load the songs
        os.makedirs('./downloads/' + showID, 0o777, exist_ok=True)

        # iterate each log item, pull the .m4a url out, download it to /downloads/<showid>
        for browser_log in browser_logs:

            if "ondemandvid" in browser_log["message"]:
                # print('m4a found' + browser_log["message"])
                urls = re.findall(r'(http?://[^\s]+)', browser_log["message"])
                i = 0
                for url in urls:
                    # print(url)
                    if ".m4a" in url:
                        nugget = Nugget()
                        nugget.url = url[:-2]
                        nugget.name = str(os.path.basename(nugget.url).split("?")[0])
                        nugget.show_id = showID
                        sanitized_urls.append(nugget)
                        print(wget.download(nugget.url, './downloads/' + showID + '/' + nugget.name))
                        i += 1

        print('show ' + showID + ' finished downloading')

        # for nugget in sanitized_urls:
        #     sanitized_urls.append(nugget.url)

    driver.quit()

    return sanitized_urls


print('Starting nug_grabber in: ' + os.getcwd())

log = nug_ripper(['1345', '20660'])
