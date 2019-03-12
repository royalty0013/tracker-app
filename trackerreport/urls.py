from django.conf.urls import url
from trackerreport import views

urlpatterns = [
    url(r'^$', views.login_process, name='login_process' ),
    url(r'^fuel_report/$', views.fuel_report, name='fuel_report' ),
    url(r'^summary_report/$', views.summary_report, name='summary_report' ),
    url(r'^movestat_report/$', views.movestat_report, name='movestat_report' ),
    url(r'^overspeed_report/$', views.overspeed_report, name='overspeed_report' ),

]
