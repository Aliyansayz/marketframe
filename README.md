# MarketFrame
Tells us market prices in real time with technical indicators, crossover status. Sorting volatile forex pairs from non volatile and visualizing
* Bollinger Bands
* ATR Bands 
* ADX value
* Stochastic Momentum Index
* Exponential Moving Average
* Heikin Ashi Candles 

# Recommended Predefined Values

* EMA period = 5/20
  
* Stochastic Momentum Index= 20, 5, 5 -> period, SMI calculation period, SMI_based_ema
* ADX period = 8-10 ( 4 Hour/1 Hour )

* ATR period = 5 
* BB period  = 20 

* ATR multiplier = 1.7 
* BB Multiplier  = 2.0 


# Recommended Values Crypto 15 Minutes Timeframe 


* EMA period = 20/50
  
* Stochastic Momentum Index= 20, 5, 5 -> period, SMI calculation period, SMI_based_ema
* ADX period = 20 

* ATR period = 5 
* BB period  = 20 

* ATR multiplier = 1.7 
* BB Multiplier  = 2.0 



# Demostartion

## Selecting Symbols

symbols_forex = [
    'AUDCAD=X', 'AUDCHF=X', 'AUDJPY=X', 'AUDNZD=X', 'AUDUSD=X',
    'CADCHF=X','CADJPY=X' ,
    'CHFJPY=X',
    'EURAUD=X', 'EURCAD=X', 'EURCHF=X', 'EURGBP=X', 'EURJPY=X', 'EURNZD=X', 'EURUSD=X',
    'GBPAUD=X', 'GBPCAD=X', 'GBPCHF=X', 'GBPJPY=X', 'GBPUSD=X',  'GBPNZD=X',
    'NZDCAD=X', 'NZDCHF=X', 'NZDJPY=X', 'NZDUSD=X',
    'USDCHF=X', 'USDCAD=X', 'USDJPY=X'
]

## Get Data In Numpy Structured Array

bar_list = get_clean_data.get_data_np_df(symbols , interval = '1H' , period = '7d' )


chart = '1H'
step  =  1
chart_type = str(int( int(chart[0]) * step)) + str(f"{chart[-1]}")


##  Resample Data
resample = resample_data( data_list=bar_list , step=1 , rotate = False , format = 'pkt'  )

resample_list = resample.run_resample_data()

##  Lookback Mode
bar_df = indicators_lookback_mode.transform_data_list( refine_list = resample_list, multiplier= 1.7 ,\
                  atr_period = 5, adx_period = 8 , lookback = 14, ema_period = [5, 20], ha_ohlc = True )

## Sorting Pairs For Buy & Sell Trade 

#(Strategy : adx_stochastic_momentum)
sorted_data, sell_signal_list, buy_signal_list = sorting.adx_stochastic_momentum(bar_df, last_candles = 30, cross_only= True , chart_type = None )

#(Strategy : adx_crossover_ema)
sorted_data,  sell_signal_list, buy_signal_list  = sorting.adx_crossover_ema(bar_df, last_candles = 10, cross_only= False , chart_type = None )




## Signal 
print(sell_signal_list)

[['CADJPY=X',
  'sell',
  106.99999844974509,
  108.11799776607522,
  numpy.datetime64('2023-12-20T12','h'),
  None],
 ['EURAUD=X',
  'sell',
  1.6161189888125749,
  1.6327459003323226,
  numpy.datetime64('2023-12-19T19','h'),
  None],
 ['EURCHF=X',
  'sell',
  0.9423212324646401,
  0.9466138566466881,
  numpy.datetime64('2023-12-20T20','h'),
  None],
 ['EURNZD=X',
  'sell',
  1.7424071921234967,
  1.7588979111785052,
  numpy.datetime64('2023-12-19T23','h'),
  None],
 ['GBPCAD=X',
  'sell',
  1.6890379151897021,
  1.6959620752735547,
  numpy.datetime64('2023-12-20T12','h'),
  None],
 ['GBPJPY=X',
  'sell',
  181.78699966514975,
  183.54750350867837,
  numpy.datetime64('2023-12-20T11','h'),
  None],
 ['USDCAD=X',
  'sell',
  1.3312737413275333,
  1.3356562189233212,
  numpy.datetime64('2023-12-20T19','h'),
  None],
 ['USDJPY=X',
  'sell',
  142.8086540889015,
  144.28186104781724,
  numpy.datetime64('2023-12-20T13','h'),
  None]]

buy_signal_list


  
print(buy_signal_list)

[['AUDCAD=X',
  'buy',
  0.9054028337574302,
  0.8997872526073158,
  numpy.datetime64('2023-12-20T19','h'),
  None],
 ['AUDUSD=X',
  'buy',
  0.6774198494410605,
  0.6708734550022989,
  numpy.datetime64('2023-12-19T18','h'),
  None],
 ['EURCAD=X',
  'buy',
  1.4713904840660088,
  1.4579296129035957,
  numpy.datetime64('2023-12-19T21','h'),
  None],
 ['EURJPY=X',
  'buy',
  158.38416868585188,
  157.5048388825075,
  numpy.datetime64('2023-12-20T02','h'),
  None],
 ['NZDCAD=X',
  'buy',
  0.8410293932290173,
  0.8368506555228138,
  numpy.datetime64('2023-12-20T18','h'),
  None],
 ['NZDJPY=X',
  'buy',
  90.50199058976096,
  89.87500831160622,
  numpy.datetime64('2023-12-20T14','h'),
  None]]

