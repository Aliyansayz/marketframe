class ema_indicator:

    def __init__(self, data_list = None  ):

        self.data_list = data_list


    def ema (self, array, period ):

        ema = np.empty_like(array)
        ema = np.full( ema.shape , np.nan)
        ema[0] = np.mean(array[0] , dtype=np.float64)
        alpha  = 2 / (period + 1)
        # Calculate the EMA for each window of 14 values
        for i in range(1 , len(array) ):
              ema[i] = np.array( (array[i] * alpha +  ema[i-1]  * (1-alpha) ) , dtype=np.float16 )

        return ema


    def run(self ):

      if self.data_list :
        # constants
        symbols = 0  # index 0 for symbols
        values  = 1  # index 1 for ohlc

        crossover_direction = [[0]]  * len(self.data_list[symbols])

        # crossover_direction_list  = [  bar_list[symbols][name] , crossover_direction ]

        for  symbol, ohlc in enumerate(self.data_list[values]) :

              crossover,  direction     = self.crossover_and_direction( np.array(ohlc['Close'], ohlc['Open']  ) )
              crossover_direction[symbol] =   [crossover,  direction]

        crossover_direction_list  = [  self.data_list[symbols] , crossover_direction ]
        return  crossover_direction_list


    def crossover_and_direction_archived (self, array):

      short_ema  = self.ema(array , 5 )[-1]
      long_ema   = self.ema(array , 20 )[-1]

      # excluding last element from array
      # Caution using third last value for comparision instead second last

      # Experiment for forex pairs : if crossover difficult to detect and show 0 direction we can go with candle index open vs close price
      # if index or candle bullish then upward crossover
      # else if index or candle bearish then downward crossover

      prev_short_ema =   self.ema(array[:-1] , 5 )[-1]
      prev_long_ema  =   self.ema(array[:-1] , 20 )[-1]

      crossover  = direction  = 0

      if prev_short_ema < prev_long_ema and short_ema > long_ema :

            crossover = direction = 1

      elif prev_short_ema > prev_long_ema and short_ema < long_ema :

            crossover = direction = -1

      else:
           if   short_ema > long_ema :
                    direction = 1

           elif short_ema < long_ema  :
                    direction = -1

          #  elif short_ema ==  long_ema  :
          #         direction =

      return  crossover , direction

    # def crossover_direction_lookback(self, bar_list, lookback):

    #     return type(bar_list)  period
    def crossover_and_direction(self, array_close, array_open, ema_period = [5,20] ):
        # ema_period     =  [ 5 , 20 ]
        short_ema  = self.ema(array_close , 5 )[-1]
        long_ema   = self.ema(array_close , 20 )[-1]

        prev_short_ema =   self.ema(array_close[:-1] , ema_period[0] )[-1]
        prev_long_ema  =   self.ema(array_close[:-1] , ema_period[1] )[-1]
        crossover , direction  = 0 , 0

        if prev_short_ema < prev_long_ema and short_ema > long_ema :
              crossover , direction  = 1 , 1

        elif prev_short_ema > prev_long_ema and short_ema < long_ema :
              crossover , direction  = -1 , -1

        else:
            if   short_ema > long_ema :
                      direction = 1

            elif short_ema < long_ema  :
                    direction = -1
            #this means :    long_ema = short_ema True
            elif array_close[-1]  > array_open[-1]  :
                  crossover  = direction = 1
            elif array_open[-1] > array_close[-1]   :
                  crossover  = direction = -1
                  # direction =
        return  crossover , direction


    def  ema_lookback(self, bar_list , ema_period = [5,20] , lookback ):

        symbols  = 0
        values   = 1

        emaz_list = [[0]] * len(bar_list[symbols])

        for  symbol , ohlc in enumerate(bar_list[values]):

            emaz = [[0]]  * lookback

            start_index = len(ohlc['Close'])-lookback
            for i in range( (len(ohlc['Close'])-lookback), (len(ohlc['Close'])), 1):

                 short_ema  = self.ema(array , ema_period[0] )[-1]
                 long_ema   = self.ema(array , ema_period[1] )[-1]
                 emaz[ i-start_index ] = [ short_ema, long_ema ]

            emaz_list[symbol] =  emaz

        return emaz_list


    def crossover_direction_lookback(self, bar_list, ema_period =[5,20], lookback = 10):
        symbols  = 0
        values   = 1

        crossover_direction_list = [[0]] * len(bar_list[symbols])

        for  symbol , ohlc in enumerate(bar_list[values]):

            crossover_direction = [[0]]  * lookback

            start_index = len(ohlc['Close'])-lookback

            for i in range( (len(ohlc['Close'])-lookback), (len(ohlc['Close'])), 1):

                 crossover, direction =  self.crossover_and_direction( ohlc['Close'][:i] , ohlc['Open'][:i], ema_period )
                 crossover_direction[ i-start_index ] = [ crossover, direction ]

            crossover_direction_list[symbol] =  crossover_direction

        return crossover_direction_list

    def crossover_direction_lookback_archived(self, bar_list, lookback = 10):

       symbols  = 0
       values   = 1

       crossover_direction_list = [[0]] * len(bar_list[symbols])

       for  symbol , ohlc in enumerate(bar_list[values]):

            crossover_direction = [[0]]  * lookback

            start_index = len(ohlc['Close'])-lookback

            for i in range( (len(ohlc['Close'])-lookback), (len(ohlc['Close'])), 1):

                 crossover, direction =  self.crossover_and_direction_archived(array = ohlc['Close'][:i] )
                 crossover_direction[ i-start_index ] = [ crossover, direction ]

            crossover_direction_list[symbol] =  crossover_direction

       return crossover_direction_list

