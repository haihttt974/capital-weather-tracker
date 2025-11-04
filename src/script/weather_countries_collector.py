import requests
import csv
import os
import time
import json
from datetime import datetime, timedelta, timezone
import sys

# =============================
# ĐỌC API KEY TỪ FILE
# =============================
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)
API_KEY = config["API_KEY"]

FOLDER = "Countries"
os.makedirs(FOLDER, exist_ok=True)

# =============================
# Đọc danh sách quốc gia
# =============================
locations = []
with open("countries_with_continent.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        country = row["Country"].strip()
        capital = row["Capital"].strip()
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])
        continent = row.get("Continent", "").strip()
        locations.append((country, capital, lat, lon, continent))

# =============================
# Đọc lịch chạy từ utc-time.csv
# =============================
run_times = set()
with open("utc-time.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            hour = int(row["hour"])
            minute = int(row["minute"])
            run_times.add((hour, minute))
        except:
            pass

# =============================
# Hàm an toàn ép kiểu
# =============================
def safe(val, cast=float):
    try:
        return cast(val)
    except:
        return "N/A"

# =============================
# Tạo file CSV nếu chưa có
# =============================
def ensure_csv(country, capital):
    filename = f"{country.replace(' ', '')}-{capital.replace(' ', '')}.csv"
    file_path = os.path.join(FOLDER, filename)
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "utc_time", "local_time",
                "country", "capital", "continent",
                "temperature", "temp_min", "temp_max",
                "humidity", "feels_like", "visibility",
                "precipitation", "cloudcover", "wind_speed", "wind_gust",
                "wind_direction", "pressure", "is_day",
                "weather_code", "weather_main", "weather_description", "weather_icon"
            ])
    return file_path

# =============================
# File isRun.csv
# =============================
ISRUN_FILE = "isRun.csv"

def init_isrun():
    if not os.path.exists(ISRUN_FILE):
        with open(ISRUN_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "run"])
            for idx in range(1, len(locations)+1):
                writer.writerow([idx, 0])

def load_isrun():
    runs = {}
    with open(ISRUN_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            runs[int(row["id"])] = int(row["run"])
    return runs

def save_isrun(runs):
    with open(ISRUN_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "run"])
        for idx in range(1, len(locations)+1):
            writer.writerow([idx, runs.get(idx, 0)])

# =============================
# Gọi API và ghi dữ liệu
# =============================
def fetch_and_write(country, capital, lat, lon, continent):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        main = data.get("main", {})
        wind = data.get("wind", {})
        rain = data.get("rain", {})
        clouds = data.get("clouds", {})
        weather = data.get("weather", [{}])[0]
        sys_data = data.get("sys", {})

        # === Thời gian ===
        utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
        offset_seconds = data.get("timezone", 0)
        local_now = utc_now + timedelta(seconds=offset_seconds)

        sunrise = datetime.fromtimestamp(sys_data.get("sunrise", 0), timezone.utc) + timedelta(seconds=offset_seconds)
        sunset = datetime.fromtimestamp(sys_data.get("sunset", 0), timezone.utc) + timedelta(seconds=offset_seconds)
        is_day = 1 if sunrise < local_now < sunset else 0

        filename = ensure_csv(country, capital)
        with open(filename, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                utc_now.strftime("%Y-%m-%d %H:%M:%S"),
                local_now.strftime("%Y-%m-%d %H:%M:%S"),
                country, capital, continent,
                safe(main.get("temp")),
                safe(main.get("temp_min")),
                safe(main.get("temp_max")),
                safe(main.get("humidity")),
                safe(main.get("feels_like")),
                safe(data.get("visibility")),
                safe(rain.get("1h", 0.0)),
                safe(clouds.get("all")),
                safe(wind.get("speed")),
                safe(wind.get("gust", 0.0)),
                safe(wind.get("deg")),
                safe(main.get("pressure")),
                is_day,
                safe(weather.get("id"), int),
                weather.get("main", ""),
                weather.get("description", ""),
                weather.get("icon", "")
            ])
        print(f"✅ {capital}, {country} - thành công")
        return True
    except Exception as e:
        print(f"❌ {capital}, {country} - lỗi: {e}")
        return False

# =============================
# Chạy một lượt với isRun.csv
# =============================
def run_once():
    utc_start = datetime.utcnow()
    print(f"\n🔔 Bắt đầu lượt lúc (UTC): {utc_start.strftime('%Y-%m-%d %H:%M:%S')}")

    runs = load_isrun()
    pending = []

    for idx, (country, capital, lat, lon, continent) in enumerate(locations, start=1):
        if runs.get(idx, 0) == 1:
            continue  # đã chạy rồi, bỏ qua

        retry_count = 0
        success = False
        while retry_count < 5 and not success:
            success = fetch_and_write(country, capital, lat, lon, continent)
            if not success:
                retry_count += 1
                time.sleep(5)
        if success:
            runs[idx] = 1
            save_isrun(runs)  # lưu lại ngay sau khi thành công
        else:
            pending.append((idx, country, capital, lat, lon, continent))

    # Xử lý lại pending
    while pending:
        print(f"\n🔄 Đang xử lý lại {len(pending)} thủ đô lỗi trước đó...")
        new_pending = []
        for idx, country, capital, lat, lon, continent in pending:
            if fetch_and_write(country, capital, lat, lon, continent):
                runs[idx] = 1
                save_isrun(runs)
            else:
                new_pending.append((idx, country, capital, lat, lon, continent))
                time.sleep(5)
        pending = new_pending

    # Nếu tất cả đều = 1 thì reset về 0
    if all(val == 1 for val in runs.values()):
        print("🔄 Hoàn tất một lượt → reset isRun.csv về 0")
        for k in runs.keys():
            runs[k] = 0
        save_isrun(runs)

    utc_end = datetime.utcnow()
    print(f"✅ Hoàn thành lượt. Bắt đầu: {utc_start.strftime('%Y-%m-%d %H:%M:%S')} - Kết thúc: {utc_end.strftime('%Y-%m-%d %H:%M:%S')}")

# =============================
# Vòng lặp chính
# =============================
print("🚀 Chương trình lấy dữ liệu thời tiết các thủ đô bắt đầu...")
init_isrun()
while True:
    now = datetime.utcnow()
    if (now.hour, now.minute) in run_times:
        run_once()
        time.sleep(60)  # tránh chạy lại cùng phút
    else:
        time.sleep(10)