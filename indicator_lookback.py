"""
bar_df = indicators_lookback_mode.transform_data_list( refine_list = refined_list, multiplier= 1.7 , atr_period = 5,  adx_period = 8 ,   lookback = 1  , ha_ohlc = True)
print(bar_df)

"""
from numpy.lib.recfunctions import append_fields

class  indicators_lookback_mode( access_indicators ):

  @classmethod
  def transform_data_list(cls, refine_list ,  multiplier= 1.7 , atr_period = 5,  adx_period = 8,   lookback = 10, ema_period = [5, 20], ha_ohlc = True ):

    symbols   = 0
    values    = 1
    indicator = cls() # universal class of project => access_indicator

    heikin_ashi = indicator.get_heikin_ashi (bar_list = refine_list,  ohlc_data=True)

    # crossover_direction_list  =  adx_atr_bands_indicator.crossover_direction_lookback(bar_list = refine_list, lookback = lookback )
    ha_status_list = indicator.get_heikin_ashi ( refine_list, lookback = lookback)
    if ha_ohlc :
      refine_list = indicator.normal_to_ha(data_list = refine_list, ha_ohlc_list = heikin_ashi )

    ha_ohlc_list = indicator.get_heikin_ashi (bar_list = refine_list, lookback = lookback, ohlc_data=True)

    crossover_direction_list   =  indicator.crossover_direction_lookback(bar_list = refine_list, ema_period = ema_period ,lookback = lookback )

    stochastic_momentum_list =  indicator.stochastic_momentum_lookback( bar_list = refine_list, period = ema_period[1], lookback = lookback, ema_period = 5)

    stochastic_momentum_crossover_list = indicator.stochastic_momentum_lookback( bar_list = refine_list, period = ema_period[1], lookback = lookback, ema_period = ema_period[0], crossover_direction=True)
    emaz_list  =  indicator.ema_lookback( bar_list = refine_list, lookback = lookback , ema_period = ema_period )

    atr_bands_list = indicator.atr_bands_lookback( refine_list , multiplier,  period = atr_period ,  lookback = lookback  )
    adx_value_list = indicator.adx_lookback( bar_list = refine_list,   period = adx_period , lookback = lookback)

    channel_list, trend_outofchannel_list = indicator.get_linear_regression_channel_lookback(bar_list= refine_list , period=21, dev_multiplier=2.0, lookback = lookback )
    bollinger_bands_list = indicator.get_bollinger_bands( bar_list= refine_list, lookback = lookback )

    # lookback = 10
    dt   = np.dtype([ ('index', 'datetime64[h]'),  ('symbol', 'U20'), ('Open', float ), ('High', float ), ('Low', float),  ('Close', float ),  ('Heikin-Ashi-Status', 'U10'),  ('Direction', float), ('Average-Directional-Index', float), ('Crossover', float),   \
        ('Stop_Loss', float), ('Take_Profit', float), ('direction_smi', float), ('crossover_smi', float), ('ema_low', float), ('ema_high', float), ('smi', float), ('smi_ema', float), ('', 'U10' ), ('trend_status', 'U10' ), ('outofchannel_status', 'U10' ), ('bb_lower', float ), ('bb_upper', float), ('atr_lower', float), ('atr_upper', float ), ('ha_open', float), ('ha_high', float),('ha_low', float),('ha_close', float)  ])


    column_names = dt.names
    data = [[0]]  * len(refine_list[symbols])

    for sym , ohlc in enumerate(refine_list[values]):

            index  = ohlc['index'][-lookback:]
            symbol = ohlc['symbol'][-lookback:]
            open   = ohlc['Open'][-lookback:]
            high   = ohlc['High'][-lookback:]
            low    = ohlc['Low'][-lookback:]
            close  = ohlc['Close'][-lookback:]

            heikin_ashi_status = [  element for element in ha_status_list[sym]  ]

            # fractal_status  = [ element  for  element in ha_ohlc_list[sym]  ]
            ha_open , ha_close = [ element for  element in ha_ohlc_list[sym][0] ], [ element for  element in ha_ohlc_list[sym][3] ]
            ha_high , ha_low   = [ element for  element in ha_ohlc_list[sym][1] ], [ element for  element in ha_ohlc_list[sym][2] ]

            smi =     [ element[0] for element in stochastic_momentum_list[sym] ]
            smi_ema = [ element[1] for element in stochastic_momentum_list[sym] ]

            trend_status        = [ element[0] for element in trend_outofchannel_list[sym] ]
            outofchannel_status = [ element[1] for element in trend_outofchannel_list[sym] ]

            direction_smi = [ element[0] for element in stochastic_momentum_crossover_list[sym] ]
            crossover_smi = [ element[1] for element in stochastic_momentum_crossover_list[sym] ]


            adx_value  = [  element    for element in adx_value_list[sym]  ]
            lower_band = [  element[0] for element in atr_bands_list[sym]  ]
            upper_band = [  element[1] for element in atr_bands_list[sym]  ]

            bb_lower = [  element[0] for element in bollinger_bands_list[sym]  ]
            bb_upper = [  element[1] for element in bollinger_bands_list[sym]  ]
            bb_bands = [ bb_lower,  bb_upper ]
            # crossover =   crossover_direction_list[index][dynamic--for next values of crossover of date time index][0-->static for crossover]
            crossover = [ element[0] for element in crossover_direction_list[sym] ]
            direction = [ element[1] for element in crossover_direction_list[sym] ]

            short_ema = [ element[0] for element in emaz_list[sym] ]
            long_ema  = [ element[1] for element in emaz_list[sym] ]
            # ha_ohlc_list[symbol]   =  [ha_open, ha_high, ha_low, ha_close]
            ha_ohlc = [ element for  element in  ha_ohlc_list[sym] ]

            ohlc_df = np.empty(len(close), dtype=dt)

            for i in range(0 , len(ohlc_df)):

                stop_loss   = 0
                take_profit = 0
                if crossover[i] == 1  or  direction[i] == 1 :
                      stop_loss   = lower_band[i]
                      take_profit = upper_band[i]

                elif crossover[i] == -1  or  direction[i] == -1 :
                      stop_loss   = upper_band[i]
                      take_profit = lower_band[i]

                ohlc_df[i] = ( index[i], symbol[i], open[i], high[i], low[i], close[i], heikin_ashi_status[i], direction[i], adx_value[i], \
                               crossover[i], stop_loss, take_profit, direction_smi[i] , crossover_smi[i],  short_ema[i], long_ema[i], smi[i], smi_ema[i], trend_status[i], outofchannel_status[i], bb_lower[i], bb_upper[i], lower_band[i], upper_band[i], ha_open[i], ha_high[i] , ha_low[i], ha_close[i]  )
#

            data[sym] = ohlc_df

    return [column_names, data]
