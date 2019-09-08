import requests
import json

from django.utils import timezone
from datetime import timedelta
from dateutil.parser import parse

from trackerreport.models import LoginHash, VehicleReport

"""
device_id = models.IntegerField()
	target_name = models.CharField(max_length=50)
	distance_covered = models.FloatField(null=True)
	fuel_consumption = models.FloatField(null=True)
	fuel_allocated = models.IntegerField(default=0)
	location = models.CharField(max_length=50, blank=True, null=True)
	distance_allocated = models.IntegerField(default=0)
	fuel_per_km = models.FloatField(null=True)
	top_speed = models.IntegerField(default=0)
	move_duration = models.CharField(max_length=100, blank=True, null=True)
	stop_duration = models.CharField(max_length=100, blank=True, null=True)
	move_at = models.CharField(max_length=100, blank=True, null=True)
	overspeed = models.FloatField(null=True)
	added = models.DateTimeField(auto_now_add=True)
"""
def run_job():
	upto = timezone.localtime(timezone.now()) - timedelta(days=1)
	start_date = str(upto.date())
	end_date = str(upto.date())
	users = LoginHash.objects.all()
	for user in users:
		get_device_data(user.hash_token, start_date, end_date, upto)


def get_devices(login_hash):
	parameter = {'lang': 'en', 'user_api_hash':login_hash}
	url = "https://service.packet-v.com/api/get_devices"
	rep = requests.get(url, params=parameter)
	devices = rep.json()[0]['items']
	devices_id = []
	for d in devices:
		devices_id.append(d['id'])
	return devices_id

def get_device_history(login_hash, vehicle_id, start_date, end_date):
	parameter = {'lang': 'en', 'user_api_hash': login_hash, 'device_id': vehicle_id , 'from_date':start_date, 'from_time':'00:00:00', 'to_date':end_date, 'to_time':'23:59:59'}
	url = "https://service.packet-v.com/api/get_history"
	rep = requests.get(url, params=parameter)
	devices_data = rep.json()
	return devices_data

def get_device_data(login_hash, start_date, end_date, upto):
	vehicle_reports = []
	devices_id = get_devices(login_hash)
	for device_id in devices_id:
		device_history = get_device_history(login_hash, device_id, start_date, end_date)
		vehicle_report = transform(device_history)
		save_record(vehicle_report, login_hash, device_id, upto)
		

def save_record(record, login_hash, device_id, upto):
	try:
		old_rec = VehicleReport.objects.get(upto=upto,device_id=device_id, login_hash=login_hash)
	except VehicleReport.DoesNotExist:		
		new_rec = VehicleReport(
			target_name = record['Target_name'],
			fuel_consumption = record['Fuel_consumption'],
			top_speed = record['Top_speed'],
			distance_covered = record['Total_distance'],
			fuel_per_km = record['Fuel_per_km'],
			location = record['Location'],
			move_duration = record['Move_duration'],
			stop_duration = record['Stop_duration'],
			fuel_economy = record['Fuel_economy'],
			login_hash = login_hash,
			device_id = device_id,
			upto = upto.date()
		)
		new_rec.save()

def transform(device_history):
	device = {}
	#print(device_history)
	device['Fuel_consumption'] = device_history['fuel_consumption'].split(" ")[0]

	device['Target_name'] = device_history['device']['name']
	device['Total_distance'] = device_history['distance_sum'].split(" ")[0]
	device['Move_distance'] = device_history['move_duration']
	device['Stop_distance'] = device_history['stop_duration']
	device['Top_speed'] = device_history['top_speed'].split(" ")[0]
	device['Move_duration'] = device_history['move_duration']
	device['Fuel_per_km'] = device_history['device']['fuel_per_km'] 
	device['Location'] = device_history['device']['object_owner'] 
	device['Stop_duration'] = device_history['device']['stop_duration']
	fuel = device_history['fuel_consumption'].split(" ")[0]
	distance = device_history['distance_sum'].split(" ")[0] 
	fuel = float(fuel)
	distance = float(distance)
	try: 
		device['Fuel_economy'] = fuel / distance * 100
	except ZeroDivisionError:
		device['Fuel_economy'] = 0
	# device['Fuel_economy'] = device_history['fuel_consumption'].split(" ")[0] / device_history['distance_sum'].split(" ")[0] * 100
	return device