
import datetime
import time

from selenium import webdriver

from models.trip import Trip


driver = webdriver.Chrome(executable_path='/home/diego/Programs/chromedriver')
driver.get('https://riders.uber.com/')

start_date = datetime.datetime(2018, 3, 26)
end_date = datetime.datetime(2018, 4, 25)

while "trips" not in driver.current_url:
	time.sleep(5)

element = driver.find_element_by_class_name('trip-expand__origin')
element.click()

lst = []
trip = Trip()
stop = False
page = 1
canceladas = 0
while stop == False:
	trips_table = driver.find_element_by_id('trips-table')
	trs = driver.find_elements_by_xpath('//*[@id="trips-table"]/tbody/tr[@class = "trip-expand__origin collapsed"]')

	for tr in trs:
		pickup = tr.find_elements_by_tag_name('td')[1].text.replace('""', '')[:8]
		pickup = datetime.datetime.strptime(pickup, '%m/%d/%y')

		if pickup > end_date:
			continue
		
		if pickup < start_date:
			stop = True
			break

		fare = 	tr.find_elements_by_tag_name('td')[3].text.replace('R$', '').replace('Cancelado', '').replace(',', '.').replace('\n','');

		if fare == 'Canceled' or fare == 'Cancelado':
			fare = 0
			canceladas = canceladas + 1

		if not fare:
			fare = 0
			canceladas = canceladas + 1

		lst.append(trip.make_trip(pickup, fare))

	page = page + 1
	driver.get('https://riders.uber.com/trips?page={}'.format(str(page)))
	time.sleep(2)
	element = driver.find_element_by_class_name('trip-expand__origin')
	element.click()

total_fare = 0
with open('report.txt', 'wt') as f:
	f.write('---RELATORIO DE VIAGENS UBER---\n')

	for item in lst:
		f.write('pickup: {pickup} - fare: {fare} \n'.format(pickup=item['pickup'].date(), fare=str(item['fare'])))
		total_fare = float(total_fare) + float(item['fare'])

	f.write('total: {total} \n'.format(total=str(total_fare)))

driver.quit()
