import requests
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import  logout
from dateutil.parser import parse
import datetime
from email_split import email_split
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from trackerreport.models import LoginHash, VehicleReport
# from .forms import DateForm


def index(request):
	context = {}
	return render(request, 'trackerreport/index.html', context)

def fuel_report(request):
	#context = generate_report(request)
	context = {}
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	all_report = VehicleReport.objects.filter(upto__gte=(yesterday), login_hash=request.session['login_hash'])
	page = request.GET.get('page', 1)

	paginator = Paginator(all_report, 10)
	try:
		context['allReports'] = paginator.page(page)
	except PageNotAnInteger:
		context['allReports'] = paginator.page(1)
	except EmptyPage:
		context['allReports'] = paginator.page(paginator.num_pages)

	return render(request, 'trackerreport/chartjs.html', context)

def summary_report(request):
	#context = generate_report(request)
	context = {}
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	context['allReports'] = VehicleReport.objects.filter(upto__gte=(yesterday), login_hash=request.session['login_hash'])
	return render(request, 'trackerreport/chartjs.html', context)

# def movestat_report(request):
# 	#context = generate_report(request)
# 	context = {}
# 	context['allReports'] = VehicleReport.objects.all()
# 	return render(request, 'trackerreport/move_stat.html', context)

def distance_covered_report(request):
	#context = generate_report(request)
	context = {}
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	context['allReports'] = VehicleReport.objects.filter(upto__gte=(yesterday), login_hash=request.session['login_hash'])
	return render(request, 'trackerreport/distance_covered.html', context)

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
			return HttpResponseRedirect("/dashboard/")
    
	return render(request, 'trackerreport/index.html', context)

def save_hash(login_hash, username):
	try:
		get_hash = LoginHash.objects.get(hash_token=login_hash)
	except LoginHash.DoesNotExist:
		add_hash = LoginHash(username=username, hash_token=login_hash)
		add_hash.save()

def logOut(request):
	logout(request)
	return HttpResponseRedirect(reverse('login_process'))

def fuelusage_date_range(request):
	context = {}
	if "from_date" in request.GET:
		from_date_object = parse(request.GET['from_date'])
		from_date_object=from_date_object.date()

		to_date_object = parse(request.GET['to_date'])
		to_date_object=to_date_object.date()
		context = {"from_date": from_date_object.isoformat(), "to_date": to_date_object.isoformat()}
	elif request.POST:
		from_date_object = parse(request.POST['from_date'])
		from_date_object=from_date_object.date()

		to_date_object = parse(request.POST['to_date'])
		to_date_object=to_date_object.date()

		context = {"from_date": from_date_object.isoformat(), "to_date": to_date_object.isoformat()}

	the_devices = VehicleReport.objects.filter(upto__range=(from_date_object, to_date_object), login_hash=request.session['login_hash']).values('target_name').distinct()
	the_reports = VehicleReport.objects.filter(upto__range=(from_date_object, to_date_object), login_hash=request.session['login_hash'])
	context['start_date'] = from_date_object
	context['to_date_object'] = to_date_object
	all_report = aggregator(the_reports, the_devices)

	page = request.GET.get('page', 1)
	paginator = Paginator(all_report, 10)

	try:
		context['allReports'] = paginator.page(page)
	except PageNotAnInteger:
		context['allReports'] = paginator.page(1)
	except EmptyPage:
		context['allReports'] = paginator.page(paginator.num_pages)
	#print()
	return render(request, 'trackerreport/chartjs.html', context)

def summary_date_range(request):
	context = {}
	from_date_object = parse(request.POST['from_date'])
	from_date_object=from_date_object.date()

	to_date_object = parse(request.POST['to_date'])
	to_date_object=to_date_object.date()

	the_devices = VehicleReport.objects.filter(upto__range=(from_date_object, to_date_object), login_hash=request.session['login_hash']).values('target_name').distinct()
	the_reports = VehicleReport.objects.filter(upto__range=(from_date_object, to_date_object), login_hash=request.session['login_hash'])
	context['allReports'] = aggregator(the_reports, the_devices)
	context['start_date'] = from_date_object
	context['to_date_object'] = to_date_object
	#print()
	return render(request, 'trackerreport/summary_report.html', context)


