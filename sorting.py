class sorting :

    # define numpy structured array structure
    columns, values = 0 , 1
    @classmethod
    def sort_uptrend_crossover(cls, bar_df, last_candles  ):


      sort_index = []
      for index, ohlc in enumerate(bar_df[sorting.values]):

          last_candles = 3
          observe = ohlc[-3:]

          # Filter based on Average Directional Index (ADX)
          mask_adx = observe['Average-Directional-Index'] > 19

          # Filter based on Stochastic Oscillator
          # mask_stochastic = observe['Stochastic-Oscillator'] < 20
          mask_uptrend_crossover  = observe['Crossover'] == 1

          # Combine filters using logical AND
          filtered_data = observe[mask_adx & mask_uptrend_crossover]
          if  len(filtered_data) > 0 :  sort_index.append(index)

          # print(index, filtered_data)
      # Using list comprehension
      filtered_list = [ bar_df[values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index ]

      return filtered_list

    @classmethod
    def sort_downtrend_crossover(cls, bar_df,   last_candles ):

      sort_index = []
      for index, ohlc in enumerate(bar_df[sorting.values]):

          last_candles = 3
          observe = ohlc[-3:]

          # Filter based on Average Directional Index (ADX)
          mask_adx = observe['Average-Directional-Index'] > 19

          # Filter based on Stochastic Oscillator
          # mask_stochastic = observe['Stochastic-Oscillator'] < 20
          mask_downtrend_crossover  = observe['Crossover'] == -1

          # Combine filters using logical AND
          filtered_data = observe[mask_adx & mask_downtrend_crossover]
          if  len(filtered_data) > 0 :  sort_index.append(index)

          # print(index, filtered_data)
      # Using list comprehension
      filtered_list = [ bar_df[values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index ]

      return filtered_list

def sort_trend_change_early_exit(cls, bar_df,   last_candles ):

      sort_index = []
      for index, ohlc in enumerate(bar_df[sorting.values]):

          last_candles = 3
          observe = ohlc[-3:]

          # Filter based on Average Directional Index (ADX)
          mask_adx = observe['Average-Directional-Index'] > 19

          # Filter based on Stochastic Oscillator
          # mask_stochastic = observe['Stochastic-Oscillator'] < 20
          mask_downtrend_crossover  = observe['Crossover'] == -1

          # Combine filters using logical AND
          filtered_data = observe[mask_adx & mask_downtrend_crossover]
          if  len(filtered_data) > 0 :  sort_index.append(index)

          # print(index, filtered_data)
      # Using list comprehension
      filtered_list = [ bar_df[values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index ]

      return filtered_list

