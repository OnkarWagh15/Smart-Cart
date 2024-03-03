import ssl
import requests
import pandas as pd
import streamlit as st
from urllib import request
from bs4 import BeautifulSoup

dfPrimary = pd.DataFrame()

def writeToExcel(df):
    global dfPrimary  
    dfPrimary = pd.concat([dfPrimary, df], ignore_index=True, axis=0)
    dfPrimary.to_csv("ProductDetails.csv", index=False)
       
def CrawlAmazon(amazon):

    header = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    
    web = requests.get(amazon, headers= header)
    # print(amazon)
    print(web)
    soup =  BeautifulSoup(web.content, 'lxml')

    names = []
    prices = []
    ratings = []
    estTime = []
    links = []

    blockcontent = soup.find_all("div", class_="a-section a-spacing-base")
    if blockcontent:
        for block in blockcontent:
                namecontent = block.find("span", class_="a-size-base-plus a-color-base a-text-normal")
                if namecontent:
                    names.append(namecontent.text)

                    ratingContent = block.find("span", class_="a-icon-alt")
                    if ratingContent:
                        ratings.append(ratingContent.string[:3])
                    else:
                        ratings.append('NA')

                    linkcontent = block.find("a", class_="a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal")
                    if linkcontent:
                        links.append("https://www.amazon.in" + linkcontent.get("href"))
                    else:
                        links.append('NA')

                    pricecontent = block.find("span", class_="a-offscreen")
                    if pricecontent:
                        price_str = pricecontent.text.replace('₹', '').replace(',', '')  
                        try:
                            price = int(price_str)
                            prices.append(price)
                        except ValueError:
                            prices.append('NA')
                    else:
                        prices.append('NA')

                    timecontent = block.find("span", class_="a-color-base a-text-bold")
                    if timecontent:
                        estTime.append(timecontent.string)
                    else:
                        estTime.append('NA')
    else:
        blockcontent = soup.find_all("div", class_="a-section")
        if blockcontent:
            for block in blockcontent:
                namecontent = block.find("span", class_="a-size-base-plus a-color-base a-text-normal")
                if namecontent:
                    names.append(namecontent.text)
                    ratingContent = block.find("span", class_="a-icon-alt")
                    if ratingContent:
                        ratings.append(ratingContent.string[:3])
                    else:
                        ratings.append('NA')

                    linkcontent = block.find("a", class_="a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal")
                    if linkcontent:
                        links.append("https://www.amazon.in" + linkcontent.get("href"))
                    else:
                        links.append('NA')

                    pricecontent = block.find("span", class_="a-offscreen")
                    if pricecontent:
                        price_str = pricecontent.text.replace('₹', '').replace(',', '')  
                        try:
                            price = int(price_str)
                            prices.append(price)
                        except ValueError:
                            prices.append('NA')
                    else:
                        prices.append('NA')

                    timecontent = block.find("span", class_="a-color-base a-text-bold")
                    if timecontent:
                        estTime.append(timecontent.string)
                    else:
                        estTime.append('NA')

    min_length = min(len(names), len(prices), len(ratings), len(estTime), len(links))
    names = names[:min_length]
    prices = prices[:min_length]
    ratings = ratings[:min_length]
    estTime = estTime[:min_length]
    links = links[:min_length]

    df = pd.DataFrame({
                        'Name': names,
                        'Price' : prices,
                        'Ratings' : ratings,
                        'Time' : estTime,
                        'Link' : links})
    
    # print(df)
    if df.empty:
        CrawlAmazon(amazon)
    writeToExcel(df)
    print("Data found from Amazon")
    
