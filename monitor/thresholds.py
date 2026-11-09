import os


def _configured_level(name):
 value=os.getenv(name)
 return float(value) if value else None


def evaluate_thresholds(soil_moisture_pct,rain_rate_mm_h,humidity_pct,water_level_cm):
 findings=[]
 bankfull=_configured_level('BANKFULL_WATER_LEVEL_CM')
 overbank=_configured_level('OVERBANK_WATER_LEVEL_CM')

 if soil_moisture_pct>=46:
  findings.append(('CRITICAL',f'soil moisture {soil_moisture_pct:.1f}% (saturation/action band)'))
 elif soil_moisture_pct>35:
  findings.append(('WARNING',f'soil moisture {soil_moisture_pct:.1f}% (approaching field capacity)'))

 if rain_rate_mm_h is not None:
  if rain_rate_mm_h>25:
   findings.append(('CRITICAL',f'rain rate {rain_rate_mm_h:.1f} mm/h (flash-flood band)'))
  elif rain_rate_mm_h>=2.5:
   findings.append(('WARNING',f'rain rate {rain_rate_mm_h:.1f} mm/h (elevated runoff/ponding band)'))

 if humidity_pct is not None:
  if humidity_pct>90:
   findings.append(('CRITICAL',f'humidity {humidity_pct:.1f}% (storm-context band)'))
  elif humidity_pct>=75:
   findings.append(('WARNING',f'humidity {humidity_pct:.1f}% (high-moisture context band)'))

 if overbank is not None and water_level_cm>=overbank:
  findings.append(('CRITICAL',f'water level {water_level_cm:.1f} cm (overbank level)'))
 elif bankfull is not None and water_level_cm>=bankfull:
  findings.append(('WARNING',f'water level {water_level_cm:.1f} cm (bankfull level)'))

 severity=max((item[0] for item in findings),key={'NORMAL':0,'WARNING':1,'CRITICAL':2}.get,default='NORMAL')
 return severity,[message for _,message in findings]