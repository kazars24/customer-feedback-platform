import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--city_name',
                        type=str,
                        dest='city_name',
                        help='City name',
                        required=True)
    parser.add_argument('-i', '--shops_id',
                        type=str,
                        dest='shops_id',
                        help='Shops network ID',
                        required=True)
    parser.add_argument('-n', '--shops_name',
                        type=str,
                        dest='shops_name',
                        help='Shops network name',
                        required=True)

    args = parser.parse_args()
    city_name = args.city_name
    shops_network_id = args.shops_id
    shops_network_name = args.shops_name

    url = f"https://2gis.ru/{city_name}/branches/{shops_network_id}/"
    driver.get(url)

    scrollable_div = driver.find_element(By.CLASS_NAME, "_1rkbbi0x")
    end_of_page = False

    # Scroll to the end of the page until all shops are loaded
    while not end_of_page:
        scrollable_div.send_keys(Keys.END)
        time.sleep(2)

        driver.execute_script('''
            var loadMoreButton = document.querySelector('button._1iczexgz');
            if (loadMoreButton) {
                loadMoreButton.click();
            }
        ''')

        time.sleep(2)
        load_more_button = driver.find_elements(By.XPATH, "//div/button[@class='_1iczexgz']")
        
        if not load_more_button:
            end_of_page = True

    divs_1kf6gff = driver.find_elements(By.CLASS_NAME, "_1kf6gff")

    with open(f"parsed_urls_{city_name}_{shops_network_name}.txt", "w") as file:
        for div_1kf6gff in divs_1kf6gff:
            div_zjunba = div_1kf6gff.find_element(By.CLASS_NAME, "_zjunba")
            a_elements = div_zjunba.find_elements(By.CLASS_NAME, "_1rehek")
            
            for a_element in a_elements:
                href = a_element.get_attribute("href")
                file.write(f"{href}\n")

    print(f"URLs extracted and saved to parsed_urls_{city_name}_{shops_network_name}.txt")
    driver.quit()


if __name__ == '__main__':
    main()