# ema_indicator.transform_data_list(bar_list, lookback, crossover_direction_list  )


#___________________________________________________________________________________________________

class atr_bands_indicator ( ema_indicator):

  def  __init__(self,  data_list= None ):

      self.data_list = data_list
      # , period=8, multiplier= 2.0 , lookback = None

  def  get_atr_bands(self, bar_list, period=5 , multiplier= 1.7  ):

        # constants
        symbols = 0  # index 0 for symbols
        values  = 1  # index 1 for ohlc
        atr_bands = [[0]]  * len(bar_list[symbols])

        for  index, ohlc in enumerate(bar_list[values]) :

              close = ohlc['Close']
              high  = ohlc['High']
              low   = ohlc['Low']

              lower_band,  upper_band   = self.atr_bands( close, high, low, multiplier, period  )

              atr_bands[index]   = [ [lower_band[i],  upper_band[i]] for i in range(len(lower_band)) ]

        atr_bands_list  = [  bar_list[symbols] , atr_bands ]

        return   atr_bands_list


  def  atr_bands(self, close,  high,  low,  multiplier,  period ):

        # multiplier = 2.0 / 1.7
        close_shift = self.shift(close , 1)
        high_low, high_close, low_close  = np.array( high - low ,dtype=np.float32) ,\
        np.array(abs(high - close_shift  ),dtype=np.float32 ) , \
        np.array(abs(low -  close_shift  ) ,dtype=np.float32 )

        true_range = np.max(np.hstack( (high_low, high_close, low_close) ).reshape(-1,3),axis=1 )
        # true_range[true_range == 0] = 0.0001

        # nan_indices = np.where(np.isnan(true_range))
        mean = np.nanmean(true_range)
        true_range[np.isnan(true_range)] = mean

        # true_range = self.missing_nan(true_range)
        avg_true_range = self.smoothed(true_range, period)

        price =        close
        upper_band =   price + (multiplier * avg_true_range)
        lower_band =   price - (multiplier * avg_true_range)

        return   lower_band , upper_band

  def  shift(self, array , place):

        array =  np.array(array, dtype= np.float32)

        shifted = np.roll(array, place)
        shifted[0:place]  = np.nan
        shifted[np.isnan(shifted)] = np.nanmean(shifted)

        return shifted

  def  smoothed(self, array, period , alpha = None):

        ema = np.empty_like(array)
        ema = np.full( ema.shape , np.nan)
        ema[0] = np.mean(array[0] , dtype=np.float16)
        if alpha == None:
          alpha = 1 / ( period )

        for i in range(1 , len(array) ):
              ema[i] = np.array( (array[i] * alpha +  ema[i-1]  * (1-alpha) ) , dtype=np.float32 )

        ema[np.isnan(ema)] = np.nanmean(ema)
        return ema


  def  atr_bands_lookback(self,  bar_list,  multiplier = 1.7,  period = 5,  lookback = 10 ):

        values   = 1
        symbols  = 0
        atr_bands_list = [[0]] * len(bar_list[symbols])

        for  symbol , ohlc in enumerate(bar_list[values]):

          close = ohlc['Close']
          high  = ohlc['High']
          low   = ohlc['Low']

          lower_band,  upper_band   = self.atr_bands( close, high, low, multiplier, period )

          lower_band = lower_band[-lookback:]
          upper_band = upper_band[-lookback:]

          atr_bands = [ [ lower_band[i], upper_band[i]] for i in range( lookback )]
          atr_bands_list[symbol] =  atr_bands

        return atr_bands_list

  def sma(self, array, period):

      weights = np.ones(period) / period
      arr     =  np.convolve(array, weights, mode='valid')

      window = period - 1
      sma = np.empty(window + len(arr), dtype=arr.dtype)
      sma[:window] = np.nan * window
      sma[window:] = arr
      sma[np.isnan(sma)] = np.nanmean(arr[:period])

      return sma



