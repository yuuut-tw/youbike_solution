
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir)))

import time
import json
import pandas as pd
import requests
import mysql.connector
from dotenv import load_dotenv # 環境變數

# get data
env_path = 'D:/yuting_repo/youbike_solution/data/.env'
load_dotenv(env_path)
my_client = {'host':os.environ['host'],
             'user':os.environ['user'],
             'pwd' :os.environ['password']}


def write_table(client, database, table, col, df):
    
    database = database.replace('`','')
    if len(df)<1:
        return 'empty data'
    
    df = df.where(pd.notnull(df), None)
    try:
        col = [ f'`{x}`' for x in col]
        con = mysql.connector.connect(
            host=client['host'],
            user=client['user'],
            password=client['pwd'],
            database=database,
            auth_plugin='mysql_native_password'
        )
        cursor = con.cursor(buffered=True)
        
        s = ['%s'] * len(col)  #  col數量
        insert_sql = f'''
            INSERT INTO `{database}`.`{table.replace('`','')}`
                ({', '.join(col)})
            VALUES
                ({', '.join(s)})
        '''
        if len(df)>1:
            values = df.values.tolist()
            for i in range(1+len(values)//10000):
                cursor.executemany(insert_sql, values[i*10000:(i+1)*10000])
                con.commit()
        else:
            for val in df.values:
                val = tuple(val)
                cursor.execute(insert_sql, val)
            con.commit()
            
        res = f'success : insert {database}.{table}'
    except Exception as e:
        con.rollback()
        res = f'failed : insert {database}.{table}'
        print(e)
        error = e
    finally:
        cursor.close()
        con.close()
        print(res)
        if 'failed' in res:
            raise Exception(error)
        return res



def get_open_data():

  # government open data
  url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'

  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

  res = requests.get(url, headers=headers)
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
    "ar": "address",
    "sareaen": "distrct_eng",
    "snaen": "station_name_eng",
    "aren": "address_eng",
    "bemp": "empty",
    "act": "if_open",
    "srcUpdateTime": "system_update_time",
    "updateTime": "update_time_after_processing",
    "infoTime": "update_time",
    "infoDate": "update_date"
  }

  df.columns = [col_switch[col] for col in list(df.columns)]

  df['generation'] = df['station_name'].apply(lambda x: x.split('_')[0])
  df['station_name'] = df['station_name'].apply(lambda x: x.split('_')[1])


  df = df.filter(items=['update_time', 'station_no', 'generation', 
                        'station_name', 'if_open', 'total', 'available', 'empty', 'district',     
                        'latitude', 'longtidue']) \
        .astype({'station_no':int,
                  'if_open':bool,
                  })


  return df



start = 0
end = 900
for _ in range(900):
  
  print(f'loop time count: {start}')

  try:
    df = get_open_data()
    write_table(my_client, 'open_data', 'youbike_station_data', list(df.columns), df)

  except:
    print('data duplicated. Skip this time!')
  
  time.sleep(180)

  start += 1

  if start == end:
    break


