from django.conf.urls import url
from trackerreport import views

urlpatterns = [
    url(r'^$', views.login_process, name='login_process' ),
    url(r'^fuel_report/$', views.fuel_report, name='fuel_report' ),
    url(r'^date_range/$', views.fuelusage_date_range, name='fuel_report2' ),
    url(r'^summary_report/$', views.summary_report, name='summary_report' ),
    url(r'^summary_date_range/$', views.summary_date_range, name='summary_report2' ),
    # url(r'^movestat_report/$', views.movestat_report, name='movestat_report' ),
    url(r'^distance_covered_report/$', views.distance_covered_report, name='distance_covered_report' ),
    url(r'^distance_date_range/$', views.distance_date_range, name='distance_covered_report2' ),
    url(r'^logout/$', views.logOut, name='log_out'),

]
