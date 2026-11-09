import json,os,hmac
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET,require_POST
from .models import Reading,Alert
from .thresholds import evaluate_thresholds

def dashboard(request): return render(request,'dashboard.html')
def serialize(r):
 return {'time':r.received_at.isoformat(),'station_id':r.station_id,'water_level_cm':r.water_level_cm,'soil_moisture_pct':r.soil_moisture_pct,'rain_detected':r.rain_detected,'rain_rate_mm_h':r.rain_rate_mm_h,'temperature_c':r.temperature_c,'humidity_pct':r.humidity_pct,'risk':r.risk,'simulated':r.simulated}
@require_GET
def readings(request):
 rows=list(Reading.objects.all()[:60]); latest=rows[0] if rows else None
 return JsonResponse({'latest':serialize(latest) if latest else None,'history':[serialize(x) for x in reversed(rows)],'stale':latest is None or timezone.now()-latest.received_at>timedelta(seconds=45)})
@require_GET
def alerts(request):
 return JsonResponse({'alerts':[{'time':a.created_at.isoformat(),'severity':a.severity,'message':a.message} for a in Alert.objects.all()[:20]]})
def number(data,key,low,high,nullable=False):
 v=data.get(key)
 if nullable and v is None:return None
 if isinstance(v,bool) or not isinstance(v,(int,float)) or not low<=v<=high:raise ValueError(f'{key} must be a number from {low} to {high}')
 return float(v)
@csrf_exempt
@require_POST
def ingest(request):
 expected=os.getenv('DEVICE_API_KEY','')
 if not expected or not hmac.compare_digest(request.headers.get('X-Device-Key',''),expected):return JsonResponse({'error':'Unauthorized'},status=401)
 try:
  data=json.loads(request.body)
  water=number(data,'water_level_cm',0,10000)
  soil=number(data,'soil_moisture_pct',0,100)
  rain_rate=number(data,'rain_rate_mm_h',0,500,True)
  temp=number(data,'temperature_c',-40,80,True)
  humid=number(data,'humidity_pct',0,100,True)
  rain=data.get('rain_detected')
  if not isinstance(rain,bool):raise ValueError('rain_detected must be true or false')
  station=str(data.get('station_id','CHIM-01'))[:64]
  if not station:raise ValueError('station_id required')
  simulated=data.get('simulated',False)
  if not isinstance(simulated,bool):raise ValueError('simulated must be boolean')
  risk,reasons=evaluate_thresholds(soil,rain_rate,humid,water)
  r=Reading.objects.create(station_id=station,water_level_cm=water,soil_moisture_pct=soil,rain_detected=rain,rain_rate_mm_h=rain_rate,temperature_c=temp,humidity_pct=humid,risk=risk,simulated=simulated,packet_id=str(data.get('packet_id',''))[:80])
  if reasons:Alert.objects.create(reading=r,severity=risk,message=f'{station}: {"; ".join(reasons)}')
  return JsonResponse({'id':r.id,'risk':risk},status=201)
 except (ValueError,TypeError,json.JSONDecodeError) as e:return JsonResponse({'error':str(e)},status=400)
