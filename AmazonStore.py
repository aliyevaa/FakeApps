import os
import requests
from bs4  import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 

class AmazonStore:
	#needs an Amazon account
	def __init__(self, url = "https://amazon.com"):
		self.url = url
		profile = webdriver.FirefoxProfile("/home/vasilek/.mozilla/firefox/xy36jtgi.amazon/")
		self.driver = webdriver.Firefox(firefox_profile = profile)
		self.driver.get(self.url)
		# TO-DO : get rid of hardcoded home and profile

	def search_for_app(self, name) :
		sbox = self.driver.find_element_by_id("twotabsearchtextbox")
		sbox.send_keys("%s app" % name)
		sbox.send_keys(Keys.ENTER)
		time.sleep(2)
		soup = BeautifulSoup(self.driver.page_source, 'html.parser')
		#with open("a", "w") as f:
		#	f.write(self.driver.page_source)
	
		results = []
		for i in soup.findAll('a', href = True):
			link = i.get("href")
			if "keywords=" in link and "+app" in link and link.endswith("customerReviews")==False:
				results.append("https://www.amazon.com/" + link)
		return list(dict.fromkeys(results))

	def get_reviews(self, elem):
		reviews = []
		for i in elem.find_elements_by_xpath("//span[@class='a-size-base review-text review-text-content']"):
			reviews.append(i.text)
		return reviews

	def get_app_info(self, url):
		self.driver.get(url)
		soup = BeautifulSoup(self.driver.page_source, 'html.parser')
		with open("a", "w") as f:
			f.write(self.driver.page_source)
		results = {}
		n = soup.find("span", {"id":"btAsinTitle"})
		if n is None:
			return None
		na = n.get_text()
		name = na.strip()
		results["title"] = name

		icon = soup.find("img", {"id": "js-masrw-main-image"})
		link = icon.get("src")
		results["icon_url"] = link

		des = soup.find("div", {"id": "mas-product-description"})
		description = des.get_text()
		results["desc"] = description[1:-2] #"\n"

		dev = soup.find("div", {"id": "mas-developer-info"})
		email = ""
		developerWeb = ""
		g = dev.findAll("a")
		for  i in g:
			if i.has_attr("href"):
				link = i.get("href")
				if "mailto:" in link:
					email = link
				if "http" in link:
					developerWeb = link
		results["dWebsite"] = developerWeb
		results["dEmail"] = email
	
		developer = ""
		pp = ""
		s = soup.find("div", {"id": "mobileApplicationTechnicalDetails_feature_div"})
		for i in s.findAll("div", {"class":"a-row"}):
			if "Developed By" in i.get_text():
				if "Privacy Policy" in i.get_text():
					link = i.find("a")
					pp = link["href"]	
					tmp = i.get_text().split("(")[0]
					developer = tmp.split(":")[1].strip()	
				else:
					developer = i.get_text()
		results["d"] = developer
		results["pp"] = pp

		#release date
		elem = self.driver.find_element_by_xpath("//div[@id='detailBullets_feature_div']")
		date = ""
		category = ""
		if elem:
			text = elem.text
			for  i in text.split("\n"):
				if "Date First" in i:
					date = i.split(": ")[-1]
				if "Best Sellers" in i:
					tmp = i.split(": ")[-1]
					tmp1 = tmp.split(" in ")[-1]
					tmp2 = tmp1.split("(")[0]
					category = tmp2
		results["date"] = date
		results["category"] = category
		
		elem = self.driver.find_element_by_xpath("//div[@id='masTechnicalDetails-btf']")
		version = ""
		size = ""
		print("before size")
		if elem is not None:
			text = elem.text
			for i in text.split("\n"):
				if "Size" in i:
					size = i.split(": ")[-1]
				if "Version" in i:
					version = i.split(": ")[-1]
		results["version"] = version
		results["size"] = size
	
		reviews = []
		try:
			elem = self.driver.find_element_by_xpath("//a[@data-hook='see-all-reviews-link-foot']")
			time.sleep(5)
			elem.click()
			elem = self.driver.find_element_by_xpath("//span[@class='a-button a-button-dropdown cr-filter-dropdown']")
			elem.click()
			elem = self.driver.find_element_by_xpath("//a[@id='reviewer-type-dropdown_1']")
			elem.click()
			while True:
				time.sleep(1)
				elem = self.driver.find_element_by_xpath("//div[@class='a-section a-spacing-none reviews-content a-size-base']")
				reviews = reviews + self.get_reviews(elem)
				if len(reviews)<=100:
					a = self.driver.find_element_by_xpath("//li[@class='a-last']")
					if a:
						a.click()
					else:
						break
				else:
					break
					
		except:
			pass
		results["reviews"] = reviews
		return results
		
	def done(self):
		self.driver.close()
