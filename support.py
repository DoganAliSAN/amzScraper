from amazoncaptcha import AmazonCaptcha
from seleniumbase import BaseCase
import datetime
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs
from requests_html import HTMLSession
def captcha(self,):
    self.open('https://www.amazon.com/errors/validateCaptcha')
    solution = "not"
    while "not" in solution.lower():
        self.reload()
        selector = "body"
        element = self.wait_for_element_visible(selector)
        height = element.size["height"]
        self.set_window_size(1920, height)
        img_name = f"test{datetime.datetime.now()}.png"
        self.save_element_as_image_file(selector, img_name, "images")
        captcha = AmazonCaptcha.fromdriver(self, png=f"images/{img_name}")
        solution = captcha.solve()
        print(solution)

    self.type('//*[@id="captchacharacters"]', solution + "\n")
def change_zone():

    self.wait_for_element_visible('//*[@id="nav-global-location-popover-link"]').click()
    self.type('//*[@id="GLUXZipUpdateInput"]', '20010')
    self.wait_for_element_visible('//*[@id="GLUXZipUpdate"]').click()
    self.reload()
def get_reviews(asin):
    reviews_page = 1
    reviews = []

    while len(reviews) < 100:
        url_review = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_srt?sortBy=recent&pageNumber={str(reviews_page)}"
        self.open(url_review)
        html_reviews = self.get_page_source()
        soup_reviews = bs(html_reviews, 'html.parser')
        review_containers = soup_reviews.find_all('div', {'data-hook': 'review'})
        if len(review_containers) == 0:
            break
        for container in review_containers:
            #get verifed purchase badge and if veried make a variable named verified and make it true 
            verified = False
            if self.is_element_present('//*[@id="avp-badge"]'):
                verified = True
            title_element = container.find('a', {'data-hook': 'review-title'})
            if title_element is not None:
                title = title_element.find_all('span')[2].text.strip()
            else:
                title = None
            date_element = container.find('span', {'data-hook': 'review-date'})
            date = date_element.text.strip() if date_element is not None else None
            rating_element = container.find('i', {'data-hook': 'review-star-rating'})
            if rating_element is not None:
                rating = rating_element.text.strip()
            else:
                rating_element = container.find('i', {'data-hook': 'cmps-review-star-rating'})
            body_element = container.find('span', {'data-hook': 'review-body'})
            body = body_element.text.strip() if body_element is not None else None
            name_element = container.find('span', {'class': 'a-profile-name'})
            name = name_element.text.strip() if name_element is not None else None
            # Create review dictionary
            review = {
                'title': title,
                'date': date,
                'rating': rating[0],
                'body': body,
                'name': name,
                'asin': asin,
                'url': url_review,
                'verified': verified
            }
            # Add the review to the list
            reviews.append(review)
        reviews_page += 1
    return reviews
    
def needed_values(self, subcategory, current_category, keywords, page_count):
    self.open(f"https://www.amazon.com/s?k={keywords}&page={page_count}")
    self.wait_for_element_clickable('/html/body/div[1]/div[1]/div[1]/div[2]/div/div[3]/span/div/div/div/div[2]/ul/span/li/span/a/div[1]/label/i')
    self.click('/html/body/div[1]/div[1]/div[1]/div[2]/div/div[3]/span/div/div/div/div[2]/ul/span/li/span/a/div[1]/label/i')
    self.wait_for_element_clickable('//*[@id="s-result-sort-select"]/option[6]')
    self.click('//*[@id="s-result-sort-select"]/option[6]')
    
    html = self.find_element('//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]').get_attribute('innerHTML')
    soup = bs(html, 'html.parser')
    elements = soup.find_all(attrs={"data-index": True})
    
    products = []
    for element in elements:
        h2_tags = element.find_all("h2")
        for h2_tag in h2_tags:
            url = "https://www.amazon.com/" + h2_tag.select_one("a").get("href")
            self.open(url)
            html = self.get_page_source()
            soup = bs(html, 'html.parser')
            form = soup.find('div', id='twisterContainer')
            
            if not form:
                if self.is_element_present("select[name='quantity'] option:last-child"):
                    quantity = self.find_element("select[name='quantity'] option:last-child").text
                else:
                    quantity = None
                
                try:
                    asin = str(urlparse(self.get_current_url()).path).split("/")[3]
                    if asin == "dp":
                        asin = str(urlparse(self.get_current_url()).path).split("/")[4]
                except Exception as e:
                    print(self.get_current_url())
                
                if self.is_element_present('//*[@id="productOverview_feature_div"]/div/table/tbody/tr[1]/td[2]/span'):
                    brand = self.find_element('//*[@id="productOverview_feature_div"]/div/table/tbody/tr[1]/td[2]/span').text
                elif self.is_element_present('//*[@id="productOverview_feature_div"]/div/div[1]/span[2]'):
                    brand = self.find_element('//*[@id="productOverview_feature_div"]/div/div[1]/span[2]').text
                else:
                    print("Both codes didn't work")
                    break
                
                price = self.execute_script('return document.querySelector(".a-price .a-offscreen").textContent').strip()
                title = self.get_text('//*[@id="title"]')
                
                if self.is_element_present('//*[@id="acrPopover"]/span[1]/a/span'):
                    stars = self.get_text('//*[@id="acrPopover"]/span[1]/a/span')
                else:
                    stars = None
                
                if self.is_element_present('//*[@id="acrCustomerReviewText"]'):
                    star_vote = self.get_text('//*[@id="acrCustomerReviewText"]')
                else:
                    star_vote = None
                
                if self.is_element_present('//*[@id="prodDetails"]/div/div[1]/div'):
                    information = self.get_text('//*[@id="prodDetails"]/div/div[1]/div')
                else:
                    information = None
                
                shipping_time = self.get_text('//*[@id="mir-layout-DELIVERY_BLOCK"]')
                images = self.find_elements('//*[@id="altImages"]/ul//li//img')
                imgurl_list = [img.get_attribute('src') for img in images]
                
                reviews = get_reviews(asin)
                
                product = {
                    "title": title,
                    "brand": brand,
                    "price": price,
                    "stars": stars,
                    "star_vote": star_vote,
                    "information": information,
                    "shipping_time": shipping_time,
                    "imgurl_list": imgurl_list,
                    "asin": asin,
                    "quantity": quantity,
                    "url" : url,
                    "category": current_category,
                    "sub_category": subcategory,
                    "keyword": keywords,
                }
                products.append(product)
                print("Product Added to list")
    return products,reviews
