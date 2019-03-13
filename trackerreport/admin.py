from django.contrib import admin
from trackerreport.models import VehicleReport, LoginHash

# Register your models here.

admin.site.site_header = "Tracker Report Admin"
admin.site.index_title = "Tracker Report Admin"
admin.site.site_title = "Tracker Report Admin"

admin.site.register(VehicleReport)
admin.site.register(LoginHash)



