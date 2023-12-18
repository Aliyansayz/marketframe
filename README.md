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



symbols_forex = [
    'AUDCAD=X', 'AUDCHF=X', 'AUDJPY=X', 'AUDNZD=X', 'AUDUSD=X',
    'CADCHF=X','CADJPY=X' ,
    'CHFJPY=X',
    'EURAUD=X', 'EURCAD=X', 'EURCHF=X', 'EURGBP=X', 'EURJPY=X', 'EURNZD=X', 'EURUSD=X',
    'GBPAUD=X', 'GBPCAD=X', 'GBPCHF=X', 'GBPJPY=X', 'GBPUSD=X',  'GBPNZD=X',
    'NZDCAD=X', 'NZDCHF=X', 'NZDJPY=X', 'NZDUSD=X',
    'USDCHF=X', 'USDCAD=X', 'USDJPY=X'
]
