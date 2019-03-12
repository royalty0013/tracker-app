from django.db import models

# Create your models here.

class VehicleReport(models.Model):
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
	


	class Meta:
		verbose_name = 'Vehicle Report' 
		verbose_name_plural = 'Vehicle Reports'

	def __str__(self):
		return self.target_name


class login_hash(models.Model):
	username = models.CharField(max_length=100)
	hash_token = models.CharField(max_length=100)
	added = models.DateTimeField(auto_now_add=True)


	class Meta:
		verbose_name = 'login hash'
		verbose_name_plural = 'login hashs'

	def __str__(self):
		return self.username



