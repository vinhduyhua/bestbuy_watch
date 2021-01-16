from background_task import background
import requests
from bs4 import BeautifulSoup
from background_task.models import Task
from .models import Item, Watchlist, User

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}

details = {"name": "", "price": 0, "url": ""}

def get_converted_price(price):
    stripped_price = price.strip("$ ,")
    replaced_price = stripped_price.replace(",", "")

    return float(replaced_price)

def get_price(script):
    script = script.replace("\\", '')

    index = script.find('currentPrice')
    price = ""
    for char in script[index + 14:]:
        if char == ",":
            break
        price += char

    return price

@background(schedule=3)
def get_product_details():

	page_num = 1

	url = f"https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8cp%3D2&cp={page_num}&id=pcat17071&iht=y&keys=keys&ks=960&list=n&sc=Global&st=graphics%20card&type=page&usc=All%20Categories"

	while requests.get(url, headers=headers):

		url = f"https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8cp%3D2&cp={page_num}&id=pcat17071&iht=y&keys=keys&ks=960&list=n&sc=Global&st=graphics%20card&type=page&usc=All%20Categories"

		page = requests.get(url, headers=headers)

		soup = BeautifulSoup(page.content, "html.parser")
		items = soup.find_all('div', class_="list-item lv")

		for item in items:

			try:

                # Get Title
				title = item.find('h4', class_="sku-header").find('a').text

				link = item.find('h4', class_="sku-header").find('a', href=True)['href']

			except:

				print('Check title')
				title = "None"
				link = "None"

			try:

                # Get Status
				status = item.find('div', class_="fulfillment-add-to-cart-button").find('button').text
				if status == "Add to Cart":
					status = "Available"

			except:
				print('Check status')
				status = "None"

			try:

                # Get Price
				get_script = item.find('div', class_="sku-list-item-price").find_all('script')
				if len(get_script) > 1:
					price = get_price(str(get_script[-1]))
				else:
					price = get_price(str(get_script[0]))

			except:
				print('Check price')
				price = "None"

			if Item.objects.all().exists():
				
				if Item.objects.filter(title=title):

					existing_item = Item.objects.get(title=title)

					# Update existing item
					existing_item.status = status
					existing_item.price = price
					existing_item.link = link
					existing_item.save()

				# Import new item
				else:
					import_item = Item(
						title = title,
						status = status,
						price = price,
						link = link,
						)

					import_item.save()

			# Initial set of item
			else:
				import_item = Item(
						title = title,
						status = status,
						price = price,
						link = link,
						)

				import_item.save()

			print(f"scrape {title} | {status} | {price} | {link}")

		print(f"finish scraping page {page_num}")
		page_num += 1

	print("done scraping!!")

get_product_details(repeat=Task.DAILY, repeat_until=None)


# Call this is refresh the tasks in database
# Task.objects.all().delete()