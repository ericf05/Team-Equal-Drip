#!/usr/bin/python3
import schedule
import time
import sys

sys.path.append('/home/equaldrip/Desktop/Sensor_Code')

import os
import pandas as pd
from datetime import datetime
import temperature
import light
import moisture
import json

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://dnpool88:TmC6zQ9H5Yo1rurA@equaldrip.9grq0g8.mongodb.net?retryWrites=true&w=majority&appName=EqualDrip"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Capstone']
collection = db['Sensor_Data']

def run_temp():
	output_value = temperature.main()
	
	current_time = datetime.now().strftime('%m-%d %H')
	#print(current_time)
	store_output('Temperature', output_value, 'F', current_time)
	
def run_light():
	output_value = light.main()
	
	current_time = datetime.now().strftime('%m-%d %H')
	#print(current_time)
	store_output('Light', output_value, 'Lux', current_time)
	
def run_moisture():
	output_value, moisture_per = moisture.main()
	print(output_value, moisture_per)
	current_time = datetime.now().strftime('%m-%d %H')
	#print(current_time)

	store_output('Moisture', moisture_per, '%', current_time)


output_df = pd.DataFrame(columns=['Type', 'Value', 'Measurement', 'Time (M-D H)'])

def store_output(val_type, value, measurement, time):
	global output_df

	data = {
	'Type': val_type,
	'Value': value,
	'Measurement': measurement,
	'Time (M-D H)': time
	}

	result = collection.insert_one(data)
	print("Inserted ID:", result.inserted_id)

	#file_path = '/home/equaldrip/Desktop/Sensor_Code/output.json'
	#output_df = output_df.append({'Type': val_type, 'Value': value, 'Measurement': measurement, 'Time (M-D H)': time}, ignore_index = True)

	#with open(file_path, 'a') as f:
	#	json.dump(output_df.to_dict(orient='records'), f)

schedule.every().hour.do(run_temp)
schedule.every().hour.do(run_light)
schedule.every().hour.do(run_moisture)

while True:
	test_df = pd.DataFrame([datetime.now()], columns=['Test'])
	test_df.to_csv('test.csv', index=False)
	print('pending')
	schedule.run_pending()
	time.sleep(30)
