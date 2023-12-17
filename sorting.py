import numpy as np
from numpy.lib.recfunctions import append_fields

class sorting :
    # define numpy structured array structure
    columns, values = 0 , 1

    @classmethod
    def get_signal_data(cls, matches, order_type):

      symbol = matches['symbol'][0]

      if order_type == 1 :
         order       = 'buy'
         stop_loss   =  matches['atr_lower'][0]
         take_profit =  matches['atr_upper'][0]

      elif order_type == -1 :
         order       = 'sell'
         stop_loss   =  matches['atr_upper'][0]
         take_profit =  matches['atr_lower'][0]

      time  = matches['index'][0]
      return  symbol, order, stop_loss, take_profit, time


    @classmethod
    def sort_uptrend_breakout(cls, bar_df, last_candles = 10 ):

      sort_index, signal_list  =  [], []
      for index, ohlc in enumerate(bar_df[sorting.values]):

          # last_candles = 10
          observe = ohlc[-last_candles:]

          volatile_adx = (observe['Average-Directional-Index'] > 18) &  (observe['Average-Directional-Index'] < 25)

          uptrend_bb_band     = observe[(observe['High'] > observe['bb_upper']) | (observe['Close'] > observe['bb_upper']) ]
          uptrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Green'

          find    = volatile_adx & uptrend_bb_band & uptrend_heikin_ashi
          matches = observe[find]
          if  len(matches) > 0 :
              sort_index.append(index)
              symbol, order, stop_loss, take_profit, time  =  cls.get_signal_data( matches, order_type = 1 )
              signal  =  [symbol, order, stop_loss, take_profit, time]
              signal_list.append(signal)

      sorted_data = [ bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index ]

      return sorted_data, signal_list


    @classmethod
    def sort_downtrend_breakout(cls, bar_df, last_candles = 10 ):

      sort_index, signal_list  =  [], []

      for index, ohlc in enumerate(bar_df[sorting.values]):

          # last_candles = 10
          observe = ohlc[-last_candles:]

          volatile_adx = (observe['Average-Directional-Index'] > 18) &  (observe['Average-Directional-Index'] < 25)

          downtrend_bb_band      = (observe['Low'] < observe['bb_lower']) | (observe['Close'] < observe['bb_lower'])
          downtrend_heikin_ashi  = observe['Heikin-Ashi-Status'] == 'Red'

          find    = volatile_adx & downtrend_bb_band & downtrend_heikin_ashi
          matches = observe[find]
          if  len(matches) > 0 :
              sort_index.append(index)
              symbol, order, stop_loss, take_profit, time  =  cls.get_signal_data( matches, order_type = -1 )
              signal  =  [symbol, order, stop_loss, take_profit, time]
              signal_list.append(signal)

      sorted_data = [ bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index ]

      return sorted_data, signal_list


    @classmethod
    def sort_uptrend_crossover(cls, bar_df, last_candles = 10 ):


      sort_index, signal_list  =  [], []
      for index, ohlc in enumerate(bar_df[sorting.values]):

          # last_candles = 3
          observe = ohlc[-last_candles:]

          volatile_adx = (observe['Average-Directional-Index'] > 18) &  (observe['Average-Directional-Index'] < 25)
          mask_uptrend_crossover  = observe['Crossover'] == 1
          uptrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Green'

          find    =  volatile_adx & mask_uptrend_crossover & uptrend_heikin_ashi
          matches =  observe[find]
          if  len(matches) > 0 :
              sort_index.append(index)
              symbol, order, stop_loss, take_profit, time  =  cls.get_signal_data( matches, order_type = 1 )
              signal  =  [symbol, order, stop_loss, take_profit, time]
              signal_list.append(signal)

      sorted_data = [ bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index ]

      return sorted_data, signal_list

    @classmethod
    def sort_downtrend_crossover(cls, bar_df,   last_candles=10 ):

      sort_index, signal_list  =  [], []
      for index, ohlc in enumerate(bar_df[sorting.values]):

          last_candles = 3
          observe = ohlc[-last_candles:]

          volatile_adx = (observe['Average-Directional-Index'] > 18) &  (observe['Average-Directional-Index'] < 25)

          mask_downtrend_crossover  = observe['Crossover'] == -1
          downtrend_heikin_ashi  = observe['Heikin-Ashi-Status'] == 'Red'

          find    = volatile_adx & mask_downtrend_crossover & downtrend_heikin_ashi
          matches = observe[find]
          if  len(matches) > 0 :
              sort_index.append(index)
              symbol, order, stop_loss, take_profit, time  =  cls.get_signal_data( matches, order_type = -1 )
              signal  =  [symbol, order, stop_loss, take_profit, time]
              signal_list.append(signal)
      sorted_data = [ bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index ]

      return sorted_data, signal_list


    @classmethod
    def stochastic_momentum_crossover(cls, bar_df ):

        sort_index, signal_list, comments = [] , [] , []
        for index, ohlc in enumerate(bar_df[sorting.values]):
          direction = np.where(ohlc['smi'] > ohlc['smi_ema'], 1, np.where(ohlc['smi'] < ohlc['smi_ema'], -1, 0))
          ohlc = append_fields(ohlc, 'direction_smi', direction, usemask=False)
          # Add a new column 'crossover'
          crossover_values = np.where((ohlc['direction_smi'] == 1) & (np.roll(ohlc['direction_smi'], 1) == -1), 1, \
                                      np.where((ohlc['direction_smi'] == -1) & (np.roll(ohlc['direction_smi'], 1) == 1), -1, 0)) 
          ohlc    = append_fields(ohlc, 'crossover_smi', crossover_values, usemask=False)
        return bar_df

    @classmethod
    def  stochastic_momentum_uptrend(cls, bar_df, last_candles = 10 ):

      sort_index, signal_list = [] , []
      for index, ohlc in enumerate(bar_df[sorting.values]):
        observe = ohlc[-last_candles:]
        volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] < 25)
        mask_downtrend_crossover  = observe['crossover_smi']   == 1
        downtrend_heikin_ashi  = observe['Heikin-Ashi-Status'] == 'Green'
        find    = volatile_adx & mask_downtrend_crossover & downtrend_heikin_ashi
        matches = observe[find]
        if  len(matches) > 0 :
              sort_index.append(index)
              symbol, order, stop_loss, take_profit, time  =  cls.get_signal_data( matches, order_type = -1 )
              signal  =  [symbol, order, stop_loss, take_profit, time]
              signal_list.append(signal)

      sorted_data = [ bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index ]

      return sorted_data, signal_list

    @classmethod
    def  stochastic_momentum_downtrend(cls, bar_df, last_candles = 10 ):

      sort_index, signal_list = [] , []
      for index, ohlc in enumerate(bar_df[sorting.values]):
        observe = ohlc[-last_candles:]
        volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] < 25)
        mask_downtrend_crossover  = observe['crossover_smi'] == -1
        downtrend_heikin_ashi  = observe['Heikin-Ashi-Status'] == 'Red'

        find    = volatile_adx & mask_downtrend_crossover & downtrend_heikin_ashi
        matches = observe[find]
        if  len(matches) > 0 :
              sort_index.append(index)
              symbol, order, stop_loss, take_profit, time  =  cls.get_signal_data( matches, order_type = -1 )
              signal  =  [symbol, order, stop_loss, take_profit, time]
              signal_list.append(signal)

      sorted_data = [ bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index ]

      return sorted_data, signal_list

    @classmethod
    def sort_trend_change_early_exit(cls, bar_df,   last_candles = 10  ):

      sort_index, signal_list, comments = [] , [] , []
      for index, ohlc in enumerate(bar_df[sorting.values]):

          last_candles = 3
          observe = ohlc[-last_candles:]

          # Filter based on Average Directional Index (ADX)
          volatile_adx = observe['Average-Directional-Index'] > 20

          mask_downtrend_crossover  = observe['Crossover'] == -1
          mask_uptrend_crossover    = observe['Crossover'] ==  1
          down =  np.where(mask_downtrend_crossover)
          up   =  np.where(mask_uptrend_crossover)
          # np.where

          # Combine filters using logical AND
          matches = observe[volatile_adx & mask_downtrend_crossover]
          symbol = observe['symbol'][0]

          if  len(up) > 1 or len(down) > 1 :
                  sort_index.append(index)

                  if up[0] < down[0]:   comments.append(f" Uptrend came at {observe['index'][up[0]]} but downward-crossover changed situation")
                  else: comments.append(f" Downtrend came at {observe['index'][down[0]]} but upward-crossover changed situation")


                  if up[0] != up[-1] or down[0] != down[-1]:

                    comments.append(f" Use Higher TimeFrame With 200 EMA/50 and ADX 20 period")

                    if up[-1] < down[-1]:  comments.append(f" Downtrend came at {observe['index'][down[-1]]} situation changed may close buy\
                                                          trades after seeing chart, adx status and heikin ashi candles")

                    if up[-1] > down[-1]:  comments.append(f" Uptrend came at {observe['index'][up[-1]]} situation changed may close sell\
                                                          trades after seeing chart, adx status and heikin ashi candles")
                    signal = [ symbol, comments ]
                    signal_list.append(signal)


          elif  len(up) == 1 and len(down) != 0 :
                  sort_index.append(index)
                  comments.append(f" One up-crossover  Use Higher TimeFrame With 200 EMA/50 and ADX 20 period")

                  if up[0] < down[0]:   comments.append(f" Uptrend came at {observe['index'][up[0]]} but downward-crossover changed situation")
                  else: comments.append(f" Downtrend came at {observe['index'][down[0]]} but upward-crossover changed situation")

                  if up[0] != up[-1] or down[0] != down[-1]:
                      comments.append(f" Use Higher TimeFrame With 200 EMA/50 and ADX 20 period")

                      if up[-1] < down[-1]:  comments.append(f" Downtrend came at {observe['index'][down[-1]]} situation changed may close buy\
                                                            trades after seeing chart, adx status and heikin ashi candles")
                      if up[-1] > down[-1]:  comments.append(f" Uptrend came at {observe['index'][up[-1]]} situation changed may close sell\
                                                            trades after seeing chart, adx status and heikin ashi candles")
                  signal = [ symbol, comments ]
                  signal_list.append(signal)


          elif  len(down) == 1 and len(up) != 0 :
                  sort_index.append(index)
                  comments.append(f" One down-crossover and tried   Use Higher TimeFrame With 200 EMA/50 and ADX 20 period")

                  if up[0] < down[0]:   comments.append(f" Uptrend came at {observe['index'][up[0]]} but downward-crossover changed situation")
                  else: comments.append(f" Downtrend came at {observe['index'][down[0]]} but upward-crossover changed situation")

                  if up[0] != up[-1] or down[0] != down[-1]: comments.append(f" Use Higher TimeFrame With 200 EMA/50 and ADX 20 period")

                  if up[-1] < down[-1]:  comments.append(f" Downtrend came at {observe['index'][down[-1]]} situation changed may close buy\
                                                         trades after seeing chart, adx status and heikin ashi candles")
                  if up[-1] > down[-1]:  comments.append(f" Uptrend came at {observe['index'][up[-1]]} situation changed may close sell\
                                                         trades after seeing chart, adx status and heikin ashi candles")
                  signal = [ symbol, comments ]
                  signal_list.append(signal)

          else:
                  continue
      sorted_data = [ bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index ]

      return sorted_data, signal_list
