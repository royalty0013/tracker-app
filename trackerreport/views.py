import requests
import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from trackerreport.models import LoginHash


def index(request):
	context = {}
	return render(request, 'trackerreport/index.html', context)

def fuel_report(request):
	context = generate_report(request)
	return render(request, 'trackerreport/fuel_report.html', context)

def summary_report(request):
	context = generate_report(request)
	return render(request, 'trackerreport/summary_report.html', context)

def movestat_report(request):
	context = generate_report(request)
	return render(request, 'trackerreport/move_stat.html', context)

def overspeed_report(request):
	context = generate_report(request)
	return render(request, 'trackerreport/overspeed.html', context)

def login_api(username, password):
	param = {'email': username, 'password':password}
	url = "https://service.packet-v.com/api/login"
	rep = requests.post(url, params=param)
	reps = rep.json()
	return reps

#parameter = {'lang': 'en', 'user_api_hash':request.session['login_hash'}
def login_process(request):
	context = {}
	if request.method == 'POST':		
		username = request.POST['username']
		password = request.POST['password']

		auth = login_api(username, password)
		print(auth)
		if 'user_api_hash' not in auth:
			context['error'] = " Invalid token hash, please check your network connectivity"

			return render(request, 'trackerreport/index.html', context)
		else:
			request.session['login_hash'] = auth['user_api_hash']
			request.session['client_name'] = username

			save_hash(auth['user_api_hash'], username)
			return HttpResponseRedirect("/fuel_report/")
    
	return render(request, 'trackerreport/index.html', context)

def save_hash(login_hash, username):
	try:
		get_hash = LoginHash.objects.get(hash_token=login_hash)
	except LoginHash.DoesNotExist:
		add_hash = LoginHash(username=username, hash_token=login_hash)
		add_hash.save()


def get_devices(request):
	parameter = {'lang': 'en', 'user_api_hash':request.session['login_hash']}
	url = "https://service.packet-v.com/api/get_devices"
	rep = requests.get(url, params=parameter)
	devices = rep.json()[0]['items']
	devices_id = []
	for d in devices:
		devices_id.append(d['id'])
	return devices_id

def get_device_history(request, vehicle_id, start_date, end_date):
	parameter = {'lang': 'en', 'user_api_hash':request.session['login_hash'], 'device_id': vehicle_id , 'from_date':start_date, 'from_time':'00:00:00', 'to_date':end_date, 'to_time':'23:59:59'}
	url = "https://service.packet-v.com/api/get_history"
	rep = requests.get(url, params=parameter)
	devices_data = rep.json()
	return devices_data

def get_device_data(request, start_date, end_date):
	vehicle_reports = []
	devices_id = get_devices(request)
	for device_id in devices_id:
		device_history = get_device_history(request, device_id, start_date, end_date)
		vehicle_report = transform(device_history)
		vehicle_reports.append(vehicle_report)

	return vehicle_reports

def transform(device_history):
	device = {}
	#print(device_history)
	device['Fuel_consumption'] = device_history['fuel_consumption'].split(" ")[0]

	device['Target_name'] = device_history['device']['name']
	device['Total_distance'] = device_history['distance_sum'].split(" ")[0]
	device['Move_distance'] = device_history['move_duration']
	device['Stop_distance'] = device_history['stop_duration']
	device['Top_speed'] = device_history['top_speed']
	device['Move_duration'] = device_history['move_duration']
	device['Fuel_per_km'] = device_history['device']['fuel_per_km'] 
	device['Stop_duration'] = device_history['device']['stop_duration']
	return device

def generate_report(request):
	reports = {}
	reports['vehicle_reports'] = get_device_data(request, '2019-03-01', '2019-03-06')

	return reports


















	

	




