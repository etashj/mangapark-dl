# mangapark-rl

A folder/cbz downloader for manga from mangapark. 

## Usage
Clone the repository and change into the directory. Optionally create a venv and run the command
```
pip install -r requirements.txt```

Then use the following command to download manga
```
python mangapark-dl.py [link] --path [download path] --format [folder, cbz]
```

For example, the following will download Yotsuba&! to `/Users/username/Documents/manga/Yotsuba&!` as .cbz separated by chapter. 
```
python mangapark-dl.py "https://mangapark.io/title/11684-en-yotsuba" -p "/Users/username/Documents/manga/" -f "cbz"```

Note that the default option for path is the cwd and format defaults to cbz. Folder option gives you unzipped verzions of the cbz. 
