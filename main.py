from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait #used for explicit wait
from selenium.webdriver.support import expected_conditions as EC #used for explicit wait
import requests

#Finds the fist occurance of a video that is not a YouTube Short
def find_default_video_link() -> str:
    for i in range(1,11):
        #xpath to the thumbnail of the first video that is in the main content section. Will exclude the reel section.
        overlay_xpath = f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{i}]/div[1]/ytd-thumbnail/a/div[1]/ytd-thumbnail-overlay-time-status-renderer'
        link_path = f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{i}]/div[1]/ytd-thumbnail/a'
        thumbnail_xpath = f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{i}]/div[1]/ytd-thumbnail/a/yt-image/img'
        #overlay stle is DEFAULT = normal video, overlay style is SHORTS = YouTube Short
        if driver.find_element(By.XPATH, overlay_xpath).get_attribute('overlay-style') == 'DEFAULT':
            download_thumbnail(thumbnail_xpath=thumbnail_xpath)
            return driver.find_element(By.XPATH, link_path).get_attribute('href')

def download_thumbnail(thumbnail_xpath):
    image_link = driver.find_element(By.XPATH, thumbnail_xpath).get_attribute('src')
    response = requests.get(image_link)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        with open("thumbnail.jpg", "wb") as f:
            f.write(response.content)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True) #keeps browser open
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--disable-Advertisement")
options.add_argument("--disable-popup-blocking")
options.add_argument("start-maximized")

driver = webdriver.Chrome(options=options)

if __name__ == '__main__':

    driver.get('https://www.youtube.com/results?search_query=sabaton+back+in+control')
    #xpath to the first thumbnail overlay. The overlay is the video length for a normal video and SHROTS for a short
    #ytd-video-renderer[1] is the first video, ytd-video-renderer[2] would be the second.
    overlay_path = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a/div[1]/ytd-thumbnail-overlay-time-status-renderer'
    
    try:
        #waits until the overlay_path is loaded in. Throws error after 12 seconds
        WebDriverWait(driver, timeout=12).until(
            EC.presence_of_element_located((By.XPATH, overlay_path))
        )
    except:
        print('Webdriver did not find thumbnail xpath')
        
    link = find_default_video_link()
    print(link)

    driver.get('https://cobalt.tools/')
    driver.find_element(By.ID, 'url-input-area').send_keys(link)
    driver.find_element(By.ID, 'audioMode-true').click() #sets the downlaod mode to mp3
    driver.find_element(By.ID, 'download-button').click()