import numpy as np

# atr_bands_indicator
# get_atr_bands



# adx = adx_indicator (data_list = bar_list  )

#___________________________________________________________________________________________________

# adx = adx_indicator(bar_list)
# adx_value_list = adx.run_adx()
#

class adx_indicator( atr_bands_indicator):

  def  __init__(self, data_list = None, period= 14  ):

        self.data_list = data_list
        self.period = period

  def  run_adx(self):

        adx_value_list = self.get_adx(self.data_list, self.period )

        return adx_value_list

  def  get_adx(self, bar_list, period ):

        symbols = 0
        values  = 1
        adx_value = [[0]]  * len(bar_list[symbols])

        for  index, ohlc in enumerate(bar_list[values]) :

              close = ohlc['Close']
              high  = ohlc['High']
              low   = ohlc['Low']
              adx   = self.adx( close, high, low, period )

              adx_value[index]   =  adx

        adx_value_list  = [  bar_list[symbols] , adx_value ]

        return  adx_value_list

  def  adx(self, close, high, low, period = 8 ):

      true_range   = self.true_range( high, low, close  )
      highs , lows =   high - self.shift(high , 1 ) ,  self.shift(low , 1) - low

      pdm = np.where(highs > lows  , highs , 0.0 )
      ndm = np.where(lows  > highs , lows , 0.0  )

      smoothed_atr  = self.smoothed(true_range , period)
      smoothed_atr[smoothed_atr==0] = np.nanmean(smoothed_atr)
      # smoothed_atr[smoothed_atr == 0] = 0.0001

      pdi_value =   self.smoothed( pdm , period) / smoothed_atr
      pdi = pdi_value * 100
      pdi[pdi==0] = np.nanmean(pdi)
      # pdi[pdi == 0] = 0.0001

      ndi_value = self.smoothed( ndm , period) / smoothed_atr
      ndi =  ndi_value * 100
      ndi[ndi==0] = np.nanmean(ndi)
      # ndi[ndi == 0] = 0.0001

      dx = ( abs(pdi - ndi) ) / ( abs(pdi + ndi) ) * 100

      adx =   self.smoothed(dx, period)

      return adx

  def true_range(self, high, low, close ):

        close_shift = self.shift(close , 1)
        high_low, high_close, low_close  = np.array( high - low ,dtype=np.float32) ,\
        np.array(abs(high - close_shift  ),dtype=np.float32 ) , \
        np.array(abs(low -  close_shift  ) ,dtype=np.float32 )

        true_range = np.max(np.hstack( (high_low, high_close, low_close) ).reshape(-1,3),axis=1 )

        return true_range

  def shift(self, array , place):

      array =  np.array(array, dtype= np.float64)

      shifted = np.roll(array, place)
      shifted[0:place]  = 0.0

      return shifted

  def sma(self, array, period):

      weights = np.ones(period) / period
      arr     =  np.convolve(array, weights, mode='valid')

      window = period - 1
      sma = np.empty(window + len(arr), dtype=arr.dtype)
      sma[:window] = np.nan * window
      sma[window:] = arr
      sma[np.isnan(sma)] = np.nanmean(arr[:period])

      return sma

  def  adx_lookback(self,   bar_list, period = 8 , lookback = 10):


      symbols  = 0
      values   = 1
      adx_values_list = [[0]] * len(bar_list[symbols])

      for  symbol , ohlc in enumerate(bar_list[values]):

        close = ohlc['Close']
        high  = ohlc['High']
        low   = ohlc['Low']

        adx   = self.adx( close, high, low, period )

        adx_values = adx[-lookback:]

        adx_values_list[symbol] =  adx_values

      return adx_values_list


#___________________________________________________________________________________________________