def crawlFlipkart(flipkart):   
   
    web = requests.get(flipkart)
    print(flipkart)
    print(web)
    soup =  BeautifulSoup(web.content,"html.parser")

    names = []
    prices = []
    ratings = []
    estTime = []
    links = []

    blockContent = soup.find_all("div", class_="_2kHMtA")
    if(blockContent):
        for block in blockContent:
            if (block):
                namecontent = block.find("div", class_="_4rR01T")
                if namecontent:
                    names.append(namecontent.text)

                    ratingContent = block.find("div", class_="_3LWZlK")
                    if ratingContent:
                        ratings.append(ratingContent.text)
                    
                    else:
                        ratings.append('NA')

                    linkcontent = block.find("a", class_="_1fQZEK")
                    if linkcontent:
                        links.append("https://www.flipkart.com" + linkcontent.get("href"))
                    else:
                        links.append('NA')

                    pricecontent = block.find("div", class_="_30jeq3 _1_WHN1")
                    if pricecontent:
                        price_str = pricecontent.text.replace('₹', '').replace(',', '')  
                        try:
                            price = int(price_str)
                            prices.append(price)
                        except ValueError:
                            prices.append('NA')
                    else:
                        prices.append('NA')

                    tempvar = links[len(links) - 1]
                    if(tempvar != "NA"):
                        tempweb = requests.get(tempvar)
                        tempsoup = BeautifulSoup(tempweb.content, "lxml")
                        timecontent = tempsoup.find("span", class_="_1TPvTK")
                        if timecontent:
                            estTime.append(timecontent.text)
                        else:
                            estTime.append('NA')
    else:
        blockContent = soup.find_all("div", class_="_4ddWXP") 
        if(blockContent):
            for block in blockContent:
                if (block):
                    namecontent = block.find("a", class_="s1Q9rs")
                    if namecontent:
                        names.append(namecontent.text)

                        ratingContent = block.find("div", class_="_3LWZlK")
                        if ratingContent:
                            ratings.append(ratingContent.text)
                        
                        else:
                            ratings.append('NA')

                        linkcontent = block.find("a", class_="s1Q9rs")
                        if linkcontent:
                            links.append("https://www.flipkart.com" + linkcontent.get("href"))
                        else:
                            links.append('NA')

                        pricecontent = block.find("div", class_="_30jeq3")
                        if pricecontent:
                            price_str = pricecontent.text.replace('₹', '').replace(',', '')  
                            try:
                                price = int(price_str)
                                prices.append(price)
                            except ValueError:
                                prices.append('NA')
                        else:
                            prices.append('NA')

                        tempvar = links[len(links) - 1]
                        if(tempvar != "NA"):
                            tempweb = requests.get(tempvar)
                            tempsoup = BeautifulSoup(tempweb.content, "lxml")
                            timecontent = tempsoup.find("span", class_="_1TPvTK")
                            if timecontent:
                                estTime.append(timecontent.text)
                            else:
                                estTime.append('NA')

    min_length = min(len(names), len(prices), len(ratings), len(estTime), len(links))
    names = names[:min_length]
    prices = prices[:min_length]
    ratings = ratings[:min_length]
    estTime = estTime[:min_length]
    links = links[:min_length]

    df = pd.DataFrame({
                        'Name': names,
                        'Price' : prices,
                        'Ratings' : ratings,
                        'Time' : estTime,
                        'Link' : links})
    
    # print(df)
    writeToExcel(df)
    print("Data found from Flipkart")

def crawlSnapdeal(snapdeal): 

    header = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    
    web = requests.get(snapdeal, headers= header)
    print(snapdeal)
    soup =  BeautifulSoup(web.content, 'lxml')

    names = []
    prices = []
    ratings = []
    estTime = []
    links = []

    linkcontent = soup.findAll("a", class_="dp-widget-link noUdLine")
    for i in range(0, len(linkcontent), 2):
        href = linkcontent[i].get('href')
        if href:
            tempweb = requests.get(href)
            tempsoup = BeautifulSoup(tempweb.content,"lxml")
            namecontent = tempsoup.find("div", class_="col-xs-22")
            if namecontent:
                # print(namecontent)
                names.append(namecontent.text.strip())
            else:
                names.append("NA")
   
            pricecontent = tempsoup.find("span", class_="payBlkBig")
            if pricecontent:
                prices.append(pricecontent.text)
            else:
                prices.append("NA")
    
            ratingContent = tempsoup.find("span", class_="avrg-rating")
            if (ratingContent):
                ratings.append(ratingContent.string[1:-1])
            else:
                ratings.append("NA")

            timecontent = tempsoup.find('p', class_="expect-delvry")
            if timecontent:
                estTime.append(' '.join(timecontent.stripped_strings))
            else:
                estTime.append("NA")

            links.append(href)
    
    min_length = min(len(names), len(prices), len(ratings), len(estTime),len(links))
    names = names[:min_length]
    prices = prices[:min_length]
    ratings = ratings[:min_length]
    estTime = estTime[:min_length]
    links = links[:min_length]
    df = pd.DataFrame({
                
                        'Name': names,
                        'Price' : prices,
                        'Ratings' : ratings,
                        'Time' : estTime,
                        'Link' : links,
                        })
    
    # print(df)
    writeToExcel(df)
    print("Data found from Snapdeal")

