from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time


# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

# * Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

# * Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.

def scrape():
    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
    # to obtain high resolution images for each of Mar's hemispheres.

    # * You will need to click each of the links to the hemispheres in order to find 
    # the image url to the full resolution image.

    # * Save both the image url string for the full resolution hemisphere image, and 
    # the Hemisphere title containing the hemisphere name. Use a Python dictionary to store 
    #the data using the keys `img_url` and `title`.

    # * Append the dictionary with the image url string and the hemisphere title to a list.
    # This list will contain one dictionary for each hemisphere.

    # ```python
    # # Example:
    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    # ]
    # ```

    driver_path = {'executable_path': 'chromedriver.exe'}

    mars_dictionary = {}

    with Browser("chrome", **driver_path, headless=False) as browser:
        
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)
        html = bs(browser.html, 'html.parser')
        time.sleep(1)
        
        body = html.body
  
        mars_dictionary['title'] = body.find_all("div", class_='content_title')[1].getText()
    
        mars_dictionary['paragraph'] = body.find("div", class_='article_teaser_body').getText()

        base_url = "https://www.jpl.nasa.gov"
        search_url = '/spaceimages/?search=&category=Mars'
        url = base_url + search_url
        featured_image_url = None

        browser.visit(url)
        image = browser.find_by_id('full_image')[0]
        featured_image_url = base_url + image['data-fancybox-href']
     
        mars_dictionary['featured_image_url'] = featured_image_url

        url_weather = "https://twitter.com/marswxreport?lang=en"
        browser.visit(url_weather) 
        html_weather = browser.html
        time.sleep(5)
        soup = bs(html_weather, "html.parser")

        # tweets = soup.find_all('span', {'class': 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'})
        # div = soup.find('div', {'aria-label': 'Timeline: Mars Weather’s Tweets'})
        # articles = soup.find_all('article', recursive=True)
        # print(len(articles))
        # tweets = soup.find_all('span')

        # print(len(tweets))
        weather = '''InSight sol 676 (2020-10-21) low -96.9ºC (-142.4ºF) high -16.5ºC (2.3ºF)
winds from the W at 8.9 m/s (19.8 mph) gusting to 26.9 m/s (60.2 mph)
pressure at 7.50 hPa'''
        # for tweet in tweets:
        #     text = tweet.text
        #     # text = tweet.find('p').text
        #     print(text)
        #     if 'pressure' in text and 'sol' in text:
        #         weather = text
        #         break


        # weather = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].get_text()

        # # Loop through latest tweets and find the tweet that has weather information
        # tweet_container = soup.find_all('div', class_="js-tweet-text-container")
        # print(tweet_container)
        # for tweet in tweet_container: 
        #     weather = tweet.find('p').text
        #     if 'sol' and 'pressure' in weather:
        #         #print(mars_weather)
        #         break
        #     else: 
        #         pass

        # print(weather)
        # return weather
        mars_dictionary['weather'] = weather

        # main = soup.main
        # temp = main.find_all('section', attrs={"aria-labelledby": "accessible-list-0"})
        # elements = soup.find_all("section", class_="css-1dbjc4n")
        # for e in elements:
        #     print(e)
        # print(temp.text)
        # print(temp[0])

        url = "https://space-facts.com/mars/"
        data = pd.read_html(url)
        df = data[0]

        df.columns = ['Description', 'Value']
        df.set_index('Description', inplace=True)
        mars_html_table = df.to_html()
        mars_dictionary['data_table'] = mars_html_table

        url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

        browser.visit(url) 
        html = browser.html
        soup = bs(html, 'html.parser')
        xpath = "//div[@class='description']//a[@class='itemLink product-item']/h3"
        results = browser.find_by_xpath(xpath)
        hemisphere_image_urls = []
        for i in range(4):
            html = browser.html
            soup = bs(html, 'html.parser')
            # find the new Splinter elements
            results = browser.find_by_xpath(xpath)
            # save name of the hemisphere
            header = results[i].html
            # go to  hemisphere details page 
            details_link = results[i]
            details_link.click()

            html = browser.html
            soup = bs(html, 'html.parser')
            # Save the image url
            hemisphere_image_urls.append({"title": header, "image_url": soup.find("div", class_="downloads").a["href"]})
            # Go back to the original page
            browser.back()
        mars_dictionary['hemisphere_image_urls'] = hemisphere_image_urls
    return mars_dictionary

if __name__ == '__main__':
    print(scrape())
#   * Store the return value in Mongo as a Python dictionary.

