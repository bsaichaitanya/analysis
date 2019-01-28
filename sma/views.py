from django.http import HttpResponse
import quandl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import redirect

# Create your views here.
def graphview(request):


    equitydata = quandl.get("HKEX/02382",authtoken='Jjz7SvMpapFPhoZPAzga',pagination = True)
    #print(equitydata)
    #plotting nominal prices
    #equitydata['Nominal Price'].plot(grid=True)
    #plt.title("Sunny optical closing price")
    #plt.show()

    #making short and long windows
    short_window = 40
    long_window = 100
    signals = pd.DataFrame(index=equitydata.index)
    signals['signal'] = 0.0

    #SMA of Short window

    signals['short_mavg'] = equitydata['Nominal Price'].rolling(window=short_window,min_periods=1,center=False).mean()

    #SMA of Long WIndow
    signals['long_mavg'] = equitydata['Nominal Price'].rolling(window=long_window,min_periods=1,center=False).mean()


    # Create signals
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:],1.0,0.0)

    #Generate trading orders

    signals['positions'] = signals['signal'].diff()
    #print(signals)

    # Initialize the plot figure
    fig = plt.figure(figsize=(20,15))

    # Add a subplot and label for y—axis
    ax1 = fig.add_subplot(111, ylabel='Price in $')

    # Plot the closing price
    equitydata['Nominal Price'].plot(ax=ax1, color='black', lw=2.)

    # Plot the short and long moving averages
    signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

    # Plot the buy signals

    ax1.plot(signals.loc[signals.positions == 1.0].index,signals.short_mavg[signals.positions == 1.0],'^', markersize=20, color='g')

    # Plot the sell signals
    ax1.plot(signals.loc[signals.positions == -1.0].index,signals.short_mavg[signals.positions == -1.0],'v', markersize=20, color='r')

    # Show the plot
    plt.show()

    return redirect('http://localhost:8000/home/')

def home(request):

    html = "<!DOCTYPE html><center><html><head><style>table, th, td {  border: 1px solid black;}</style></head><body><table>  <tr><th>Moving Average Crossover</th></tr><tr>  <td><p><li>A trading signal occurs when a short-term moving average (SMA) crosses through a long-term moving average (LMA).</li><li> I defined my short-term and long-term windows to be 40 and 100 days respectively. Next, I created a new Pandas dataframe called 'signals' and create a 'signal' column in which all rows are initially assigned a value of zero. I then create columns in the 'signal' dataframe that store both Sunny Optical's SMA and the LMA. To do this, I use .rolling() and .mean() methods simultaneously.</li><li>After the above prep-work, I can finally create the trading signal. Using np.where() , I create a conditional statement that states: Any day the SMA is greater than the LMA for 40 days (duration of the short window),  a signal will be triggered and set to a value of '1'. If otherwise, the signal value remains at zero.</li><li>A 'positions' column is then created and is marked the difference between signal values of two corresponding days. A difference of '1' marks a buy signal and a difference of '-1' marks a sell signal. To make more sense of what has been done here, continue by cliking the link below where I plot everything onto a scatterplot</li>.</p></td></tr><tr><td><center><h1><a href ='http://localhost:8000/graphs/'>click</a><h1></center></td></tr></table></body></html></center>"
    return HttpResponse(html)







