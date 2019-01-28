from django.http import HttpResponse
import quandl
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

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
    print(signals)
    
     
    
    import matplotlib.pyplot as plt
    
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
    
    return HttpResponse(plt.show())