def distance_date_range(request):
	context = {}
	from_date_object = parse(request.POST['from_date'])
	from_date_object=from_date_object.date()

	to_date_object = parse(request.POST['to_date'])
	to_date_object=to_date_object.date()

	the_devices = VehicleReport.objects.filter(upto__range=(from_date_object, to_date_object), login_hash=request.session['login_hash']).values('target_name').distinct()
	the_reports = VehicleReport.objects.filter(upto__range=(from_date_object, to_date_object), login_hash=request.session['login_hash'])
	context['allReports'] = aggregator(the_reports, the_devices)
	context['start_date'] = from_date_object
	context['to_date_object'] = to_date_object
	#print()
	return render(request, 'trackerreport/chartjs.html', context)


def aggregator(the_reports, the_devices):
	"""the_devices is a distinct list of dict containing stuffs like {'target_name': 'ACH9998'}
	which we loop through then create a temp dict and for each of the device we loop through the_reports
	looking for the target_name(device) in the reports so we can add the fuel and the distance covered
	before we now append temp to all_devices list and return it
	"""	
	all_devices = []
	for rep in the_devices:
		temp = {'fuel_consumption': 0, 'distance_covered':0, 'target_name': rep['target_name']}
		for device in the_reports:
			if rep['target_name'] == device.target_name:
				temp['fuel_consumption'] = temp['fuel_consumption'] + device.fuel_consumption
				temp['distance_covered'] = temp['distance_covered'] + device.distance_covered
				temp['top_speed'] = device.top_speed
				temp['location'] = device.location
				temp['distance_allocated'] = device.distance_allocated
				temp['fuel_allocated'] = device.fuel_allocated
				temp['fuel_economy'] = device.fuel_economy
		all_devices.append(temp)
	return all_devices





# def datePicker(request):
# 	context = {}
# 	date_form = DateForm()
# 	context['date_picker_form'] = date_form
# 	return render(request, 'trackerreport/fuel_report.html', context)




# def get_devices(request):
# 	parameter = {'lang': 'en', 'user_api_hash':request.session['login_hash']}
# 	url = "https://service.packet-v.com/api/get_devices"
# 	rep = requests.get(url, params=parameter)
# 	devices = rep.json()[0]['items']
# 	devices_id = []
# 	for d in devices:
# 		devices_id.append(d['id'])
# 	return devices_id

# def get_device_history(request, vehicle_id, start_date, end_date):
# 	parameter = {'lang': 'en', 'user_api_hash':request.session['login_hash'], 'device_id': vehicle_id , 'from_date':start_date, 'from_time':'00:00:00', 'to_date':end_date, 'to_time':'23:59:59'}
# 	url = "https://service.packet-v.com/api/get_history"
# 	rep = requests.get(url, params=parameter)
# 	devices_data = rep.json()
# 	return devices_data

# def get_device_data(request, start_date, end_date):
# 	vehicle_reports = []
# 	devices_id = get_devices(request)
# 	for device_id in devices_id:
# 		device_history = get_device_history(request, device_id, start_date, end_date)
# 		vehicle_report = transform(device_history)
# 		vehicle_reports.append(vehicle_report)

# 	return vehicle_reports

# def transform(device_history):
# 	device = {}
# 	#print(device_history)
# 	device['Fuel_consumption'] = device_history['fuel_consumption'].split(" ")[0]

# 	device['Target_name'] = device_history['device']['name']
# 	device['Total_distance'] = device_history['distance_sum'].split(" ")[0]
# 	device['Move_distance'] = device_history['move_duration']
# 	device['Stop_distance'] = device_history['stop_duration']
# 	device['Top_speed'] = device_history['top_speed']
# 	device['Move_duration'] = device_history['move_duration']
# 	device['Fuel_per_km'] = device_history['device']['fuel_per_km'] 
# 	device['Stop_duration'] = device_history['device']['stop_duration']
# 	return device

# def generate_report(request):
# 	reports = {}
# 	reports['vehicle_reports'] = get_device_data(request, '2019-03-01', '2019-03-06')

# 	return reports


















	

	




