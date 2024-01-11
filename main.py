from utils import driver, is_file_downloaded, video_title_xpath, playlist_title_xpath
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait #used for explicit wait
from selenium.webdriver.support import expected_conditions as EC #used for explicit wait
import shutil, os, sys, datetime, re
from pathlib import Path
import pyperclip

if __name__ == '__main__':
    playlist_link = pyperclip.paste()
    driver.get(playlist_link)
    playlist_title = driver.find_element(By.XPATH, playlist_title_xpath).text
    print('playlist title:', playlist_title)
    
    #finds all the videos in the playlist
    items = driver.find_elements(By.CSS_SELECTOR, 'a#thumbnail.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail[aria-hidden="true"][tabindex="-1"][rel="null"]')
    
    links_list = []
    for item in items:
        links_list.append(item.get_attribute('href'))

    for video_link in links_list:
        print(video_link)
        driver.get(video_link)
        
        try:
            #xpath to the video title
            video_title_xpath = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[1]/h1/yt-formatted-string'
            
            #waits until the video title is loaded in. Throws error after 15 seconds.
            #The script will be looking for the title, so it's a good way to check if the videos have loaded properly
            WebDriverWait(driver, timeout=15).until(
                EC.presence_of_element_located((By.XPATH, video_title_xpath))
            )
        except:
            print('YouTube did not load properly.')
            
        video_title = driver.find_element(By.XPATH, video_title_xpath).text

        video_code = re.compile(r'=(.*?)&').search(video_link).group(1)
        print('video code:',video_code)

        driver.get('https://cobalt.tools/')
        driver.find_element(By.ID, 'url-input-area').send_keys(video_link)
        driver.find_element(By.ID, 'audioMode-true').click() #sets the download mode to mp3
        driver.find_element(By.ID, 'download-button').click()

        try:
            os.mkdir('Music Folder')
        except FileExistsError :
            print('Music Folder alreay exists')
        
        #removes invalid characters from the video title
        video_title = video_title.replace('.', '-')
        video_title = video_title.replace('\\', '')
        video_title = video_title.replace('/', '')
        video_title = video_title.replace('?', '')
        video_title = video_title.replace('*', '')
        video_title = video_title.replace('"', '')
        video_title = video_title.replace('<', '')
        video_title = video_title.replace('>', '')
        video_title = video_title.replace('|', '')

        #name of the folder for the downloaded song. Will include mp3 and thumbnail jpg
        song_folder = f'{playlist_title} - ' + str(datetime.datetime.now()).replace(':', '-').replace('.', '-') 

        try:
            os.mkdir(f'Music Folder\{playlist_title}')
        except FileExistsError:
            #This should not happen!
            print('Song folder alreay exists')

        downloads_path = str(Path.home() / "Downloads") #path to the downloads folder
        song_download_path = f'{downloads_path}\youtube_{video_code}_audio.mp3' #path to the downloaded file.

        if is_file_downloaded(file_name=song_download_path, downloads_folder_path=downloads_path):
            #file is downloaded properly. Move it from downloads to the song folder.
            shutil.move(song_download_path, f'Music Folder\{playlist_title}\{video_title}.mp3')
        else:
            print('DOWNLOAD WAS NOT COMPLETE')
            driver.quit()
            
    driver.quit()