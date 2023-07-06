import os
import openpyxl
import pandas as pd
import numpy as np
import csv

workbook = openpyxl.Workbook()
worksheet = workbook.active

# directory = 17405350002
# total_collected = 24888.28

headers = ['account','ac_code','desc','amount','proceeds','late','misc','prin paid','eff date']
c_df.columns = headers

grouped = c_df.groupby('account')
account_dfs = {}

for account_number, group in grouped:
  account_dfs[account_number] = group

account = account_dfs[directory]
df = account
account = df.iloc[0,0]
proceeds = df.iloc[0,4]


headers = ['account','payment','comment','balance','cust_pmts','pydu','disi','bbwvP','bbwvI','ddis','adis','wpay','ugap','uwar','drsv','ltca','0nf2','repo','coll','impo','mech','auct','rcdn','keys','lfe']
c_df1.columns = headers

grouped = c_df1.groupby('account')
account_dfs = {}
for account_number, group in grouped:
  account_dfs[account_number] = group

account = account_dfs[directory]
df1 = account

total_due = proceeds + 195
bb_checker = total_collected - total_due

df['prin paid'] = df['prin paid'].round(2)
prin_sum = round(df['prin paid'].sum(), 2)

if 'PYDU' or 'DHBB' in df['desc'].values:
  pydu_posted = df.loc[(df['desc'] == 'PYDU'), 'prin paid'].sum()
  dhbb_posted = df.loc[(df['desc'] == 'DHBB'), 'prin paid'].sum()
  already_collected = round(pydu_posted + dhbb_posted, 2)
  prin_sum -= (already_collected)
  prin_sum = round(prin_sum, 2)
else:
  pass

prin_sum

if bb_checker >=  0:
  pydu = total_due
elif -195 <= bb_checker < 0:
  pydu = total_collected
else:
  pydu = 0

late = df1.iloc[0,15]
NSF = df1.iloc[0,16]
repo = df1.iloc[0,17]
impo = df1.iloc[0,19]
keys = df1.iloc[0,23]
lfe = df1.iloc[0,24]

balance = df1.iloc[0,3]
remaining_balance = round(balance - pydu, 2)

#bbwvI
bbwvI = df1.iloc[0,8]

#ddis
if 'DDIS' in df['desc'].values:
  ddis = abs(df.loc[df['desc'] == 'DDIS', 'amount'].values.item())
else:
  ddis = 0

#adis
if pydu == proceeds:
  adis = abs(df.loc[df['desc'] == 'ADIS', 'amount'].values.item())
elif pydu >= total_due:
  adis = abs(df.loc[df['desc'] == 'ADIS', 'amount'].values.item()) - 195
elif pydu == 0:
  if already_collected == proceeds:
    adis = abs(df.loc[df['desc'] == 'ADIS', 'amount'].values.item())
  elif already_collected >= total_due:
    adis = abs(df.loc[df['desc'] == 'ADIS', 'amount'].values.item()) - 195

#wpay
if 'WPAY' in df['desc'].values:
  wpay = abs(df.loc[df['desc'] == 'WPAY', 'amount'].values.item())
else:
  wpay = 0

#ugap
if 'UGAP' in df['desc'].values:
  ugap = abs(df.loc[df['desc'] == 'UGAP', 'amount'].values.item())
else:
  ugap = 0

#uwar
if 'UWAR' in df['desc'].values:
  uwar = abs(df.loc[df['desc'] == 'UWAR', 'amount'].values.item())
else:
  uwar = 0

#drsv
if 'DRSV' in df['desc'].values:
  drsv = abs(df.loc[df['desc'] == 'DRSV', 'amount'].values.item())
else:
  drsv = 0

#GPSR
if 'GPSR' in df['desc'].values:
  gpsr = abs(df.loc[df['desc'] == 'GPSR', 'amount'].values.item())
else:
  gpsr = 0

#released dhfl
if 'DHFL' in df['desc'].values:
  dhfl = abs(df.loc[df['desc'] == 'DHFL', 'amount'].values.item())
else:
  dhfl = 0

#not released dhfl
if 'DHBB' in df['desc'].values:
  dhfl = abs(df.loc[df['desc'] == 'DHBB', 'amount'].values.item())
else:
  dhfl = 0

#disi
disi = ddis + 195 + ugap + uwar

#bbwvP
if adis == 0 and wpay == 0 and drsv == 0 and prin_sum == 0:
  bbwvP = round(remaining_balance - disi + 195, 2)
elif adis == 0 and wpay == 0 and drsv == 0 and prin_sum != 0:
  bbwvP = round(remaining_balance - disi + 195 + prin_sum, 2)
elif adis != 0 and prin_sum == 0:
  bbwvP = round(remaining_balance - disi, 2)
elif adis != 0 and prin_sum != 0:
  bbwvP = round(remaining_balance - disi + prin_sum, 2)
else:
  bbwvP = round(remaining_balance - disi, 2)

#cst pmts
cust_pmts = df1.iloc[0,4]

if adis == 0:

  if wpay != 0 and drsv != 0:
    if gpsr != 0:
      bbwvP_cal1 = wpay + drsv - 195 - gpsr
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
    elif gpsr == 0:
      bbwvP_cal1 = wpay + drsv - 195
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
  elif wpay != 0:
    if gpsr != 0:
      bbwvP_cal1 = wpay - 195 - gpsr
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
    elif gpsr == 0:
      bbwvP_cal1 = wpay - 195
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
  elif drsv != 0:
    if gpsr != 0:
      bbwvP_cal1 = drsv - 195 - gpsr
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
    elif gpsr == 0:
      bbwvP_cal1 = drsv - 195
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
  elif wpay == 0 and drsv == 0:
    if gpsr != 0:
      bbwvP_cal1 = -195 - gpsr
      bbwvP = round(bbwvP + gpsr, 2)
      disi += bbwvP_cal1
    elif gpsr == 0:
      bbwvP_cal1 = -195
      disi += bbwvP_cal1

elif adis == 195:

  if wpay != 0 and drsv != 0:
    if gpsr != 0:
      bbwvP_cal1 = wpay + drsv - gpsr
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
    elif gpsr == 0:
      bbwvP_cal1 = wpay + drsv
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
  elif wpay != 0:
    if gpsr != 0:
      bbwvP_cal1 = wpay - gpsr
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
    elif gpsr == 0:
      bbwvP_cal1 = wpay
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
  elif drsv != 0:
    if gpsr != 0:
      bbwvP_cal1 = drsv -gpsr
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
    elif gpsr == 0:
      bbwvP_cal1 = drsv
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
  elif wpay == 0 and drsv == 0:
    if gpsr != 0:
      bbwvP_cal1 =  -75
      bbwvP = round(bbwvP - bbwvP_cal1, 2)
      disi += bbwvP_cal1
    elif gpsr == 0:
      pass

if bb_checker > 0:
  disi -= bb_checker
  ddis -= bb_checker

disi -= prin_sum
ddis -= prin_sum

# # # Add data to the row
# data = [directory, total_collected, '', balance, cust_pmts, total_collected, disi, bbwvP, bbwvI, ddis, adis, wpay, ugap, uwar, drsv, late, NSF, '', '', '', gpsr,'','','','']

# for col_num, value in enumerate(data, start=1):
#     cell = worksheet.cell(row=1, column=col_num, value=value)

# # # data
# workbook.save('my_file.xlsx')