class heikin_ashi (adx_indicator):

  def __init__(self, refine_list = None):

      self.refine_list = refine_list

  def run_heikin_ashi(self, refine_list ):

      ha_status_list = self.get_heikin_ashi(self, bar_list )

      return  ha_status_list

  def heikin_ashi_status(self, ha_open , ha_close ):

      candles =  np.full_like( ha_close, '', dtype='U10')

      for i in range(1 , len(ha_close) ):

            # green_condition =  ha_close[i] > ha_open[i]
            # red_condition   =  ha_close[i] < ha_open[i]
            if ha_close[i] > ha_open[i] :
              candles[i]  = 'Green'

            elif ha_close[i] < ha_open[i] :
              candles[i]  = 'Red'

            else:
              candles[i] = 'Neutral'

      return  candles


  def heikin_ashi_candles (self, open, high, low, close ):

      ha_close =  np.empty(len(close), dtype=np.float32 )

      ha_high = np.empty(len(close), dtype=np.float32 )
      ha_low  = np.empty(len(close), dtype=np.float32 )
      ha_open = np.empty(len(close), dtype=np.float32 )

      # candles =  np.empty(len(close) , dtype='U10')
      # candles = [[]] *  len(close) , dtype=np.int16

      ha_open[0]  = (open[0] + close[0] ) /2
      ha_close[0] = (close[0] + open[0] + high[0] + low[0]) /4

      for i in range(1 , len(close) ):
            ha_open[i]  = (ha_open[i-1] + ha_close[i-1] ) / 2
            ha_close[i] = (open[i] +  high[i] + low[i] + close[i]) / 4
            ha_high[i]  = max( high[i], ha_open[i], ha_close[i]  )
            ha_low[i]   = min( low[i], ha_open[i], ha_close[i]  )

      return   ha_open, ha_close, ha_high, ha_low


  def get_heikin_ashi (self, bar_list, lookback = None, ohlc_data=None):

      symbols  = 0
      values   = 1
      ha_status_list = [[]] * len(bar_list[symbols])
      ha_ohlc_list   = [[]] * len(bar_list[values])
      # np.empty(len(bar_list[symbols]), dtype='U10')

      for  symbol , ohlc in enumerate(bar_list[values]):

          open, high,  low, close  = ohlc['Open'],  ohlc['High'],  ohlc['Low'], ohlc['Close']

          ha_open, ha_close, ha_high, ha_low   =  self.heikin_ashi_candles( open, high, low, close )
          candles  =  self.heikin_ashi_status(ha_open , ha_close)

          if lookback :
            candles  =  candles[-lookback:]
            ha_open, ha_close, ha_high, ha_low = ha_open[-lookback:], ha_close[-lookback:], ha_high[-lookback:], ha_low[-lookback:]
            # ha_open_close  = [ ha_open[-lookback:] , ha_close[-lookback:] ]

          ha_ohlc_list[symbol]   =  [ha_open, ha_high, ha_low, ha_close]
          ha_status_list[symbol] = candles

      if  ohlc_data == True :

          return ha_ohlc_list

      return ha_status_list

  def normal_to_ha(self, data_list , ha_ohlc_list):

        symbols = 0  # index 0 for symbols
        values  = 1  # index 1 for ohlc

        for  sym, ohlc in enumerate(data_list[values]) :
              ha_open , ha_close = [ element for  element in ha_ohlc_list[sym][0] ], [ element for  element in ha_ohlc_list[sym][3] ]
              ha_high , ha_low   = [ element for  element in ha_ohlc_list[sym][1] ], [ element for  element in ha_ohlc_list[sym][2] ]

              ohlc['Close'], ohlc['Open'] = ha_close  ,  ha_open
              ohlc['High'] , ohlc['Low']  = ha_high   ,  ha_low
              # lower_band,  upper_band   = atr_bands( close, high, low, multiplier, period  )
        return   data_list

#___________________________________________________________________________________________________

