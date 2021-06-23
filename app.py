from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib
from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)



# By Deafult Flask will come into this when we run the file
@app.route('/')
def index():
    return ("index.html")  # Returns index.html file in templates folder.


# After clicking the Submit Button FLASK will come into this
def ebayed(url):
    try:
        r = Request(url,
                    headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1;+http://www.google.com/bot.html)'})
        web_url = urllib.request.urlopen(r)
        d = web_url.read().decode('utf-8', 'ignore')
        d = str(d)
        soup = BeautifulSoup(d, 'html.parser')

        listu1 = []
        bloggy = soup.select('#CenterPanel')
        for x in bloggy:
            name = x.find_all('h3', attrs={'class': 'item-info__title clearfix'})[0].text
            price = x.find_all('div', attrs={'class': 'item-info__price mot-price clearfix'})[0].text
            pic = x.select('#mainImgHldr')[0].find_all(id='icImg')[0]['src']
            a = pic.split('-')
            d = a[0] + '-l1600.png'
            pic = d
            g={'name':name,'price':price,'pic':pic,'url':url}
            listu1.append(g)
        return listu1

    except Exception as es:
        return str(es)


def amazed(url):
    try:
        r = Request(url,
                    headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1;+http://www.google.com/bot.html)'})
        web_url = urllib.request.urlopen(r)
        d = web_url.read().decode('utf-8', 'ignore')
        d = str(d)
        soup = BeautifulSoup(d, 'html.parser')

        listu = []
        bloggy = soup.select('#dp-container')

        for x in bloggy:
            name = x.select('#productTitle')[0].text.strip()
            image = x.select('#landingImage')[0]['data-old-hires']
            price = x.select('#priceblock_ourprice')[0].text
            try:
                price = price.split('-')
                price = price[0]
            except:
                pass

            g = {'name': name, 'price': price, 'pic':image, 'url': url}
            listu.append(g)
        return listu

    except Exception as es:
        return str(es)





@app.route('/api/', methods=['GET'])
@cross_origin()
def home():
    try:
        if 'url' in request.args:
            baseURL = str(request.args['url'])

        else:
            return "Error: No id field provided. Please specify an id."
       

        if 'ebay' in baseURL:
            kl=ebayed(baseURL)

            return jsonify(kl)
        elif 'amazon' in baseURL:
            pl=amazed(baseURL)

            return jsonify(pl)

        else:
            pass

    except Exception as es:


        return str(es)




if __name__ == '__main__':
    app.run(debug=True)


#if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port)