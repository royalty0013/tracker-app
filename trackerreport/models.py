from django.db import models

# Create your models here.

class VehicleReport(models.Model):
	target_name = models.CharField(max_length=50)
	distance_covered = models.CharField(max_length=50)
	fuel_consumption = models.CharField(max_length=50)
	fuel_allocated = models.CharField(max_length=50, blank=True, null=True)
	location = models.CharField(max_length=50, blank=True, null=True)
	distance_allocated = models.CharField(max_length=100, blank=True, null=True)
	fuel_per_km = models.CharField(max_length=100, blank=True, null=True)
	top_speed = models.CharField(max_length=50, blank=True, null=True)
	move_duration = models.CharField(max_length=100, blank=True, null=True)
	stop_duration = models.CharField(max_length=100, blank=True, null=True)
	move_at = models.CharField(max_length=100, blank=True, null=True)
	overspeed = models.CharField(max_length=100, blank=True, null=True)
	added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Vehicle Report' 
		verbose_name_plural = 'Vehicle Reports'

	def __str__(self):
		return self.target_name


