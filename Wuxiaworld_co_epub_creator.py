#Python 3.9
# #install EbookLib 
#install beautifulsoup4
#install requests
#install tqdm
#install lxml

#ayooo
# importing libraries
import requests
from bs4 import BeautifulSoup
import re
import os
import ebooklib
from ebooklib import epub
from tqdm import tqdm
import urllib.request

table = [] #useful for making Table of contents (TOC)

#------------------enter your URL here-------------------------------
# make sure its from wuxiaworld.co and not wuxiaworld.com
url = "https://www.wuxiaworld.co/My-Vampire-System/" #url of the chapter


#extract links 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
content = requests.get(url, headers = headers)
soup = BeautifulSoup (content.text, 'html.parser')
links =  soup.find_all("a", {"class": "chapter-item"}) #all the links here

#creating EPUB
book = epub.EpubBook()
book.set_language('en')

#adding Author name
author = soup.find("span", {"class": "name"})
author = BeautifulSoup (author.text, 'html.parser')
author = str(author.get_text())
book.add_author(author)

#adding Title name
titleOfBook = soup.find("div", {"class": "book-name"})
titleOfBook = BeautifulSoup (titleOfBook.text, 'html.parser')
titleOfBook = str(titleOfBook.get_text())
book.set_title(titleOfBook)

#adding Cover image
imgurl = soup.find("img", {"class": "bg-img"})
imgurl = imgurl.attrs['src']
urllib.request.urlretrieve(imgurl, "cover.jpg")
book.set_cover("cover.jpg", open('cover.jpg', 'rb').read())
os.remove("cover.jpg")

#adding spine = important
book.spine = ['cover','nav']

#loop
for url in tqdm(links):
 
 # making the URL for content extraction
 url = url.attrs['href']
 url = "https://www.wuxiaworld.co"+ url

 #Extract all data from Chapter
 headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
 content = requests.get(url, headers = headers)
 soup = BeautifulSoup (content.text, 'html.parser')
 
 #Extract Title and contents of chapter
 head = str(soup.find_all('h1',class_='chapter-title'))
 para = str(soup.find_all('div',class_='chapter-entity'))
 head = head[1:len(head)-1]
 start = 'Please go to <a href="https://www.readlightnovel.cc/'
 para = para[1:para.find(start)]
 
 #Making xhtml data
 a = """<?xml version="1.0" encoding="utf-8"?>
 <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
 "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
 
 <html xmlns="http://www.w3.org/1999/xhtml">
 <head>
 <title></title>
 </head>
 
 <body>"""

 b = """</div></body>
 </html>"""

 #making nake for xhtml files
 title = BeautifulSoup(head, 'html.parser')
 title = str(title.get_text())
 title = re.sub(r'[^A-Za-z0-9 ]+', '', title)
 content = a + head + para + b
 
 #writing in xhtml
 content = content.encode(encoding='UTF-8',errors='ignore')
 c = epub.EpubHtml(title= title,
                   file_name=title + '.xhtml',
                   lang='en')
 c.set_content(content)
 book.add_item(c)

 #for TOC
 table.append(c)

 #adding to spine important
 book.spine.append(c)

# adding TOC
book.toc = (epub.Link('nav.xhtml', titleOfBook, 'nav'),
           (epub.Section('book'),
           (table))
           )

#Make Epub
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
epub.write_epub( titleOfBook + '.epub', book, {})

#Successful
print ("your book is ready")
 
 
