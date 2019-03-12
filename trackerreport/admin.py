from django.contrib import admin
from trackerreport.models import VehicleReport, login_hash

# Register your models here.

admin.site.site_header = "Tracker Report Admin"
admin.site.index_title = "Tracker Report Admin"
admin.site.site_title = "Tracker Report Admin"

admin.site.register(VehicleReport)
admin.site.register(login_hash)



