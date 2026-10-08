import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import requests

print("=== กำลังสร้างกราฟสรุปสภาพอากาศพิษณุโลก ===")

# -------------------------------------------------------------
# 1. EXTRACT HOURLY DATA: ดึงข้อมูลพยากรณ์ 24 ชั่วโมงของวันนี้
# เพื่อให้เรามีข้อมูลครบ 24 จุดเวลามาวาดกราฟเส้นสวยๆ
# -------------------------------------------------------------
url = "https://api.open-meteo.com/v1/forecast?latitude=16.82&longitude=100.26&hourly=temperature_2m,relative_humidity_2m&timezone=Asia%2FBangkok&forecast_days=1"
response = requests.get(url)
data = response.json()["hourly"]

# แปลงเป็น DataFrame และตัดเวลาให้เหลือเฉพาะชั่วโมง (เช่น "08:00")
df_24h = pd.DataFrame({
    "time": [t.split("T")[1] for t in data["time"]],
    "temperature_c": data["temperature_2m"],
    "humidity_pct": data["relative_humidity_2m"],
})

# -------------------------------------------------------------
# 2. LOAD TO DB: บันทึกข้อมูล 24 ชั่วโมงลงในตารางใหม่ของ weather.db
# -------------------------------------------------------------
conn = sqlite3.connect("weather.db")
df_24h.to_sql("weather_24h_forecast", conn, if_exists="replace", index=False)
print("อัปเดตข้อมูล 24 ชั่วโมงเข้าสู่ฐานข้อมูลเรียบร้อย!")

# -------------------------------------------------------------
# 3. QUERY & VISUALIZE: เขียน SQL ดึงข้อมูลจาก DB มาวาดกราฟ
# -------------------------------------------------------------
query = (
    "SELECT time, temperature_c, humidity_pct FROM weather_24h_forecast;"
)
df_plot = pd.read_sql(query, conn)
conn.close()

# สร้างรูปกราฟ
fig, ax1 = plt.subplots(figsize=(10, 5))

# กราฟเส้นที่ 1: อุณหภูมิ (แกนซ้าย - สีแดง/ส้ม)
color = "tab:red"
ax1.set_xlabel("Time (Hour)", fontsize=12)
ax1.set_ylabel("Temperature (°C)", color=color, fontsize=12)
line1 = ax1.plot(
    df_plot["time"],
    df_plot["temperature_c"],
    color=color,
    marker="o",
    linewidth=2,
    label="Temperature (°C)",
)
ax1.tick_params(axis="y", labelcolor=color)
ax1.set_xticks(df_plot["time"][::3])  # แสดงป้ายเวลาทุกๆ 3 ชั่วโมงให้อ่านง่าย
ax1.grid(True, linestyle="--", alpha=0.5)

# กราฟเส้นที่ 2: ความชื้น (แกนขวา - สีฟ้า)
ax2 = ax1.twinx()
color = "tab:blue"
ax2.set_ylabel("Humidity (%)", color=color, fontsize=12)
line2 = ax2.plot(
    df_plot["time"],
    df_plot["humidity_pct"],
    color=color,
    marker="s",
    linestyle="--",
    linewidth=2,
    label="Humidity (%)",
)
ax2.tick_params(axis="y", labelcolor=color)

# ตั้งชื่อหัวกราฟ
plt.title(
    "Phitsanulok 24-Hour Weather Forecast (Temperature vs Humidity)",
    fontsize=14,
    pad=15,
)

# บันทึกรูปภาพออกมาเป็นไฟล์ .png
output_image = "weather_chart.png"
plt.tight_layout()
plt.savefig(output_image, dpi=300)
print(f"บันทึกรูปกราฟเรียบร้อยที่ไฟล์: {output_image}")