import json,os,random,time,urllib.request
from dotenv import load_dotenv
load_dotenv()
url='http://127.0.0.1:8000/api/ingest/'
key=os.getenv('DEVICE_API_KEY','')
if not key:raise SystemExit('Set DEVICE_API_KEY in .env first')
print('Sending simulated flood readings. Ctrl+C to stop.')
for n in range(1000):
 water=min(95,20+n*2.3+random.uniform(-2,2))
 raining=n>4
 payload={'station_id':'CHIM-01','packet_id':f'SIM-{n}','water_level_cm':round(water,1),'soil_moisture_pct':round(min(95,43+n*1.5),1),'rain_detected':raining,'rain_rate_mm_h':round(random.uniform(2.5,40),1) if raining else 0,'temperature_c':round(23+random.uniform(-1,1),1),'humidity_pct':round(65+random.uniform(-4,4),1),'simulated':True}
 req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','X-Device-Key':key},method='POST')
 try:
  with urllib.request.urlopen(req,timeout=5) as response:print(n,payload['water_level_cm'],response.read().decode())
 except Exception as e:print('Failed:',e)
 time.sleep(3)
