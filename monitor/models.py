from django.db import models
class Reading(models.Model):
 received_at=models.DateTimeField(auto_now_add=True,db_index=True)
 station_id=models.CharField(max_length=64,default='CHIM-01')
 water_level_cm=models.FloatField()
 soil_moisture_pct=models.FloatField()
 rain_detected=models.BooleanField()
 rain_rate_mm_h=models.FloatField(null=True,blank=True)
 temperature_c=models.FloatField(null=True,blank=True)
 humidity_pct=models.FloatField(null=True,blank=True)
 risk=models.CharField(max_length=12,choices=[(x,x) for x in ['NORMAL','WARNING','CRITICAL']])
 simulated=models.BooleanField(default=False)
 packet_id=models.CharField(max_length=80,blank=True)
 class Meta: ordering=['-received_at']
class Alert(models.Model):
 reading=models.ForeignKey(Reading,on_delete=models.CASCADE,related_name='alerts')
 created_at=models.DateTimeField(auto_now_add=True)
 severity=models.CharField(max_length=12)
 message=models.CharField(max_length=250)
 class Meta: ordering=['-created_at']