def crawlAlibaba(Alibaba):   

    header = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
   
    web = requests.get(Alibaba, headers= header)
    # print(Alibaba)
    soup =  BeautifulSoup(web.content,"html.parser")

    names = []
    prices = []
    ratings = []
    estTime = []
    links = []

    blockcontent = soup.find_all("div", class_="product-card-gallery product-card")
    if blockcontent:
        for block in blockcontent:
            linkcontent = block.find("a", class_="product-image")
            specificLink = ""
            if linkcontent:
                href = linkcontent.get('href')  
                if href:
                    specificLink = "https:" + href + "+india.html"
            else:
                links.append('NA')

            ratingContent = block.find("div", class_="product-review-score")

            if(specificLink):
                tempweb = requests.get(specificLink)
                tempsoup = BeautifulSoup(tempweb.content, "lxml")
        
                namecontent = tempsoup.find("div", class_="product-title-container")
                if namecontent:
                    names.append(namecontent.text)
                   
                    if ratingContent:
                        ratings.append(ratingContent.text)
                    else:
                        ratings.append('NA')

                    pricecontent = tempsoup.find("div", class_="price")
                    if pricecontent:
                            prices.append(pricecontent.text)
                    else:
                        prices.append('NA')
                    
                    estTime.append("NA")
                    links.append(specificLink)

    min_length = min(len(names), len(prices), len(ratings), len(estTime), len(links))
    names = names[:min_length]
    prices = prices[:min_length]
    ratings = ratings[:min_length]
    estTime = estTime[:min_length]
    links = links[:min_length]
    df = pd.DataFrame({
                       
                        'Name': names,
                        'Price' : prices,
                        'Ratings' : ratings,
                        'Time' : estTime,
                        'Link' : links})
    
    # print(df)
    writeToExcel(df)
    print("Data found from Alibaba")
    
def urlFormation(product, specsList):
    
    amazon = ""
    amazon = amazon + "https://www.amazon.in/s?k=" + product
    
    flipkart = ""
    flipkart = flipkart + "https://www.flipkart.com/search?q=" + product

    snapdeal = ""
    snapdeal = snapdeal + "https://www.snapdeal.com/search?keyword="  + product
    
    alibaba = ""
    alibaba = alibaba +  "https://www.alibaba.com/showroom/" + product

    for i in specsList:
        amazon += '+' + i
        snapdeal += '+' + i
        alibaba += '+' + i
        flipkart += '+' + i

    CrawlAmazon(amazon)
    crawlFlipkart(flipkart)
    crawlSnapdeal(snapdeal)
    alibaba = alibaba + "+india.html"
    crawlAlibaba(alibaba)

def crawling():
    product = st.text_input("Enter Product")
    product = product.replace(" ","+")

    specs = st.text_input("Enter specifications : ( colon separated ) ")

    specsList = []
    specs = specs.replace(": ", "" ).replace(" ", "+").replace("\t", "+").replace("\n", "+")
    specsList = specs.split(";")
    
    if st.button("Search", type = "primary"):
        urlFormation(product, specsList)
   
    
crawling()

