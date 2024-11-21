from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize ChromeDriver with headless options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')
options.add_argument('--disable-extensions')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

# List to store page URLs
pages = []

# Navigate to the base URL
base_url = 'https://www.gulahmedshop.com/mens-clothes/unstitched/summer'
driver.get(base_url)
pages.append(base_url)

while True:
    try:
        # Wait until the pagination div is loaded
        pagination_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.pages"))
        )

        # Find the "Next" button element
        next_button = pagination_div.find_element(By.CSS_SELECTOR, "li.pages-item-next.desktop-show a.action.next")

        # Get the href attribute of the "Next" button
        next_page_url = next_button.get_attribute("href")

        # Append the next page URL to the list
        pages.append(next_page_url)

        # Navigate to the next page
        driver.get(next_page_url)

    except Exception as e:
        print("No more pages or an error occurred:", e)
        break

# Print the extracted pagination URLs
print("Pagination URLs:")
for url in pages:
    print(url)

# Function to scrape product URLs from a page
def scrape_product_urls(url):
    driver.get(url)
    try:
        # Wait until the product items are loaded
        product_divs = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.item.main-image a"))
        )

        # Extract product URLs
        product_urls = [div.get_attribute("href") for div in product_divs]
        return product_urls

    except Exception as e:
        print("An error occurred while scraping products:", e)
        return []

# Scrape product URLs from each page
all_product_urls = []
for page_url in pages:
    print(f"Scraping products from page: {page_url}")
    product_urls = scrape_product_urls(page_url)
    all_product_urls.extend(product_urls)

# Print the extracted product URLs
print("Product URLs:")
for url in all_product_urls:
    print(url)

# Function to scrape data from a product page
def scrape_product_data(product_url):
    driver.get(product_url)
    time.sleep(2)  # Adding delay to ensure page load

    try:
        # Extract image URL
        img_tag = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img.no-sirv-lazy-load"))
        )
        img_url = img_tag.get_attribute("src")

        # Extract product title
        title_span = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-title span.base"))
        )
        title = title_span.text

        # Extract product details
        details_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.data.item.content"))
        )
        details = details_div.text

        return {
            "url": product_url,
            "img_url": img_url,
            "title": title,
            "details": details
        }

    except Exception as e:
        print(f"An error occurred while scraping data from {product_url}: {e}")
        return {}

# Scrape data from each product URL
product_data = []
for product_url in all_product_urls:
    print(f"Scraping data from product: {product_url}")
    data = scrape_product_data(product_url)
    if data:
        product_data.append(data)

# Print the extracted product data
print("Product Data:")
for data in product_data:
    print(data)

# Close the driver
driver.quit()
