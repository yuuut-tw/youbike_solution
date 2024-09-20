
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir)))

import json
import config.import_config as cf

def get_json_data(file_name):
    
    file_path = rf"{cf.config['root_path']}/{file_name}"
    
    with open(file_path, 'r') as f:
        data = json.loads(f.read())

    return data





# ###################### 排查area
# path = rf'//192.168.1.20/Rmc/Data Analysis/Dropbox/Daily PNL/{tdday[3]}/{tdday[2]}/MT4-百万交易量{tdday[1]}.xlsx'

# mt5_vol_real = pd.read_excel(path, sheet_name='raw-mt5')
# mt5_inf_vol_real = pd.read_excel(path, sheet_name='INFINOX_mt5')
# eod = pd.read_excel(path, sheet_name='Eod', usecols='L:O').dropna(how='all').rename(columns={'Symbol.1':'symbol', 'CCY':'ccy', 'Eod':'eod', 'Rate':'rate'})


# from openpyxl import load_workbook

# # MT4
# # read volume (MT4)
# volume_book_mt4 = pd.DataFrame()

# wb = load_workbook(path, read_only=True)
# load_sheets = [sheet for sheet in wb.sheetnames if re.match(r'^Raw.*', sheet)]

# for sheet in load_sheets:
#     df = pd.read_excel(path, sheet_name=sheet) \
#         .rename(str.lower, axis='columns') \
#         .dropna(subset=['login'])
    
#     volume_book_mt4 = pd.concat([volume_book_mt4, df], ignore_index=True)

# mt4 = volume_book_mt4.rename(str.lower, axis=1) \
#                      .filter(items = ['db', 'type', 'login', 'symbol', 'real bs', 'product', 'milldollar', 'ticket'])


# ## 排查
# mt4_test = raw_mt4_adj.rename(str.lower, axis=1) \
#                      .filter(items = ['db', 'type', 'login', 'symbol', 'clean_symbol', 'bs', 'is_test', 'milliondollar', 'ticket'])


# df_check = mt4.merge(mt4_test, how='left', on=['login', 'type', 'ticket'], suffixes=['', '_test'])

# df_check['million_diff'] = df_check['milldollar'] - df_check['milliondollar']

# df_check.query('million_diff != 0').sort_values(by='million_diff', ascending=False).head(20)



# # MT5
# ## 排查
# mt5 = mt5_vol_real.rename(str.lower, axis=1) \
#                   .filter(items = ['server', 'type', 'login', 'symbol', 'real bs', 'milldollar', 'deal', 'positionid'])

# ## 排查
# mt5_test = raw_mt5_adj.rename(str.lower, axis=1) \
#                      .filter(items = ['server', 'type', 'login', 'symbol', 'bs', 'is_test', 'milliondollar', 'deal', 'positionid'])


# df_mt5_check = mt5.merge(mt5_test, how='left', on=['deal'], suffixes=['', '_test'])

# df_mt5_check['million_diff'] = df_mt5_check['milldollar'] - df_mt5_check['milliondollar']

# df_mt5_check.query('million_diff != 0').sort_values(by='million_diff', ascending=False)






# ## INFINOX mt5排查
# mt5_inf = mt5_inf_vol_real.rename(str.lower, axis=1) \
#                           .filter(items = ['server', 'type', 'login', 'symbol', 'real bs', 'milldollar', 'deal', 'positionid'])

# ## 排查
# mt5_inf_test = raw_inf_mt5_adj.rename(str.lower, axis=1) \
#                                 .filter(items = ['server', 'type', 'login', 'symbol', 'bs', 'is_test', 'milliondollar', 'deal', 'positionid'])


# df_mt5_inf_check = mt5_inf.merge(mt5_inf_test, how='left', on=['deal'], suffixes=['', '_test'])

# df_mt5_inf_check['million_diff'] = df_mt5_inf_check['milldollar'] - df_mt5_inf_check['milliondollar']

# df_mt5_inf_check.query('million_diff != 0').sort_values(by='million_diff', ascending=False)



# path = r'\\192.168.1.20\Rmc\Data Analysis\Dropbox\Daily PNL\2023-10\1012\MT4-百万交易量20231012.xlsx'

# df_mt4 = pd.read_excel(path, sheet_name='Result', usecols='I:K').dropna(how='all').head(30)


# df_acc_sheet = pd.read_excel(path, sheet_name='account')

# ## exlcude RG IV
# million_all = pd.concat([raw_mt4_adj, raw_mt5_adj, raw_inf_mt5_adj], ignore_index=True) \
#         .query('Entry != 3') \
#         .filter(items=['db', 'clean_symbol', 'is_test', 'milliondollar']) \
#         .query('(is_test == 0) & (~db.str.contains("IV|RD", case=False, na=False))')

# v = ['VAU1', 'VAU2', 'VAU3', 'VAU4', 'VAU5', 'VAU6', 'VUK1', 'VUK2', 'VUK3', 'VUK4', 'VUK5', 'VUK6', 'VUK7', 'VUK8', 'VUK9'
#      'VT', 'VT2', 'VT3', 'VT4', 'VT5', 'VT6', 'PUG', 'PUG2', 'PUG3', 'PUG4', 'PUG5', 'OPL',
#      'VGP_UK','Moneta01','PUG_MT5','VFX-MT5','MT5-UK']

# i = ['IUK','BHSCN','BHS','BHS3','INF06','INF08','INF08_MT5','INFINOX_MT5']


# rank_v = million_all.query(f'db.isin({v})') \
#                     .groupby('clean_symbol',as_index=False).sum() \
#                     .sort_values(by='milliondollar', ascending=False)  \
#                     .assign(million = lambda x: x.milliondollar * 2) \
#                     .head(10)



# rank_i = million_all.query(f'db.isin({i})') \
#                     .groupby('clean_symbol',as_index=False).sum() \
#                     .sort_values(by='milliondollar', ascending=False)  \
#                     .assign(million = lambda x: x.milliondollar * 2) \
#                     .head(10)

