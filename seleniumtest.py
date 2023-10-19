from amazoncaptcha import AmazonCaptcha
from seleniumbase import BaseCase
import seleniumwire.undetected_chromedriver as uc
import requests,time,random,json,traceback,datetime
from bs4 import BeautifulSoup as bs
import support as sp

class MyTestCase(BaseCase):
    def test_get_content(self) -> None:
            page_count: int = 1
            sp: SomeClass = SomeClass()
            sp.captcha(self)

            while page_count < 11:
                try:
                    with open('category.json', 'r') as file:
                        data: List[Dict[str, Union[str, Dict[str, List[str]]]]] = json.load(file)

                    # Iterate through each category and its subcategories
                    for item in data:
                        current_category: str = item['category']
                        subcategories: Dict[str, List[str]] = item['subcategory']
                        for subcategory, keywords in subcategories.items():
                            for keyword in keywords:

                                products,reviews = sp.needed_values(self,subcategory,current_category,keyword,page_count)
                                with open("basic_products.json","a+") as f:
                                    json.dump(products,f)
                                with open("basic_products-reviews.json","a+") as g:
                                    json.dump(reviews,g)

                                print(products)
                                page_count+=1
                except Exception as e:
                    #print errors using traceback 
                    traceback.print_exc()

                    with open("error.html","w") as f:
                        f.write(str(self.get_page_source()))
