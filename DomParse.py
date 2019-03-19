# CS288 Homework 9
# Read the skeleton code carefully and try to follow the structure
# You may modify the code but try to stay within the framework.

import libxml2
import sys
import os
import commands
import re
import sys

import MySQLdb

from xml.dom.minidom import parse, parseString

# for converting dict to xml 
from cStringIO import StringIO
from xml.parsers import expat

def get_elms_for_atr_val(tag,atr,val):
   lst=[]
   elms = dom.getElementsByTagName(tag)
   for node in elms:
      for atrN, atrV in node.attributes.items():
         if atrN == atr and atrV == val:
            lst = list(filter(lambda x: x.nodeType == 1, node.childNodes))
    
   # ............

   return lst

# get all text recursively to the bottom
def get_text(e):
   lst = []
   if e.nodeType in (3, 4):
      if not e.data.isspace():
         lst.append(e.data)
   else:
      for x in e.childNodes:
         lst = lst + get_text(x)
   
   # ............
   return lst

# replace whitespace chars
def replace_white_space(str):
   p = re.compile(r'\s+')
   new = p.sub(' ',str)   # a lot of \n\t\t\t\t\t\t
   return new.strip()

# replace but these chars including ':'
def replace_non_alpha_numeric(s):
   p = re.compile(r'[^a-zA-Z0-9:-]+')
   #   p = re.compile(r'\W+') # replace whitespace chars
   new = p.sub(' ',s)
   return new.strip()

# convert to xhtml
# use: java -jar tagsoup-1.2.jar --files html_file
def html_to_xml(fn):
   xhtml_file = os.system('/home/g00dz/Desktop/hw9/ java -jar tagsoup-1.2.1.jar --files %s' % (fn))
   fn = fn.replace('.html', '.xhtml')
   # ............
   return fn

def extract_values(dm):
   lst = []
   temp = []
   l = get_elms_for_atr_val('table', 'class', 'mdcTable') # list or trs
   l.pop(0)
   for trs in l:
      tds = list(filter(lambda x: x.nodeType == 1, trs.childNodes))
      for td in tds:
         item = get_text(td)
         temp.append(item[0].replace('\n', ''))
      lst.append(to_dict(temp))
      temp = []

   # ............
   #    get_text(e)
   # ............
   return lst

# mysql> describe most_active;
def insert_to_db(l,tbl):
   dbconn = MySQLdb.connect(host="localhost", user="root", passwd="")
   cursor = dbconn.cursor()
   sql = "CREATE DATABASE IF NOT EXISTS todaysStocks"
   cursor.execute(sql)
   db = MySQLdb.connect(host="localhost", user="root", passwd="", db="todaysStocks")
   c = db.cursor()
   c.execute("""CREATE TABLE IF NOT EXISTS `%s` (
   `rank` VARCHAR(50),
   `title` VARCHAR(255),
   `volume` VARCHAR(50),
   `price` VARCHAR(50),
   `cng` VARCHAR(50),
   `perc_cng` VARCHAR(50)
   )""" % (tbl))

   for d in l:
      query = """INSERT INTO `%s` (rank, title, volume, price, cng, perc_cng) VALUES ("%s", "%s", "%s", "%s", "%s", "%s");""" % (tbl, d['rank'], d['title'], d['volume'], d['price'], d['cng'], d['perc_cng'])
      #print query
      c.execute(query)
      db.commit()
   c.close()
   db.close()
   return
   # ............

# show databases;
# show tables;

def to_dict(l):
   keys = ['rank', 'title', 'volume', 'price', 'cng', 'perc_cng']
   d = []
   d.append(dict(zip(keys, l)))

   return d

def main():
   html_fn = sys.argv[1]
   fn = html_fn.replace('.html','')
   xhtml_fn = html_to_xml(html_fn)

   global dom
   dom = parse(xhtml_fn)

   lst = extract_values(dom)

   # make sure your mysql server is up and running
   for stocks in lst:
      cursor = insert_to_db(stocks,fn) # fn = table name for mysql

   #l = select_from_db(cursor,fn) # display the table on the screen

   # make sure the Apache web server is up and running
   # write a PHP script to display the table(s) on your browser

   return True
# end of main()

if __name__ == "__main__":
    main()

# end of hw7.py
