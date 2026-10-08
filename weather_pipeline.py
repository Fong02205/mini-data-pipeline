import sqlite3
import pandas as pd
import requests

print("=== เริ่มต้นดึงข้อมูลสภาพอากาศพิษณุโลก ===")

# -------------------------------------------------------------
# 1. EXTRACT: ดึงข้อมูลสดผ่าน Web API ด้วย requests
# -------------------------------------------------------------
# พิกัดของจังหวัดพิษณุโลก (ละติจูด 16.82, ลองจิจูด 100.26)
url = "https://api.open-meteo.com/v1/forecast?latitude=16.82&longitude=100.26&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&timezone=Asia%2FBangkok"

print("[1] กำลังส่ง Request ไปยัง Open-Meteo API...")
response = requests.get(url)

# แปลงข้อมูลผลลัพธ์จาก JSON เป็น Dictionary ใน Python
raw_json = response.json()
current = raw_json["current"]

print("ข้อมูลดิบที่ได้จาก API:")
print(current)

# -------------------------------------------------------------
# 2. TRANSFORM: จัดรูปแบบข้อมูล และแปลรหัสสภาพอากาศ
# -------------------------------------------------------------
print("\n[2] กำลังแปลงและทำความสะอาดข้อมูล (Transform)...")


# ฟังก์ชันแปลงตัวเลข Weather Code เป็นคำอธิบายภาษาไทย
def interpret_weather(code):
  if code == 0:
    return "ท้องฟ้าแจ่มใส"
  elif code in [1, 2, 3]:
    return "มีเมฆบางส่วน"
  elif code in [45, 48]:
    return "มีหมอก"
  elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
    return "มีฝนตก"
  elif code in [95, 96, 99]:
    return "พายุฝนฟ้าคะนอง"
  else:
    return "สภาพอากาศทั่วไป"


# จัดข้อมูลให้อยู่ในรูปแบบตาราง 1 แถว
clean_data = [{
    "location": "Phitsanulok",
    "recorded_at": current["time"],  # เวลาที่บันทึก
    "temperature_c": current["temperature_2m"],  # อุณหภูมิ (°C)
    "humidity_pct": current["relative_humidity_2m"],  # ความชื้นสัมพัทธ์ (%)
    "wind_speed_kmh": current["wind_speed_10m"],  # ความเร็วลม (กม./ชม.)
    "condition": interpret_weather(current["weather_code"]),  # สภาพอากาศ
}]

df = pd.DataFrame(clean_data)
print("ตารางข้อมูลที่พร้อมบันทึก:")
print(df)

# -------------------------------------------------------------
# 3. LOAD: บันทึกลงฐานข้อมูล SQLite (แบบสะสมข้อมูล: Append)
# -------------------------------------------------------------
print("\n[3] กำลังบันทึกลงฐานข้อมูล weather.db...")
conn = sqlite3.connect("weather.db")

# ⚠️ จุดสำคัญ: ใช้ if_exists="append" เพื่อเก็บสะสมข้อมูลต่อท้าย ไม่ทับของเดิม
df.to_sql("phitsanulok_weather", conn, if_exists="append", index=False)
print("บันทึกข้อมูลเรียบร้อย!")

# -------------------------------------------------------------
# 4. VERIFY: ใช้คำสั่ง SQL ตรวจสอบประวัติสภาพอากาศใน Database
# -------------------------------------------------------------
print("\n[4] ตรวจสอบข้อมูลทั้งหมดในตาราง phitsanulok_weather ด้วย SQL:")
query = "SELECT * FROM phitsanulok_weather;"
df_all = pd.read_sql(query, conn)
print(df_all)

conn.close()
print("\n=== Pipeline ทำงานเสร็จสมบูรณ์! ===")