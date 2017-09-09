from icrawler.builtin import GoogleImageCrawler
import datetime
import os
import random

#get wallpaper from google images
def setWallpaper(searchTerms, wallpaperPath, numResults, size):
    if os.path.exists(wallpaperPath):
        try:
            if (size == "huge"):
                x,y = 1920,1200

            google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4,
                                                storage={'root_dir': wallpaperPath})
            google_crawler.crawl(keyword=searchTerms, max_num=numResults,
                                 date_min=None, date_max=None,
                                 min_size=(x,y), max_size=None)
            displayWallpaper(wallpaperPath)
        except:
            print("unable to fetch new wallpapers")

# set desktop background picture
def displayWallpaper(wallpaperPath):
    path, dirs, files = os.walk(wallpaperPath).__next__()
    fileName = wallpaperPath + random.choice(files)

    ## This works for ONE desktop
    try:
        from appscript import app, mactypes
        finder = app('Finder')
        finder.desktop_picture.set(mactypes.File(fileName))
    except:
        print("unable to update wallpaper")
