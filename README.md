# mangapark-dl
 - A folder/cbz downloader for manga from mangapark v5.3. Uses chrome OR safari drivers via selenium.
 - This project is for educational purposes only. I do not condone piracy. 

## Usage
Clone the repository and change into the directory. Optionally create a venv and run the command
```
pip install -r requirements.txt
```

Then use the following command to download manga
```
python mangapark-dl-py [link] --path [download path] --format [folder, cbz, zip, pdf]
```

For example, the following will download Yotsuba&! to `/Users/username/Documents/manga/Yotsuba&!` as cbz separated by chapter.
```
python mangapark-dl.py "https://mangapark.io/title/11684-en-yotsuba" -p "/Users/username/Documents/manga/" -f "cbz"
```
 - Note that the default option for path is the cwd and format defaults to cbz. Folder option gives you unzipped verzions of the cbz.
 - For safari usage, remote automation must be enabled and no headless mode is available.
 - Performance may be slow since page must be fully rendered (dynamic JS rendering) before downloads begin.

