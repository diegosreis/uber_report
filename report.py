
from selenium import webdriver
from models.trips import Trips

import time


driver = webdriver.Chrome()
driver.get("https://riders.uber.com/")

start_date = "09/26/17"
end_date = "10/25/17"

while "trips" not in driver.current_url:
#while "trips" not in driver.current_url:
	time.sleep(5)
	pass
element = driver.find_element_by_class_name('trip-expand__origin')
element.click()



lst = []

stop = False
page = 1
canceladas = 0
while stop == False:
	trips_table = driver.find_element_by_id('trips-table')
	trs = driver.find_elements_by_xpath('//*[@id="trips-table"]/tbody/tr[@class = "trip-expand__origin collapsed"]')
	for tr in trs:
		pickup = tr.find_elements_by_tag_name('td')[1].text

		if pickup < start_date:
			stop = True
			break

		fare = 	tr.find_elements_by_tag_name('td')[3].text.replace('R$', '');
		
		if fare == 'Canceled':
			fare = 0
			canceladas = canceladas + 1

		if not fare:
			fare = 0
			canceladas = canceladas + 1

		lst.append(Trips.make_trip(pickup, fare))

	page = page + 1
	driver.get("https://riders.uber.com/trips?page="+str(page))
	time.sleep(2)
	element = driver.find_element_by_class_name('trip-expand__origin')
	element.click()
total_fare = 0

with open('report.txt', 'wt') as f:
	f.write('---RELATORIO DE VIAGENS UBER---\n')
	for item in lst:	
		f.write('pickup: ' +  item.pickup +' - fare: ' + str(item.fare) + '\n')
		total_fare = float(total_fare) + float(item.fare)
	f.write('total: '+ str(total_fare)+ '\n')
driver.quit()