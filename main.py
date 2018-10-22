import os
import requests
from openpyxl import load_workbook
from sets import Set

TANTALUS_SAMPLE_URL = "http://tantalus.bcgsc.ca/api/sample"

if __name__ == '__main__':
	tantalus_sample_set = Set()
	excel_sample_set = Set()
	workbook = load_workbook('Aparicio_Library_master_list__June2017.xlsx')
	master_sheet = workbook['master page']
	count = 1
	for row in master_sheet.rows:
		if count == 1:
			count += 1
			continue
		for cell in row:
			if(cell.value is not None):
				excel_sample_set.add(cell.value)
			break

	r = requests.get(TANTALUS_SAMPLE_URL).json()
	while(True):
		for result in r['results']:
			tantalus_sample_set.add(result['sample_id'])
		if(r['next'] is None):
			break
		r = requests.get(r['next']).json()

	not_imported_set = excel_sample_set.difference(tantalus_sample_set)

	with open("not_imported_samples.txt", "w") as file:
		for sample in list(not_imported_set):
			file.write(sample.encode('utf-8') + '\n')

	print(not_imported_set)


