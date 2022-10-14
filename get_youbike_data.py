

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir)))

import json
import pandas as pd
import requests 


# government open data
url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

res = requests.get(url)
data = json.loads(res.text)


df = pd.json_normalize(data)



# 資料清理

col_switch = {
  "sno": "station_no",
  "sna": "station_name", 
  "tot": "total", 
  "sbi": "available",
  "sarea": "district", 
  "mday": "update_time_from_station",
  "lat": "latitude",
  "lng": "longtidue",
  "ar": "adress",
  "sareaen": "distrct_eng",
  "snaen": "station_name_eng",
  "aren": "address_eng",
  "bemp": "empty",
  "act": "open",
  "srcUpdateTime": "system_update_time",
  "updateTime": "update_time_after_processing",
  "infoTime": "update_time",
  "infoDate": "update_date"
}

df.columns = [col_switch[col] for col in list(df.columns)]

df = df.filter(items=['station_name', 'district', 'address', 'total', 'available', 'empty', 'update_time'])


# df = df.assign(generation_stationname= lambda x: x.station_name.str.split(pat='_'))
# df[['generation', 'station_name']] = df['station_name'].apply(lambda x: x.str.split('_', expand=True))