from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests, glob, time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", False) #close brower after execution
# options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--disable-Advertisement")
options.add_argument("--disable-popup-blocking")
options.add_argument("start-maximized")

driver = webdriver.Chrome(options=options)

#XPATHS
playlist_title_xpath = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-playlist-header-renderer/div/div[2]/div[1]/div/yt-dynamic-sizing-formatted-string/div/yt-formatted-string'
video_title_xpath = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[1]/h1/yt-formatted-string'

# def download_thumbnail(thumbnail_xpath):
#     image_link = driver.find_element(By.XPATH, thumbnail_xpath).get_attribute('src')
#     response = requests.get(image_link)
#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         with open("thumbnail.jpg", "wb") as f:
#             f.write(response.content)

#waits 30 seconds for the file to appear in the downloads folder, returns true if found.
def is_file_downloaded(file_name, downloads_folder_path) -> bool:
    seconds = 0
    while seconds < 30:
        print(seconds)
        time.sleep(1)
        download_files_list = glob.glob(downloads_folder_path + '\*.mp3') #list of all the mp3 files in downloads

        if file_name in download_files_list:
            return True
        seconds += 1

    return False #the file was not found after 30 seconds