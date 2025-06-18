# mangapark-dl
 - A folder/cbz downloader for manga from mangapark v5.3. Uses chrome OR safari drivers via selenium.
 - This project is for educational purposes only. I do not condone piracy and am not affiliated with MangaPark in any way. 

## Installation
Tested on Python 3.9 and 3.13. 
Clone the repository and change into the directory. Optionally create a venv and run the command
```
git clone https://github.com/etashj/mangapark-dl
cd mangapark-dl
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
Use `python mangapark-dl.py --help` to view the help message.
```
usage: mangapark-dl [-h] [-f FORMAT] [-p PATH] [--force-safari] [-c CHAPTER] [--no-cover] [-s START] [-e END] link

Downloads manga from mangapark v5.3 links

positional arguments:
  link

options:
  -h, --help            show this help message and exit
  -f, --format FORMAT   raw, zip, cbz, pdf
  -p, --path PATH       The path in which the download directory should be created
  --force-safari, --safari
                        MAC ONLY. Force safari browser
  -c, --chapter CHAPTER
                        downloads a chapter link instead of full manga. You must provide a chapter number as argument.
  --no-cover            Skip the cover download. No effect in since chapter mode
  -s, --start START     index (starts at 1) of the first chapter to download, if not provided will start at 1
  -e, --end END         index (starts at 1) of the final chapter to download, if not provided defaults to last
  --all-in-one, --aio   Puts all pages downloaded into a single folder (raw)/file (all other formats)
```

For example, the following will download Yotsuba&! to `/Users/username/Documents/manga/Yotsuba&!` as cbz separated by chapter.
```
python mangapark-dl.py "https://mangapark.io/title/11684-en-yotsuba" -p "/Users/username/Documents/manga/" -f "cbz"
```
 - Note that the default option for path is the cwd and format defaults to cbz. Folder option gives you unzipped verzions of the cbz.
 - For safari usage, remote automation must be enabled and no headless mode is available.
 - Performance may be slow since page must be fully rendered (dynamic JS rendering) before downloads begin.
 - Chapter indices may not correspond to actual chapter numbers due to managpark's nonstandard naming conventions

