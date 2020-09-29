import requests
import re
import csv
import threading
import time
import json
import random
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed


class Thread(threading.Thread):
    def __init__(self, keyword):
        threading.Thread.__init__(self)
        self.keyword = keyword

    def run(self):
        print("Starting to work on keyword: " + self.keyword)
        # Get lock to synchronize threads
        threadLock.acquire()
        main(self.keyword)
        # Free lock to release next thread
        threadLock.release()


def get_list(keyword):
    index = 0
    links = []
    url = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CategoryProductsListingView?langId=-1&storeId=10051&catalogId=10051&advancedSearch=&sType=SimpleSearch&categoryId=&searchType=1002&facet=&searchTermScope=&searchTerm={}&metaData=&resultCatEntryType=2&filterFacet=&manufacturer=&emsName=&gridPosition=&resultsPerPage=15&minPrice=&maxPrice=&sortBy=5&disableProductCompare=false&ajaxStoreImageDir=%2fwcsstore%2fWineandSpirits%2f&filterTerm=&variety=&categoryType=&enableSKUListView=&ddkey=ProductListingView'.format(keyword)

    s = requests.session()

    headers = {
        'Cookie': '_vuid=94cd8abe-8679-426e-9c4c-e66bd6d9079d; cookiesession1=678B2874QRSTUVWXYZABCDEFGHIL6C24; WC_PERSISTENT=%2BMWu5a8u8i02wDsDFgKxq04BspU%3D%0A%3B2020-09-25+07%3A21%3A25.749_1601032885747-40057_10051; _gcl_au=1.1.456110338.1601032889; _ga=GA1.2.1006974790.1601032890; ltkmodal-suppression-5fef5c3e-56c8-407a-9dde-7d5faa45e006=Sun%20Oct%2025%202020%2019%3A21%3A37%20GMT%2B0800%20(China%20Standard%20Time); GSIDyk8q9gLSz40L=6fbacabb-0274-4485-96dc-8bd09df93108; STSID148379=37c2a1ff-9ee4-4954-8be3-db4e8617e706; WC_SESSION_ESTABLISHED=true; WC_ACTIVEPOINTER=-1%2C10051; _gid=GA1.2.44085969.1601218938; AGEVERIFY=Over21; ltkSubscriber-Footer=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9; ltkSubscriber-AccountCreate=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9; priceMode=1; JSESSIONID=0000h8ZYy-nauzyFZqycomOQ5DZ:163j897n8; _genesys.widgets.webchat.metaData={%22proactive%22:false%2C%22prefilled%22:false%2C%22autoSubmitted%22:false%2C%22coBrowseInitiated%22:false%2C%22filesUploaded%22:0%2C%22numAgents%22:0%2C%22userMessages%22:0%2C%22agentMessages%22:0%2C%22systemMessages%22:0%2C%22errors%22:false%2C%22opened%22:false%2C%22started%22:false%2C%22cancelled%22:false%2C%22completed%22:false%2C%22closed%22:false%2C%22elapsed%22:1601257128682%2C%22waitingForAgent%22:false%2C%22agentReached%22:false%2C%22supervisorReached%22:false%2C%22form%22:{}}; WC_AUTHENTICATION_16598728=16598728%2CAoF3CXt8PD4j%2BQQwLv6or0OioWc%3D; WC_USERACTIVITY_16598728=16598728%2C10051%2Cnull%2Cnull%2C1601257129601%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2CFfIr%2BxWQLcbhrz%2FYvgRUoZD81vuPedMYNn9RNAZga8xusJZShI8szIKfLefUvC26X%2FC0WnWmuJePwONa6H4c6jMCDzB20Zkn%2BAZrMVUhrhE0sSstxgzSJg1qDp6wn8Ib6Daz6J%2FSysAE8vm8pS3zHcnJRPsJPhzJSUDVUFYJsBZqZBkIWQKu90oeVKz4JxhE2ENgecdsil0J4nBjxF99F369VCbqD61A7uLHRYuuMEo%3D; ltkpopup-session-depth=4-1; JSESSIONID=0000emumR2EcnOCjB-M1gM1fywm:163j89nib; WC_SESSION_ESTABLISHED=true; WC_PERSISTENT=QZ58LXaGWJe07ZaatyoJe8sBNI8%3D%0A%3B2020-09-27+21%3A32%3A04.852_1601256724838-783115_10051; WC_ACTIVEPOINTER=-1%2C10051; priceMode=1; cookiesession1=678B2874UVWXZABCDEFGHIJNOPQR8E30',
        'Referer': 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/SearchResultsView?categoryId=&storeId=10051&catalogId=10051&langId=-1&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&variety=&pageView=&beginIndex=0&pageSize=15&sortBy=5&searchTerm=Single+Malt&SearchKeyWord=Single+Malt',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    while True:
        data = {
            'contentBeginIndex': 0,
            'productBeginIndex': index,
            'beginIndex': index,
            'orderBy': '',
            'facetId': '1000179110108105110101',
            'facetId': '1000279110108105110101326912099108117115105118101',
            'pageView': '',
            'resultType': 'products',
            'orderByContent': '',
            'searchTerm': '',
            'facet': 'ads_f10001_ntk_cs:"Online"',
            'facet': 'ads_f10002_ntk_cs:"Online+Exclusive"',
            'facetLimit': '',
            'minPrice': '',
            'maxPrice': '',
            'pageSize': '',
            'storeId': '10051',
            'catalogId': '10051',
            'langId': -1,
            'categoryId': '',
            'objectId': '',
            'requesttype': 'ajax'
        }

        res = s.post(url=url, headers=headers, data=data)
        soup = BeautifulSoup(res.text, 'html5lib')
        cards = soup.select('.catalog_item')
        if cards:
            index = index + 15
            for card in cards:
                title = card.find_all('a')[1].text.strip()
                util = card.find_all('a')[0]['href']
                store_id = re.search('storeId=(.*)&productId=', util).group(1)
                product_id = re.search('productId=(.*)&langId=', util).group(1)
                link = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/ProductDisplay?storeId={}&productId={}&&errorViewName=ProductDisplayErrorView'.format(store_id, product_id)
                image = 'https://www.finewineandgoodspirits.com' + card.find_all('a')[0].img['src']
                volume = card.select('.item > div:nth-child(4)')[0].text.replace('\n', '').strip().split(' ')[0] + ' ML'
                price = card.find(attrs={'class': 'catalog_item_price'}).text.strip()
                line = [title, link, image, volume, price]
                links.append(line)
        else:
            break
    return links


def read_file():
    with open(file='./whisky_keyword.csv', encoding='utf-8', mode='r') as file:
        return file.readlines()


def main(keyword):
    keyword = keyword.strip()
    links = get_list(keyword)
    for k, link in enumerate(links):
        start_time = time.time()
        while True:
            webhook = DiscordWebhook(url=webhook_url)

            # create embed object for webhook
            embed = DiscordEmbed(title=link[0], description=link[1], color=242424)

            # set author
            embed.set_author(name='Amira', url='https://www.freelancer.com/u/amiratarbout96', icon_url='https://cdn2.f-cdn.com/ppic/159713777/logo/47568275/profile_logo_47568275.jpg')

            # set image
            embed.set_image(url=link[2])

            # set thumbnail
            embed.set_thumbnail(url='https://cdn5.f-cdn.com/ppic/57665018/logo/7568749/profile_logo_7568749.jpg')

            # set footer
            embed.set_footer(text=keyword)

            # set timestamp (default is now)
            embed.set_timestamp()

            # add fields to embed
            embed.add_embed_field(name='Volume', value=link[3].strip())
            embed.add_embed_field(name='Price', value=link[4].strip())

            # add embed object to webhook
            webhook.add_embed(embed)
            res = webhook.execute()
            if res.status_code == 204:
                print('{} item of {} items on keyword: {}'.format(k, len(links), keyword))
                break
            elif res.status_code == 429:
                retry_time = int(json.loads(res.text)['retry_after'])/1000
                print('Waiting... | {} seconds'.format(retry_time))
                time.sleep(retry_time)
                continue
            elif time.time() - start_time > 120:
                print('Failed. Go to next item...')
                break
            else:
                print('Waiting for static time... {} seconds'.format(5))
                time.sleep(5)

    Thread(keyword).start()


if __name__ == '__main__':

    # webhook_url = 'https://discord.com/api/webhooks/760022646648864788/079nyGnh3h66L16jUTb-U9rjBN7WtbY9qBUyFPDG_FHX8-FOYFeLXgLv8l0NdX-_PupC'
    webhook_url = 'https://discordapp.com/api/webhooks/759064586908336168/qODSpqFZhqsbw-9-qYHh7InBPqA3i0eFCusbePRfqI3vRh92ByKfBOGzkI9w8kX41s1R'

    keywords = read_file()

    threadLock = threading.Lock()

    for key in keywords:
        Thread(key).start()
