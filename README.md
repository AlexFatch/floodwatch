# Chimanimani FloodWatch — Django + PostgreSQL

Local prototype for 2× ESP32 and 2× LoRa01, with ultrasonic river level, capacitive soil moisture, resistive rain detection, and DHT22 temperature/humidity.

## Windows setup (VS Code)

1. Install Python 3.11+ and PostgreSQL. In PostgreSQL (pgAdmin Query Tool or psql), create a login and database. Example using `psql` as postgres admin:
   ```sql
   CREATE USER floodwatch WITH PASSWORD 'choose_a_strong_password';
   CREATE DATABASE floodwatch OWNER floodwatch;
   ```
2. Extract project, open its root folder in VS Code. In PowerShell:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   Copy-Item .env.example .env
   ```
3. Edit `.env`: set POSTGRES_PASSWORD to the password you chose, replace DJANGO_SECRET_KEY and DEVICE_API_KEY. Never commit `.env`.
4. In the same terminal:
   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
5. Open http://127.0.0.1:8000 . In another terminal (activate `.venv` first), run:
   ```powershell
   python simulate.py
   ```
6. Admin page: http://127.0.0.1:8000/admin/ . Ctrl+C stops simulation or server.

If PowerShell blocks activation, use `.venv\Scripts\python.exe` in place of `python` without activating.

## Hardware integration later

ESP32 #1 reads sensors and sends compact packets via LoRa01 #1. ESP32 #2 receives them using LoRa01 #2, connects to the same Wi-Fi as the laptop, and HTTP POSTs JSON to `http://LAPTOP_LAN_IP:8000/api/ingest/` with `Content-Type: application/json` and `X-Device-Key: <DEVICE_API_KEY>`. For LAN use set `DJANGO_ALLOWED_HOSTS` to include laptop IP and run `python manage.py runserver 0.0.0.0:8000`; allow firewall access only on trusted private network. Do not expose Django development server to the public internet. LoRa01 radio parameters must match and depend on actual module variant.

Example payload:
```json
{"station_id":"CHIM-01","packet_id":"101","water_level_cm":62.3,"soil_moisture_pct":44.0,"rain_detected":true,"rain_rate_mm_h":12.4,"temperature_c":24.6,"humidity_pct":78.1,"simulated":false}
```

API: GET `/api/readings/`, GET `/api/alerts/`, POST `/api/ingest/`.

## Important limitations

- Alert bands: soil moisture above 35% is WARNING and 46% or above is CRITICAL; rain rate from 2.5 through 25 mm/h is WARNING and above 25 mm/h is CRITICAL; humidity from 75 through 90% is WARNING and above 90% is CRITICAL. The bands are implemented as flood-context indicators, not independently validated evacuation guidance.
- Set `BANKFULL_WATER_LEVEL_CM` and `OVERBANK_WATER_LEVEL_CM` in `.env` to calibrated stage heights for each station. Until configured, water height is recorded but does not trigger a stage alert. These values depend on sensor datum and local channel geometry.
- `rain_rate_mm_h` is optional for backward compatibility. A wet/dry resistive rain sensor cannot measure rainfall intensity; provide readings from a calibrated intensity sensor to use those alert bands.
- Temperature is recorded for flood context but does not trigger alerts yet: numeric limits for a sudden spike and sustained high heat, plus a duration for sustained heat, must be set from local conditions before automating those warnings.
- Soil moisture percentage is meaningful only after calibration.
- Soil moisture percentage is meaningful only after calibration.
- Dashboard `Receiving data` means recent gateway posts, **not verified LoRa radio health**.
- SMS/email, buzzer, delivery acknowledgements, robust alert deduplication, packet authentication beyond a shared key, and offline gateway buffering are future tasks.
- Critical local alarms should be independent of internet, laptop, and Django availability.
