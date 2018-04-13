import requests
import bs4
import pandas as pd
import random
import time

# scraping date: Apr. 3rd 2018
url_list = []
baseurl_head = 'https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM/ref=cm_cr_arp_d_paging_btm_1?reviewerType=avp_only_reviews&pageNumber='
baseurl_end = '&sortBy=recent'
for i in list(range(1,80)):
    url = baseurl_head + str(i) + baseurl_end
    url_list.append(url)


review_list = []
headers = {'user-agent': 'my-app/0.0.1'}
for url in url_list:
    soup = bs4.BeautifulSoup(requests.get(url, headers=headers, ).text, 'html5lib')
    review_div = soup.find_all('div', attrs={'data-hook': 'review'})

    for index, review in enumerate(review_div):
        detail = []
        try:
            rate = review.find('i', attrs={'data-hook': 'review-star-rating'}).text.strip()
            review_title = review.find('a', attrs={'data-hook': 'review-title'}).text.strip()
            author = review.find('a', attrs={'data-hook': 'review-author'}).text.strip()
            date = review.find('span', attrs={'data-hook': 'review-date'}).text.strip()
            review_format = review.find('a', attrs={'data-hook': 'format-strip'}).text.strip()
            declarative = review.find('a', attrs={'data-reftag': 'cm_cr_arp_d_rvw_rvwer'}).text.strip()
            review_body = review.find('span', attrs={'data-hook': 'review-body'}).text.strip()
            image_y_or_no = review.find('div', attrs={'class': 'review-image-tile-section '})
            if image_y_or_no:
                image = True
            else:
                image = False
        except Exception as e:
            print(index)

        detail = [author, review_title, rate, date, review_format, declarative, review_body, image]

        review_list.append(detail)
        random_delay = random.normalvariate(2, 0.5)
        time.sleep(random_delay)


header = ['author', 'review_title', 'rate', 'date', 'review_format', 'declarative', 'review_body', 'image']
df_amazon = pd.DataFrame(review_list, columns=header)

df_amazon.to_json('reviews.json', orient='records')