class bollinger_bands(heikin_ashi):

  def __init__(self, refine_list = None):

      self.refine_list = refine_list


  def sma(self, array, period):

      weights = np.ones(period) / period
      arr     =  np.convolve(array, weights, mode='valid')

      window = period - 1
      sma = np.empty(window + len(arr), dtype=arr.dtype)
      sma[:window] = np.nan * window
      sma[window:] = arr
      sma[np.isnan(sma)] = np.nanmean(arr[:period])

      return sma


  def std_dev(self, array, period):

      # Calculate the squared deviations from the mean
      squared_deviations = (array - self.sma(array, period ) )**2

      # Calculate the average squared deviations
      average_squared_deviations = self.sma(squared_deviations, period)

      # Calculate the rolling standard deviation
      std_dev = np.sqrt(average_squared_deviations)

      return std_dev

  def run_bollinger_bands(self, refine_list ):

      bollinger_bands_list = self.get_bollinger_bands(bar_list = refine_list )
      return  bollinger_bands_list

  def bollinger_bands(self , high, low, close, period = 20, mult = 2.0   ):

      # bollinger_bands
      if not period or mult :
          period = 20
          k  =  2.0
      k = mult

      typical_price =  (high + low + close) / 3
      typical_price_ma  = self.sma(typical_price, period )
      # diff = (typical_price - typical_price_ma)
      # sd   = np.sqrt( diff** 2 /period )
      std_dev =  self.std_dev( typical_price,  period )

      upper_band = typical_price_ma + (k * std_dev )
      lower_band = typical_price_ma - (k * std_dev )

      return lower_band , upper_band


  def get_bollinger_bands (self, bar_list, lookback = None ):

      symbols  = 0
      values   = 1
      bollinger_bands_list  =  [[]] * len(bar_list[values])
      # np.empty(len(bar_list[symbols]), dtype='U10')

      for  symbol , ohlc in enumerate(bar_list[values]):

          high,  low,   close      =   ohlc['High'],  ohlc['Low'],  ohlc['Close']
          lower_band , upper_band  =  self.bollinger_bands( high, low, close )

          if lookback :
            lower_band , upper_band    =  lower_band[-lookback:],  upper_band[-lookback:]

          bb_bands = [ [ lower_band[i], upper_band[i]] for i in range( len(lower_band) )]
          bollinger_bands_list[symbol] = bb_bands

      return bollinger_bands_list

#___________________________________________________________________________________________________

class stochastic_oscillator(bollinger_bands):

  def sma(self, array, window):

      weights =  np.ones(window) / window
      arr     =  np.convolve(array, weights, mode='valid')

      sma = np.empty(window + len(arr), dtype=arr.dtype)
      sma[:window] = np.nan * window
      sma[window:] = arr
      sma[np.isnan(sma)] = np.nanmean(sma)

      return sma

  def moving_min (self, array, period ):
      import numpy as np
      moving_min = np.empty_like(array)
      moving_min = np.full( moving_min.shape , np.nan)
      for i in range(period, len(array)+1 ):
            moving_min[i-1] = np.min(array[i-period:i]  )
      return moving_min

  def moving_max (self, array, period ):
        import numpy as np
        moving_max = np.empty_like(array)
        moving_max = np.full( moving_max.shape , np.nan)
        for i in range(period, len(array)+1 ):
              moving_max[i-1] = np.max(array[i-period:i]  )
        return moving_max

  def moving_end (self, array, period ):
        import numpy as np
        moving_end = np.empty_like(array)
        moving_end = np.full( moving_end.shape , np.nan)

        for i in range(period, len(array)+1 ):
              moving_end[i-1] = array[i-1:i]
        return moving_end


  def  stochastic_oscillator(self, high, low, close, period):

      # calculate %K line
      # low , high , close  = low.reshape(-1,1) , high.reshape(-1,1) , close.reshape(-1,1)

      lowest_low   = self.moving_min(low  , period )
      highest_high = self.moving_max(high , period )
      close_last =   self.moving_end(close, period )

      k_percent = 100 * ( (   close_last   - lowest_low) / (highest_high - lowest_low) )
      # calculate %D line
      d_percent = self.sma( k_percent  , 3)

      return  k_percent, d_percent


  def  stochastic_oscillator_lookback(self, bar_list, period = 10, lookback = 10):

      symbols = 0
      values  = 1
      stochastic_oscillator_list  =  [[]] * len(bar_list[values])
      for index, ohlc in enumerate(bar_list):

          high,  low,   close  =   ohlc['High'],  ohlc['Low'],  ohlc['Close']
          k_percent, d_percent = stochastic_oscillator( high, low, close, period)

          if lookback :
            k_percent , d_percent   =  k_percent[-lookback:],  d_percent[-lookback:]

          stochastic_oscillator = [ [ k_percent[i], d_percent[i]] for i in range( len(k_percent) )]
          stochastic_oscillator_list[symbol] = stochastic_oscillator

      return   stochastic_oscillator_list

#___________________________________________________________________________________________________

class access_indicators( stochastic_oscillator):

        def __init__(self):
            pass
