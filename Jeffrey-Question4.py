# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 01:29:45 2022

@author: Jeffrey
"""

# Import libraries
import pandas as pd
import datetime

# Read CSV file
df = pd.read_csv('trades.csv')

# Sanity check
df.info()
df.describe()

# Check the variety of contracts and product
df['Contract'].unique()
df['Product'].unique()

# Deep copy the DataFrame incase of accident
consolidatedData = df.copy()
# Change TradeDateTime into datetime format
consolidatedData['TradeDateTime'] = pd.to_datetime(consolidatedData['TradeDateTime'])
consolidatedData.set_index('TradeDateTime',inplace=True)

# Find unique contracts and products
consolidatedData[['Contract','Product']].drop_duplicates()
    

def contractOHLCV(Data, contract, freq):
    '''
    This is the utility function for def resample():
    Parameters
    ----------
    Data : DataFrame
        DataFrame to draw OHLCV Data from.
    contract : str
        Contract name
    freq : DateOffset, Timedelta or str
        The offset string or object representing target conversion.

    Returns
    -------
    A single DataFrame of OHLCV data with ONE contract
    '''
    data = Data.copy()
    temp = data[data['Contract'] == contract] # Select contract
    resample = temp.resample(freq) # Create resample object
    o = resample.first()['Price'] # Calculate Open price
    o.rename('Open', inplace=True) 
    h = resample.max()['Price'] # Calculate High price
    h.rename('High', inplace=True)
    l = resample.min()['Price'] # Calculate Low price
    l.rename('Low', inplace=True)
    c = resample.last()['Price'] # Calculate Close price
    c.rename('Close', inplace=True)
    v = resample.sum()[['Quantity']] # Calculuate total volume
    v.rename(columns={'Quantity':'Volume'},inplace=True)
    contractDF = pd.concat([o,h,l,c,v], axis=1) # Combine into DataFrame
    contractDF['Contract'] = contract # Label the contract
    return contractDF
    

def resample (begin, end, products, freq):
    '''
    Parameters
    ----------
    begin : datetime
        Start date of extracting OHLCV data.
    end : datetime
        End date of extracting OHLCV data.
    products : list of str
        Available products are {'Emission - Venue A', 'Emission - Venue B','Energy'}.
    freq : DateOffset, Timedelta or str
        The offset string or object representing target conversion.

    Returns
    -------
    A single DataFrame of OHLCV data with all relevant contracts

    '''
    # Deep copy data
    data = consolidatedData.copy()
    # Initialise result DataFrame
    result = pd.DataFrame()
    
    # Please limit output within trading hours, i.e., 7:00 – 17:00, except when freq >= 1D
    if pd.Series(freq).str.contains('d|D|m|M|y|Y')[0]:
        data = data.between_time('07:00', '17:00')
    
    # The product “Emission - Venue A” and “Emission - Venue B” are the same product trading in two different venues, please combine them when queried
    if 'Emission - Venue A' in products:
        # calculate contract DA and M01
        
        DA = contractOHLCV(data,'DA', freq)
        result = pd.concat([result,DA]) # Append to result DataFrame
        
        M01 = contractOHLCV(data,'M01', freq)
        result = pd.concat([result,M01]) # Append to result DataFrame
        
    if ('Emission - Venue B' in products) and ('Emission - Venue A' not in products):
        # return contract M01
        M01 = contractOHLCV(data,'M01', freq)
        result = pd.concat([result,M01]) # Append to result DataFrame
        
    if 'Energy' in products:
        # return contract Q01
        Q01 = contractOHLCV(data,'Q01', freq)
        result = pd.concat([result,Q01]) # Append to result DataFrame
        
    return result # return result DataFrame


# Testing resample function
if __name__ == '__main__':
    test = resample (begin = datetime.datetime(year=2022, month=4, day=19, hour=0, minute=0, second=0),
                     end = datetime.datetime(year=2022, month=5, day=19, hour=0, minute=0, second=0),
                     products = ['Emission - Venue A', 'Energy'],
                     freq = '1D')
    
    