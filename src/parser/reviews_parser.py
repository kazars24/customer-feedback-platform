import re
import json
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=options)

def scrape_reviews(url):
    reviews_data = []

    reviews_url = f"{url}/tab/reviews"
    driver.get(reviews_url)

    # Wait for the reviews page to load
    time.sleep(5)

    scroll_num = len(driver.find_elements(By.CLASS_NAME, "_11gvyqv"))

    try:
        reviews_block = driver.find_element(By.CLASS_NAME, "_1rkbbi0x")

        # Find the total number of reviews
        reviews_count_element = driver.find_element(By.CLASS_NAME, "_1xhlznaa")
        total_reviews = int(reviews_count_element.text)
    except Exception as e:
        print(f"Error while retrieving reviews count: {str(e)}")
        total_reviews = scroll_num  # Default to 0 reviews

    reviews_block = driver.find_element(By.CLASS_NAME, "_1rkbbi0x")
    # Scroll to load all reviews
    while len(driver.find_elements(By.CLASS_NAME, "_11gvyqv")) < total_reviews:
        reviews_block.send_keys(Keys.END)
        time.sleep(2)

    review_divs = driver.find_elements(By.CLASS_NAME, "_11gvyqv") or []
    for review_div in review_divs:
        # Expand the review text if possible
        try:
            read_more_button = review_div.find_element(By.CLASS_NAME, "_17ww69i")
            driver.execute_script("arguments[0].click();", read_more_button)
            time.sleep(1)
        except Exception:
            pass

        # Find the review text container
        try:
            review_text_element = review_div.find_element(By.CSS_SELECTOR, "div._49x36f a._1it5ivp")
            review_text = review_text_element.text
        except Exception as e:
            print(f"Error while extracting review text: {str(e)}")
            review_text = ""

        # Find the star rating
        stars_colored = len(review_div.find_elements(By.CLASS_NAME, "_1fkin5c span"))
        rating = stars_colored

        # Find the review date
        try:
            date_element = review_div.find_element(By.CLASS_NAME, "_4mwq3d")
            # Extract and format the date using regular expressions
            date_text = re.search(r'(\d+\s+\w+\s+\d{4})', date_element.text)
            if date_text:
                date = date_text.group(1)
            else:
                date = ""
        except Exception as e:
            print(f"Error while extracting review date: {str(e)}")
            date = ""

        # Append the review text and date to the list
        reviews_data.append({'rating': rating, 'text': review_text, 'date': date})

    return reviews_data

def scrape_address(url):
    # Navigate to the main URL
    driver.get(url)

    # Wait for the main page to load
    time.sleep(5)

    try:
        # Find the parent element that contains the address and location information
        address_container = driver.find_element(By.CLASS_NAME, "_49kxlr")

        # Extract the text from the address container
        address_text = address_container.find_element(By.CLASS_NAME, "_2lcm958").text.strip()
        location_text = address_container.find_element(By.CLASS_NAME, "_1p8iqzw").text.strip()

        # Combine the address and location into a single string
        full_address = f"{address_text}, {location_text}"
    except Exception as e:
        print(f"Error while scraping address: {str(e)}")
        full_address = ""

    return full_address


def update_json_file(file_path, new_data):
    # Open the JSON file and load its contents into a dictionary
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Update the dictionary with the new data
    data.update(new_data)

    # Write the updated dictionary back to the JSON file
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--city_name',
                        type=str,
                        dest='city_name',
                        help='City name',
                        required=True)
    parser.add_argument('-n', '--shops_name',
                        type=str,
                        dest='shops_name',
                        help='Shops network name',
                        required=True)

    args = parser.parse_args()
    city_name = args.city_name
    shops_network_name = args.shops_name

    with open(f"parsed_urls_{city_name}_{shops_network_name}.txt", "r") as file:
        urls = file.read().splitlines()

    reviews_dict = {}

    for url in urls:
        address = scrape_address(url)
        reviews_list = scrape_reviews(url)
        reviews_dict[url] = {"address": address, "reviews_list": reviews_list}
        update_json_file(f"reviews_data_{city_name}_{shops_network_name}.json", reviews_dict)
        print(f"Dumped url: {url}")

    print(f"Review data saved to reviews_data_{city_name}_{shops_network_name}.json")

    driver.quit()

if __name__ == '__main__':
    main()
