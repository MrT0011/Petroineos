# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 22:21:06 2022

@author: Jeffrey
"""

import pandas as pd
import datetime

df = pd.read_csv('Merge.csv')

# Sanity check
df.info()
df.describe()
df['Resolution'].unique()

consolidatedData = df.copy()
consolidatedData['Datetime'] = pd.to_datetime(consolidatedData['Datetime'])
consolidatedData['Date'] = consolidatedData['Datetime'].apply(lambda x:x.date())
consolidatedData['Datetime+1'] = consolidatedData['Datetime'] + datetime.timedelta(hours=1)
consolidatedData.set_index('Datetime+1', inplace=True)


def avg2HoursPricce (DF,freq):
    df = DF.copy()
    df = df.between_time('07:00', '17:00')
    df = df[df['Resolution'] == freq].resample('2H').mean()
    df.reset_index(inplace=True)
    df['Datetime'] = df['Datetime+1'] - datetime.timedelta(hours=1)
    df.dropna(inplace=True)
    df.rename(columns={'Price':freq},inplace=True)
    df.set_index('Datetime',inplace=True)
    df.drop('Datetime+1',axis=1,inplace=True)
    return df

tenMin = avg2HoursPricce(consolidatedData,'10MIN')
sixtyMin = avg2HoursPricce(consolidatedData,'1H')

exp = tenMin.merge(sixtyMin,left_index=True,right_index=True,how='left')
exp.reset_index(inplace=True)
exp['Date'] = exp['Datetime'].apply(lambda x:x.date())

exp = exp.merge(consolidatedData[consolidatedData['Resolution'] == 'D'][['Date','Price']],on='Date',validate='many_to_one')

exp.set_index('Datetime',inplace=True)
exp.drop('Date',axis=1,inplace=True)
exp.rename(columns={'10MIN':'10-mins', '1H':'60-mins', 'Price':'1-day'},inplace=True)

# exp is the solution DataFrame for Question 1
