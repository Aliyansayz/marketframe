"""
# symbols = [ 'CHFJPY=X'  ]
# # symbols = [ 'BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'SOL-USD', 'STETH-USD', 'ADA-USD', 'DOGE-USD', 'TRX-USD', 'LTC-USD' ]
# bar_list = get_clean_data.get_data_np_df(symbols , interval = '1H' , period = '7d' )
# resample = resample_data( data_list=bar_list , step=4 , rotate = True , format = 'pkt'  )
#refine.chart_version( bar_list=bar_list, step=3, rotate = True, format = None )

# resample_list = resample.run_resample_data()
# # OR
# refine_list = resample.run_resample_data()
# resample_list
# bar_df = indicators_lookback_mode.transform_data_list( refine_list = resample_list, multiplier= 1.7 , atr_period = 5,  adx_period = 8 ,   lookback = 10  )
# print(bar_df)
                """
# ema_period     =  [ 5 , 20 ]
import yfinance as yf

symbols_forex = [
    'AUDCAD=X', 'AUDCHF=X', 'AUDJPY=X', 'AUDNZD=X', 'AUDUSD=X',
    'CADCHF=X','CADJPY=X' ,
    'CHFJPY=X',
    'EURAUD=X', 'EURCAD=X', 'EURCHF=X', 'EURGBP=X', 'EURJPY=X', 'EURNZD=X', 'EURUSD=X',
    'GBPAUD=X', 'GBPCAD=X', 'GBPCHF=X', 'GBPJPY=X', 'GBPUSD=X',  'GBPNZD=X',
    'NZDCAD=X', 'NZDCHF=X', 'NZDJPY=X', 'NZDUSD=X',
    'USDCHF=X', 'USDCAD=X', 'USDJPY=X'
]

# symbols = [ 'BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'SOL-USD', 'STETH-USD', 'ADA-USD', 'DOGE-USD', 'TRX-USD', 'LTC-USD' ]
# symbols = [ 'BTC-USD', 'ETH-USD' ]

bar_list = get_clean_data.get_data_np_df(symbols , interval = '1H' , period = '7d' )

# resample = resample_data( data_list=bar_list , step=4 , rotate = True , format = 'pkt'  )
resample = resample_data( data_list=bar_list , step=1 , rotate = False , format = 'pkt'  )

resample_list = resample.run_resample_data()

bar_df = indicators_lookback_mode.transform_data_list( refine_list = resample_list, multiplier= 1.7 ,\
                  atr_period = 5, adx_period = 8 , lookback = 14, ema_period = [5, 20], ha_ohlc = True )

