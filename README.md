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

[['AUDCAD=X',
  'sell',
  0.8915670520900429,
  0.9003129594684898,
  numpy.datetime64('2023-12-16T03','h'),
  None],
 ['AUDNZD=X',
  'sell',
  1.076644272885058,
  1.0817758130219244,
  numpy.datetime64('2023-12-16T03','h'),
  None],
 ['AUDUSD=X',
  'sell',
  0.6688642610438381,
  0.6724903474919285,
  numpy.datetime64('2023-12-16T00','h'),
  None],
 ['EURGBP=X',
  'sell',
  0.8578290653728532,
  0.8609708833194686,
  numpy.datetime64('2023-12-18T06','h'),
  None],
 ['GBPCHF=X',
  'sell',
  1.1002726329738057,
  1.1076674686497294,
  numpy.datetime64('2023-12-15T21','h'),
  None],
 ['GBPNZD=X',
  'sell',
  2.0352886030782904,
  2.0476114442239557,
  numpy.datetime64('2023-12-15T20','h'),
  None],
 ['USDJPY=X',
  'sell',
  141.1493039772997,
  142.45070212621593,
  numpy.datetime64('2023-12-15T21','h'),
  None]]
  
print(buy_signal_list)

[['AUDCHF=X',
  'buy',
  0.5861029254965807,
  0.5808170211739515,
  numpy.datetime64('2023-12-16T00','h'),
  None],
 ['AUDNZD=X',
  'buy',
  1.0817152275372703,
  1.076204656190757,
  numpy.datetime64('2023-12-16T01','h'),
  None],
 ['AUDUSD=X',
  'buy',
  0.6729110406513459,
  0.6692267729167694,
  numpy.datetime64('2023-12-15T22','h'),
  None],
 ['NZDCHF=X',
  'buy',
  0.5439171970382481,
  0.5393028079971522,
  numpy.datetime64('2023-12-18T06','h'),
  None],
 ['NZDJPY=X',
  'buy',
  88.68308646245868,
  88.16891854242414,
  numpy.datetime64('2023-12-18T05','h'),
  None],
 ['NZDUSD=X',
  'buy',
  0.6247019819321772,
  0.6197756477293829,
  numpy.datetime64('2023-12-15T21','h'),
  None],
 ['USDCHF=X',
  'buy',
  0.8716922840382967,
  0.8654877105448332,
  numpy.datetime64('2023-12-15T22','h'),
  None],
 ['USDJPY=X',
  'buy',
  142.83000897408562,
  141.46198321341438,
  numpy.datetime64('2023-12-16T02','h'),
  None]]

