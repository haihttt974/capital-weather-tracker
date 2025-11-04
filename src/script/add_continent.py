import pandas as pd
import pycountry
import pycountry_convert as pc

def get_continent(country_name):
    try:
        # Lấy alpha_2 code từ country_name
        country = pycountry.countries.lookup(country_name)
        country_alpha2 = country.alpha_2
        # Chuyển alpha_2 sang continent code
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        # Map code -> tên châu lục
        continent_names = {
            'AF': 'Africa',
            'NA': 'North America',
            'SA': 'South America',
            'AS': 'Asia',
            'EU': 'Europe',
            'OC': 'Oceania',
            'AN': 'Antarctica'
        }
        return continent_names[continent_code]
    except Exception as e:
        return "Unknown"

# Đọc file CSV
df = pd.read_csv("countries.csv")  # file bạn có dạng (Country,Capital,Latitude,Longitude)

# Tạo cột mới Continent
df["Continent"] = df["Country"].apply(get_continent)

# Xuất ra file CSV mới
df.to_csv("countries_with_continent.csv", index=False)

print("Đã tạo file countries_with_continent.csv thành công!")