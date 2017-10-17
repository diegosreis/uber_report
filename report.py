
import datetime
import time

from selenium import webdriver

from models.trip import Trip


driver = webdriver.Chrome()
driver.get('https://riders.uber.com/')

start_date = datetime.datetime(2017, 9, 26)
end_date = datetime.datetime(2017, 10, 25)

while "trips" not in driver.current_url:
	time.sleep(5)

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
		pickup = datetime.datetime.strptime(tr.find_elements_by_tag_name('td')[1].text, '%m/%d/%y')

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

		lst.append(Trip.make_trip(pickup, fare))

	page = page + 1
	driver.get('https://riders.uber.com/trips?page={}'.format(str(page)))
	time.sleep(2)
	element = driver.find_element_by_class_name('trip-expand__origin')
	element.click()

total_fare = 0
with open('report.txt', 'wt') as f:
	f.write('---RELATORIO DE VIAGENS UBER---\n')
	
	for item in lst:	
		f.write('pickup: {pickup} - fare: {fare} \n'.format(pickup=item.pickup.date(), fare=str(item.fare)))
		total_fare = float(total_fare) + float(item.fare)
	
	f.write('total: {total} \n'.format(total=str(total_fare)))

driver.quit()
