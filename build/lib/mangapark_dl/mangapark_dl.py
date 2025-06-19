import os
import shutil
import requests
from PIL import Image
from io import BytesIO
import sys
import argparse

from alive_progress import alive_bar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def main(): 
    parser = argparse.ArgumentParser(
        prog = 'mangapark-dl', 
        description='Downloads manga from mangapark v5.3 links',
    )

    parser.add_argument('link')
    parser.add_argument('-f', '--format', help="raw, zip, cbz, pdf")
    parser.add_argument('-p', '--path', help="The path in which the download directory should be created")
    parser.add_argument('--force-safari', '--safari', action="store_true", help='MAC ONLY. Force safari browser')
    parser.add_argument("-c", "--chapter",  help="downloads a chapter link instead of full manga. You must provide a chapter number as argument.")
    parser.add_argument("--no-cover", action="store_true", help="Skip the cover download. No effect in since chapter mode")
    parser.add_argument("-s", "--start", help='index (starts at 1) of the first chapter to download, if not provided will start at 1')
    parser.add_argument("-e", "--end", help="index (starts at 1) of the final chapter to download, if not provided defaults to last")
    parser.add_argument("--all-in-one", "--aio", action="store_true", help="Puts all pages downloaded into a single folder (raw)/file (all other formats)")

    args = parser.parse_args()

    src_url = args.link

    download_path = args.path
    if args.path == None: 
        download_path = os.getcwd()

    formats = ["raw", "zip", "cbz", "pdf"]
    try: format = args.format.strip().lower()
    except: pass
    if args.format == None or not (args.format.strip().lower() in formats):
        format = formats[1]

    if args.force_safari == False: 
        try: 
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable_cache")

            driver = webdriver.Chrome(service = Service(), options=chrome_options)

            #driver.get('chrome://settings/clearBrowserData')
            #driver.find_element(By.XPATH,'//settings-ui').send_keys(Keys.ENTER)
        except: 
            try: 
                options = webdriver.SafariOptions()
                driver = webdriver.Safari(options=options)
            except: 
                print("[ERROR] No supported browser detected, please install Chrome or Safari")
                sys.exit(0)
    else: 
        try: 
            options = webdriver.SafariOptions()
            driver = webdriver.Safari(options=options)
        except: 
            print("[ERROR] No supported browser detected, please install Chrome or Safari")
            sys.exit(0)

    def downloadImg(url: str, path: str, name: str): 
        # Download .webp image and converts to .png
        try: 
            response = requests.get(url)
            if response.status_code == 200: 
                webp_img = Image.open(BytesIO(response.content)).convert("RGBA")
                webp_img.save(path, 'PNG')
                print(f"[INFO] {name} saved as {path}")
            else: 
                print(f"[ERROR] Failed to download image. Status code: {response.status_code}")
        except Exception as e: 
            print(f"[ERROR] An error occured: {e}")

    def chapter_dl(link, no): 
        folder_path = os.path.join(download_path, title, f"Ch. {no}")
        if format != "raw" and os.path.exists(folder_path+"."+format):
            print(f"[INFO] Found chapter {no} already complete")
            return
        if format == "raw" and os.path.exists(os.path.join(folder_path, ".complete")): 
            print(f"[INFO] Found chapter {no} already complete")
            return
        page=driver.get(link)
        elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-name='image-item']//img"))
        )

        images = [image.get_attribute('src') for image in driver.find_elements(By.XPATH, "//div[@data-name='image-item']//img")]
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        with alive_bar(len(images), title=f"[INFO] Chapter {no} progress: ") as bar: 
            for i, image in enumerate(images): 
                if (not os.path.exists(os.path.join(folder_path, f"{i+1}.png"))):
                    downloadImg(image, os.path.join(folder_path, f"{i+1}.png"), f"page {i+1}")
                bar()
        if args.all_in_one == False: 
            if format=="cbz" or format=='zip': 
                try: os.remove(os.path.join(folder_path, ".complete"))
                except: pass
                shutil.make_archive(folder_path, "zip", folder_path)
                shutil.rmtree(folder_path)
                print("[INFO] Converted to ZIP")
                if format == 'cbz':
                    os.rename(folder_path+".zip", folder_path+".cbz")
                    print("[INFO] Converted to CBZ")
            elif format=="pdf": 
                try: os.remove(os.path.join(folder_path, ".complete"))
                except: pass
                images = []
                files = os.listdir(folder_path)
                files.sort()
                images = [Image.open(os.path.join(folder_path,f)) for f in files]
                del files
                pdf_path=folder_path+".pdf"
                images[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
                shutil.rmtree(folder_path)
                print("[INFO] Converted to PDF")
        if format=="raw": 
            with open(os.path.join(folder_path,".complete"), 'w'): 
                pass

    print("[INFO] Searching...")
    driver.get(src_url)


    if args.chapter==None: 
        title = driver.title.split(" - ")[0]
        print("[INFO] Found manga: " + title)

        elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@*[starts-with(name(), 'q:') and .='8t_8']]"))
        )
        chapter_links = driver.find_elements(By.XPATH, "//div[@*[starts-with(name(), 'q:') and .='8t_8']]")
        chapter_links = list(reversed([chapter.find_element(By.XPATH, ".//a").get_attribute('href') for chapter in chapter_links]))
        print(f"[INFO] Fetched {len(chapter_links)} chapters: " + title)

        if not os.path.isdir(os.path.join(download_path, title)):
            os.mkdir(os.path.join(download_path, title))
            print(f"[INFO] Created folder {os.path.join(download_path, title)}")
        else: 
             print(f"[INFO] Found folder {os.path.join(download_path, title)}")
        
        if (not args.no_cover) and (not os.path.isfile(os.path.join(download_path,title,"!cover.png"))): 
            elem = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//img"))
            )
            cover_link = driver.find_element(By.XPATH, "//img").get_attribute('src')
            print("[INFO] Downloading cover")
            downloadImg(cover_link, os.path.join(download_path, title, "!cover.png"), "cover")
        
        i = 1
        if args.start != None and args.end!= None: 
            print("wahoo")
            chapter_links = chapter_links[int(args.start)-1:int(args.end)]
            i=int(args.start)
        elif args.start != None and args.end == None: 
            chapter_links = chapter_links[int(args.start)-1:]
            i=int(args.start)
        elif args.start == None and args.end != None: 
            chapter_links = chapter_links[:int(args.end)]
        else: 
            pass
        print("[INFO] Downloading chapters...")
        for link in chapter_links:
            print(f"[INFO] Downloading chapter: {i}")
            chapter_dl(link, i)
            i+=1
        
        if format == "raw": 
            for chapter_folder in os.scandir(os.path.join(download_path, title)): 
                if os.path.isdir(chapter_folder) and os.path.exists(os.path.join(chapter_folder.path, ".complete")): 
                    os.remove(os.path.join(chapter_folder.path, ".complete"))

        if args.all_in_one == True:
            i=1
            for chapter_folder in os.scandir(os.path.join(download_path, title)): 
                if os.path.isdir(chapter_folder):
                    for img in os.scandir(chapter_folder): 
                        if img.name != ".complete":
                            os.rename(img.path, os.path.join(download_path, title, str(i)+"-"+img.name))
                    i+=1
                    shutil.rmtree(chapter_folder)
            if format == "cbz" or format == "zip":
                shutil.make_archive(os.path.join(download_path, title), "zip", os.path.join(download_path, title))
                shutil.rmtree(os.path.join(download_path, title))
                print("[INFO] Converted to ZIP")
                if format == 'cbz':
                    os.rename(os.path.join(download_path, title)+".zip", os.path.join(download_path, title)+".cbz")
                    print("[INFO] Converted to CBZ")
            elif format == 'pdf': 
                print("[INFO] Making PDF")
                images = []
                files = os.listdir(os.path.join(download_path, title))
                files.sort()
                for f in files: 
                    try: images.append(Image.open(os.path.join(download_path, title, f)))
                    except: pass
                del files
                pdf_path=os.path.join(download_path, title)+".pdf"
                images[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
                shutil.rmtree(os.path.join(download_path, title))
                print("[INFO] PDF Created")

    else: 
        title = driver.title.split(" - ")[0]
        print("[INFO] Found manga: " + title)
        if not os.path.isdir(os.path.join(download_path, title)):
            os.mkdir(os.path.join(download_path, title))
            print(f"[INFO] Created folder {os.path.join(download_path, title)}")
        else: 
             print(f"[INFO] Found folder {os.path.join(download_path, title)}")
        print("[INFO] Downloading chapter")
        chapter_dl(src_url, args.chapter)



    driver.quit()

    print("[INFO] Cleaning up...")

    try: 
        shutil.rmtree("chrome")
        shutil.rmtree("chromedriver")
    except: 
        pass

    print("[INFO] Donwload complete.")

if __name__=="__main__" :
    main()
