import urllib2
from BeautifulSoup import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}

drug_name_store_price_map = {}

def getDrugForDisease(disease):

    req = urllib2.Request('https://www.goodrx.com/'+disease+'/drugs', headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    table = soup.findAll("table", {"class":"table-sortable"})
#print len(table)
    table = table[0].findAll("tbody", {"class":"table-sortable-row"})
    all_drug_names = []
    for each_row in table:
    #print each_row
        drug_name = each_row.findAll("div", {"class":"text-truncate-td"})
        span = drug_name[0].findAll("span")
        span = span[0]
        span = str(span).split(">")
        name = str(span[1])
        name = name.split("<")
        name = str(name[0])
    #print name
        all_drug_names.append(name)
    #break
    return all_drug_names

#print getDrugForDisease('fever')

def getDrugPrices(drug):
    req = urllib2.Request('https://www.goodrx.com/'+drug, headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    store_name = []
    prices = []
    try:
        div = soup.findAll("div", {"class":"price-wrap"})
        #print div
        div = div[0].findAll("div", {"class": "price-row -coupon "})
        for each_div in div:
            new_div_name = each_div.findAll("div", {"class": "store-name "})
            price_ind = each_div.findAll("div", {"class": "pricerow-drugprice"})
            price_ind = price_ind[0].findAll("span", {"class": "font-weight-medium"})
            name = str(new_div_name[0]).replace('\n', '')
            name = str(new_div_name[0]).split(">")
            name = name[1]
            name = name.split("<")
            #print name
            name = name[0]
            store_name.append(name.replace('\n', ''))
            span = price_ind[0]
            span = str(span).split(">")
            price = span[1]
            price = price[:-6]
            prices.append(price)
    except:
        div = soup.findAll("div", {"id":"otc-price-container"})
        div = div[0].findAll("div", {"class":"price-item"})
        for each_div in div:
            link = each_div.findAll("a")
            link = str(link[0]).split(" ")
            #print(link[1])
            link = link[1]
            link = link[6:-1]
            #print link
            price = each_div.findAll("span", {"class":"font-weight-medium"})
            price = price[0]
            price = str(price).split(">")
            price = price[1]
            price = price[:-6]
            #print price
            store_name.append(link)
            prices.append(price)
    #print store_name
    #print prices
    return store_name, prices

def getDrugStoresAndPrice(disease):
    drugs = getDrugForDisease(disease)
    for each_drug in drugs[:4]:
        drug_name_store_price_map[each_drug] = getDrugPrices(each_drug)

    return drug_name_store_price_map
