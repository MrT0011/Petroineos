# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 23:27:51 2022

@author: Jeffrey
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Consumption.csv')

# Sanity check
df.info()
df.describe()

consolidatedData = df.copy()

format1 = consolidatedData[consolidatedData['Date'].str.contains('/')]
format2 = consolidatedData[~consolidatedData['Date'].str.contains('/')]

format1['Date'] = pd.to_datetime(format1['Date'],format='%d/%m/%Y')

format2['Date'].apply(lambda x:int(x)).min()
format2['Date'].apply(lambda x:int(x)).max()

format2['Datetime'] = pd.date_range(start='20200101',
                                    end='20201231',
                                    freq='D')

format2.drop('Date',axis=1,inplace=True)

consolidatedData = pd.concat([format1,format2.rename(columns={'Datetime':'Date'})],ignore_index=True)
consolidatedData['yyyy'] = consolidatedData['Date'].apply(lambda x:str(x.year))
consolidatedData['mm'] = consolidatedData['Date'].apply(lambda x:str(x.month))
consolidatedData['dd'] = consolidatedData['Date'].apply(lambda x:str(x.day))
consolidatedData['mm-dd'] = consolidatedData['mm'] + '-' + consolidatedData['dd']


exp = pd.DataFrame(index=consolidatedData['mm-dd'].unique())
exp.reset_index(inplace=True)
exp.rename(columns={'index':'mm-dd'},inplace=True)

def merge (df, year):
    temp = consolidatedData[consolidatedData['yyyy'] == year]
    temp = temp[['Consumption','mm-dd']].rename(columns={'Consumption':str(year)})
    df = df.merge(temp,on='mm-dd',how='left',validate='one_to_one')
    return df

for year in consolidatedData['yyyy'].unique():
    exp = merge(exp,year)

# Expected Table
expectedTable = exp.set_index('mm-dd')

# Plot
exp['Min'] = exp.min(axis=1)
exp['Max'] = exp.max(axis=1)
exp['Average'] = exp.mean(axis=1)

fig, ax = plt.subplots(1,1,figsize=(12, 6))

plt.fill_between(exp.index,exp['Min'],exp['Max'],alpha=0.2, label = 'Range')
plt.plot(exp['Average'],label = 'Average', linestyle='--')
plt.plot(exp['2021'],label = '2021', linestyle='-')
plt.plot(exp['2022'],label = '2022', linestyle='-')

ax.set_title('Seasonal Plot showing 5-years (2016-2020)')
ax.set_xlabel('Day of the year')
ax.set_ylabel('Consumption')

plt.legend()
plt.show()


# Please comment on your observation on the plot
'''
Observations:
1. There is a smile trend dreasing then increasing over the year
2. The minimum consumption period is always happens slightly after 200 days of the year (ie. summer)
3. The maximum consumption period is always happens at the beginning of the year (ie. winter)
4. There is a decreasing trend of consumption comparing the year of 2021 and 2022
5. Most of consumption after the time of 200th day in 2021 are below average
6. There exists a weekly seasonality
'''
