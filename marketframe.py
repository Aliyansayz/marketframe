import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import pytz


class get_clean_data:

    @classmethod
    def get_data_np_df(cls, symbols, interval=None, period=None, names=None):
        # symbols = ['BTC-USD' , 'ETH-USD' ]
        if interval == None and period == None:
            interval = '5m'
            period = '1d'

        data = [[0]] * len(symbols)

        for i, symbol in enumerate(symbols):
            bar = yf.download(tickers=f'{symbol}', interval=f'{interval}', period=f'{period}')
            data[i] = bar
        if names:
            symbol_name = [str(symbols[i]) + " " + str(names[i]) for i in range(len(symbols))]
            bar_list = [symbol_name, data]

        else:
            bar_list = [symbols, data]

        bar_list = cls.refined_df(bar_list)

        return bar_list

    @classmethod
    def refined_df(cls, bar_list):

        symbols = 0  # index 0 for symbols
        values = 1  # index 1 for ohlc

        for index, df in enumerate(bar_list[values]):
            df = df.drop('Adj Close', axis=1)
            df = df.drop('Volume', axis=1)
            # df = df.rename(columns={'Datetime': 'index'})
            df = df.fillna(df.mean())
            # resampled_df = df.resample(step).ohlc()
            # resampled_df = pd.DataFrame(resampled_data)
            np_df = df.to_records(index=True)

            column = []

            for name in np_df.dtype.names:
                if name == 'Datetime':
                    column.append('index')
                else:
                    column.append(name)

            np_df.dtype.names = tuple(column)
            try:
                np_df['index'] = np_df['index'].astype('datetime64[h]')
            except:
                pass
            # np_df['index']  =  cls.change_time( date_time_index= np_df['index'] , format= format)
            bar_list[values][index] = np_df

        return bar_list


""""
symbols = [ 'CHFJPY=X'  ]
# symbols = [ 'BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'SOL-USD', 'STETH-USD', 'ADA-USD', 'DOGE-USD', 'TRX-USD', 'LTC-USD' ]

bar_list = get_clean_data.get_data_np_df(symbols , interval = '1H' , period = '7d' )

resample = resample_data( data_list=bar_list , step=4 , rotate = True , format = 'pkt'  )

resample_list = resample.run_resample_data()
# = resample.chart_version( bar_list=bar_list, step=3, rotate = True, format = None )

resample_list

"""


class resample_data:

    def __init__(self, data_list, step=None, rotate=True, format=None):

        self.data_list = data_list
        self.step = step
        self.rotate = rotate
        self.format = str(format)

        # self.symbols = 0
        # self.values  = 1

    def run_resample_data(self):
        bar_list = self.chart_version(bar_list=self.data_list, step=self.step, rotate=self.rotate, format=self.format)

        return bar_list

    def chart_version(self, bar_list, step=3, rotate=True, format=None):

        symbols = 0  # index 0 for symbols
        values = 1  # index 1 for ohlc

        if rotate == True:

            if format == 'pkt':
                # Set the time zone to Pakistan Standard Time (Asia/Karachi)
                pakistan_time_zone = pytz.timezone('Asia/Karachi')
                # Get the current time in Pakistan
                current_time = datetime.now(pakistan_time_zone)

            else:
                current_time = datetime.now()

            version = int(current_time.strftime('%H')) % step

            for index, _ in enumerate(bar_list[values]):
                bar_list[values][index] = bar_list[values][index][version:]
        #   bar_list[values][index] as it is

        bar_list = self.aggregate_interval(bar_list=bar_list, step=step, format=self.format)
        return bar_list

    def aggregate_interval(self, bar_list, step=3, timezone=None, format=None):

        # step = 3
        symbols = 0  # index 0 for symbols
        values = 1  # index 1 for ohlc

        bar_list_resampled = [[]] * 2
        bar_list_resampled[symbols] = [[]] * len(bar_list[symbols])
        bar_list_resampled[values] = [[]] * len(bar_list[symbols])

        dt = np.dtype(
            [('index', 'datetime64[h]'), ('symbol', 'object'), ('Open', float), ('High', float), ('Low', float),
             ('Close', float)])

        for symbol, ohlc in enumerate(bar_list[values]):

            if format:
                date_index = self.change_time(np.datetime_as_string(ohlc['index'], unit='s'), format=format)

            else:
                date_index = np.array(ohlc['index'], dtype='datetime64[h]')

            if step > 1:
                resampled = date_index[::step]

            elif step == 1:
                resampled = date_index

            # date_objects = [np.datetime64(date_str) for date_str in resampled ]
            # resampled_dates =  np.array(date_objects, dtype='datetime64[h]')
            select_open = []
            select_high = []
            select_low = []
            select_close = []

            # step = 4 # i = 4 # 4 -4 # 5-4 # 8-4

            for i in range(0, len(bar_list[values][symbol]), step):  # logic re solved for 'step' to 'step-1'

                select_open.append(ohlc['Open'][i:i + step][0])
                select_high.append(max(ohlc['High'][i:i + step]))
                select_low.append(min(ohlc['Low'][i:i + step]))
                select_close.append(ohlc['Close'][i:i + step][-1])

            data = np.empty(len(resampled), dtype=dt)

            # return select_close
            # return resampled
            for i in range(len(resampled)):
                data[i] = (
                resampled[i], bar_list[symbols][symbol], select_open[i], select_high[i], select_low[i], select_close[i])

            bar_list_resampled[values][symbol] = data
            bar_list_resampled[symbols][symbol] = bar_list[symbols][symbol]

        return bar_list_resampled

    def change_time(self, date_time_index, format=None):

        def convert_to_local_time(datetime_str, timezone):
            utc_zone = pytz.timezone('UTC')
            timezone_zone = pytz.timezone(f'{timezone}')
            utc_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
            utc_datetime = utc_zone.localize(utc_datetime)
            local_datetime = utc_datetime.astimezone(timezone_zone)

            return local_datetime.strftime('%Y-%m-%dT%H:%M:%S')

        if format == 'pkt':
            timezone = 'Asia/Karachi'
        else:
            timezone = 'Asia/Karachi'
        vectorized_conversion = np.vectorize(convert_to_local_time, excluded=['timezone'])

        converted = vectorized_conversion(date_time_index, timezone=timezone)
        formatted_datetime = np.array(converted, dtype='datetime64[h]')

        return formatted_datetime


class indicator_store:

    def shift(self, array, place):

        array = np.array(array, dtype=np.float32)
        shifted = np.roll(array, place)
        shifted[0:place] = np.nan
        shifted[np.isnan(shifted)] = np.nanmean(shifted)

        return shifted

    def smoothed(self, array, period, alpha=None):

        ema = np.empty_like(array)
        ema = np.full(ema.shape, np.nan)
        ema[0] = np.mean(array[0], dtype=np.float64)
        if alpha == None:
            alpha = 1 / (period)

        for i in range(1, len(array)):
            ema[i] = array[i] * alpha + (ema[i - 1] * (1 - alpha))
        try:
            ema = np.nan_to_num(ema, nan=0)
        except:
            pass

        return ema

    # def ema (self, array, period ):

    #       ema = np.empty_like(array)
    #       ema = np.full( ema.shape  , np.nan)
    #       ema[0] = np.mean(array[0] , dtype=np.float64)
    #       alpha  = 2 / (period + 1)
    #       # Calculate the EMA for each window of 14 values
    #       for i in range(1 , len(array) ):
    #             ema[i] = np.array( (array[i] * alpha +  ema[i-1]  * (1-alpha) ) , dtype=np.float16 )
    #       try: ema =  np.nan_to_num(ema , nan=0)
    #       except: pass

    #       return ema

    def ema(self, price, period):

        price = np.array(price)
        alpha = 2 / (period + 1.0)
        alpha_reverse = 1 - alpha
        data_length = len(price)

        power_factors = alpha_reverse ** (np.arange(data_length + 1))
        initial_offset = price[0] * power_factors[1:]

        scale_factors = 1 / power_factors[:-1]

        weight_factor = alpha * alpha_reverse ** (data_length - 1)

        weighted_price_data = price * weight_factor * scale_factors
        cumulative_sums = weighted_price_data.cumsum()
        ema_values = initial_offset + cumulative_sums * scale_factors[::-1]

        return ema_values

    def sma(self, array, period):

        weights = np.ones(period) / period
        arr = np.convolve(array, weights, mode='valid')

        window = period - 1
        sma = np.empty(window + len(arr), dtype=arr.dtype)
        sma[:window] = np.nan * window
        sma[window:] = arr
        sma[np.isnan(sma)] = np.nanmean(arr[:period])

        return sma

    def moving_min(self, array, period):
        moving_min = np.empty_like(array)
        moving_min = np.full(moving_min.shape, np.nan)
        for i in range(period, len(array) + 1):
            moving_min[i - period] = np.min(array[i - period:i])
        try:
            moving_min = np.nan_to_num(moving_min, nan=0)
        except:
            pass
        # moving_min[np.isnan(moving_min)] = np.nanmean(moving_min)
        return moving_min

    def moving_max(self, array, period):
        moving_max = np.empty_like(array)
        moving_max = np.full(moving_max.shape, np.nan)
        # moving_max[:period] = np.max(array[:period])
        for i in range(period, len(array) + 1):
            moving_max[i - period] = np.max(array[i - period:i])
        try:
            moving_max = np.nan_to_num(moving_max, nan=0)
        except:
            pass
        # moving_max[np.isnan(moving_max)] = np.nanmean(moving_max)
        return moving_max

    def direction_crossover_signal_line(self, signal, signal_ema):

        signal_now = signal[-1]
        signal_ema_now = signal_ema[-1]

        prev_signal = signal[:-1]
        prev_signal_ema = signal_ema[:-1]

        direction = np.where(signal - signal_ema > 0, 1, -1)

        crossover = np.diff(direction, prepend=0)
        crossover = np.where(crossover < 0, -1, np.where(crossover > 0, 1, 0))

        return direction, crossover


# _____________________________________________________________________________

class ema_indicator(indicator_store):

    def __init__(self, data_list=None):

        self.data_list = data_list

    def run(self):

        if self.data_list:
            # constants
            symbols = 0  # index 0 for symbols
            values = 1  # index 1 for ohlc

            crossover_direction = [[0]] * len(self.data_list[symbols])

            # crossover_direction_list  = [  bar_list[symbols][name] , crossover_direction ]

            for symbol, ohlc in enumerate(self.data_list[values]):
                crossover, direction = self.crossover_and_direction(np.array(ohlc['Close'], ohlc['Open']))
                crossover_direction[symbol] = [crossover, direction]

            crossover_direction_list = [self.data_list[symbols], crossover_direction]
            return crossover_direction_list

    def crossover_and_direction_archived(self, array):

        short_ema = self.ema(array, 5)[-1]
        long_ema = self.ema(array, 20)[-1]

        # excluding last element from array
        # Caution using third last value for comparision instead second last

        # Experiment for forex pairs : if crossover difficult to detect and show 0 direction we can go with candle index open vs close price
        # if index or candle bullish then upward crossover
        # else if index or candle bearish then downward crossover

        prev_short_ema = self.ema(array[:-1], 5)[-1]
        prev_long_ema = self.ema(array[:-1], 20)[-1]

        crossover = direction = 0

        if prev_short_ema < prev_long_ema and short_ema > long_ema:

            crossover = direction = 1

        elif prev_short_ema > prev_long_ema and short_ema < long_ema:

            crossover = direction = -1

        else:
            if short_ema > long_ema:
                direction = 1

            elif short_ema < long_ema:
                direction = -1

        #  elif short_ema ==  long_ema  :
        #         direction =

        return crossover, direction

    # def crossover_direction_lookback(self, bar_list, lookback):

    #     return type(bar_list)  period
    def crossover_and_direction(self, array_close, array_open, ema_period=[5, 20]):
        # ema_period     =  [ 5 , 20 ]
        short_ema = self.ema(array_close, 5)[-1]
        long_ema = self.ema(array_close, 20)[-1]

        prev_short_ema = self.ema(array_close[:-1], ema_period[0])[-1]
        prev_long_ema = self.ema(array_close[:-1], ema_period[1])[-1]
        crossover, direction = 0, 0

        if prev_short_ema < prev_long_ema and short_ema > long_ema:
            crossover, direction = 1, 1

        elif prev_short_ema > prev_long_ema and short_ema < long_ema:
            crossover, direction = -1, -1

        else:
            if short_ema > long_ema:
                direction = 1

            elif short_ema < long_ema:
                direction = -1
            # this means :    long_ema = short_ema True
            elif array_close[-1] > array_open[-1]:
                crossover, direction = 1, 1
            elif array_open[-1] > array_close[-1]:
                crossover, direction = -1, -1

        return crossover, direction

    def ema_lookback(self, bar_list, lookback, ema_period=[5, 20]):

        symbols = 0
        values = 1

        emaz_list = [[0]] * len(bar_list[symbols])

        for symbol, ohlc in enumerate(bar_list[values]):

            emaz = [[0]] * lookback

            start_index = len(ohlc['Close']) - lookback
            for i in range((len(ohlc['Close']) - lookback), (len(ohlc['Close'])), 1):
                short_ema = self.ema(ohlc['Close'][:i], ema_period[0])[-1]
                long_ema = self.ema(ohlc['Close'][:i], ema_period[1])[-1]
                emaz[i - start_index] = [short_ema, long_ema]

            emaz_list[symbol] = emaz

        return emaz_list

    def crossover_direction_lookback(self, bar_list, ema_period=[5, 20], lookback=10):
        symbols = 0
        values = 1

        crossover_direction_list = [[0]] * len(bar_list[symbols])

        for symbol, ohlc in enumerate(bar_list[values]):

            crossover_direction = [[0]] * lookback

            start_index = len(ohlc['Close']) - lookback

            for i in range((len(ohlc['Close']) - lookback), (len(ohlc['Close'])), 1):
                crossover, direction = self.crossover_and_direction(ohlc['Close'][:i], ohlc['Open'][:i], ema_period)
                crossover_direction[i - start_index] = [crossover, direction]

            crossover_direction_list[symbol] = crossover_direction

        return crossover_direction_list


# ema_indicator.transform_data_list(bar_list, lookback, crossover_direction_list  )


# ___________________________________________________________________________________________________

class atr_bands_indicator(ema_indicator):

    def __init__(self, data_list=None):

        self.data_list = data_list
        # , period=8, multiplier= 2.0 , lookback = None

    def get_atr_bands(self, bar_list, period=5, multiplier=1.7):

        # constants
        symbols = 0  # index 0 for symbols
        values = 1  # index 1 for ohlc
        atr_bands = [[0]] * len(bar_list[symbols])

        for index, ohlc in enumerate(bar_list[values]):
            close = ohlc['Close']
            high = ohlc['High']
            low = ohlc['Low']

            lower_band, upper_band = self.atr_bands(close, high, low, multiplier, period)

            atr_bands[index] = [[lower_band[i], upper_band[i]] for i in range(len(lower_band))]

        atr_bands_list = [bar_list[symbols], atr_bands]

        return atr_bands_list

    def atr_bands(self, close, high, low, multiplier, period):

        # multiplier = 2.0 / 1.7
        close_shift = self.shift(close, 1)
        high_low, high_close, low_close = np.array(high - low, dtype=np.float32), \
                                          np.array(abs(high - close_shift), dtype=np.float32), \
                                          np.array(abs(low - close_shift), dtype=np.float32)

        true_range = np.max(np.hstack((high_low, high_close, low_close)).reshape(-1, 3), axis=1)
        # true_range[true_range == 0] = 0.0001

        # nan_indices = np.where(np.isnan(true_range))
        mean = np.nanmean(true_range)
        true_range[np.isnan(true_range)] = mean

        # true_range = self.missing_nan(true_range)
        avg_true_range = self.smoothed(true_range, period)

        price = close
        upper_band = price + (multiplier * avg_true_range)
        lower_band = price - (multiplier * avg_true_range)

        return lower_band, upper_band

    def atr_bands_lookback(self, bar_list, multiplier=1.7, period=5, lookback=10):

        values = 1
        symbols = 0
        atr_bands_list = [[0]] * len(bar_list[symbols])

        for symbol, ohlc in enumerate(bar_list[values]):
            close = ohlc['Close']
            high = ohlc['High']
            low = ohlc['Low']

            lower_band, upper_band = self.atr_bands(close, high, low, multiplier, period)

            lower_band = lower_band[-lookback:]
            upper_band = upper_band[-lookback:]

            atr_bands = [[lower_band[i], upper_band[i]] for i in range(lookback)]
            atr_bands_list[symbol] = atr_bands

        return atr_bands_list


# ___________________________________________________________________________________________________


import numpy as np


# atr_bands_indicator
# get_atr_bands


# adx = adx_indicator (data_list = bar_list  )
# adx = adx_indicator(bar_list)
# adx_value_list = adx.run_adx()
#

# ___________________________________________________________________________________________________
class adx_indicator(atr_bands_indicator):

    def __init__(self, data_list=None, period=14):

        self.data_list = data_list
        self.period = period

    def run_adx(self):

        adx_value_list = self.get_adx(self.data_list, self.period)

        return adx_value_list

    def get_adx(self, bar_list, period):

        symbols = 0
        values = 1
        adx_value = [[0]] * len(bar_list[symbols])

        for index, ohlc in enumerate(bar_list[values]):
            close = ohlc['Close']
            high = ohlc['High']
            low = ohlc['Low']
            adx = self.adx(close, high, low, period)

            adx_value[index] = adx

        adx_value_list = [bar_list[symbols], adx_value]

        return adx_value_list

    def adx(self, close, high, low, period=8):

        true_range = self.true_range(high, low, close)
        highs, lows = high - self.shift(high, 1), self.shift(low, 1) - low

        pdm = np.where(highs > lows, highs, 0.0)
        ndm = np.where(lows > highs, lows, 0.0)

        smoothed_atr = self.smoothed(true_range, period)

        pdi_value = self.smoothed(pdm, period) / smoothed_atr
        pdi = pdi_value * 100

        ndi_value = self.smoothed(ndm, period) / smoothed_atr
        ndi = ndi_value * 100

        dx = (abs(pdi - ndi)) / (abs(pdi + ndi)) * 100
        adx = self.smoothed(dx, period)

        return adx

    def true_range(self, high, low, close):

        close_shift = self.shift(close, 1)
        high_low, high_close, low_close = np.array(high - low, dtype=np.float32), \
                                          np.array(abs(high - close_shift), dtype=np.float32), \
                                          np.array(abs(low - close_shift), dtype=np.float32)

        true_range = np.max(np.hstack((high_low, high_close, low_close)).reshape(-1, 3), axis=1)

        return true_range

    def adx_lookback(self, bar_list, period=8, lookback=10):

        symbols = 0
        values = 1
        adx_values_list = [[0]] * len(bar_list[symbols])

        for symbol, ohlc in enumerate(bar_list[values]):
            close = ohlc['Close']
            high = ohlc['High']
            low = ohlc['Low']

            adx = self.adx(close, high, low, period)

            adx_values = adx[-lookback:]

            adx_values_list[symbol] = adx_values

        return adx_values_list


# ___________________________________________________________________________________________________

class heikin_ashi(adx_indicator):

    def __init__(self, refine_list=None):

        self.refine_list = refine_list

    def run_heikin_ashi(self, refine_list):

        ha_status_list = self.get_heikin_ashi(bar_list)

        return ha_status_list

    def heikin_ashi_status(self, ha_open, ha_close):

        candles = np.full_like(ha_close, '', dtype='U10')

        for i in range(1, len(ha_close)):

            # green_condition =  ha_close[i] > ha_open[i]
            # red_condition   =  ha_close[i] < ha_open[i]
            if ha_close[i] > ha_open[i]:
                candles[i] = 'Green'

            elif ha_close[i] < ha_open[i]:
                candles[i] = 'Red'

            else:
                candles[i] = 'Neutral'

        return candles

    def heikin_ashi_candles(self, open, high, low, close):

        ha_low, ha_close = np.empty(len(close), dtype=np.float32), np.empty(len(close), dtype=np.float32)
        ha_open, ha_high = np.empty(len(close), dtype=np.float32), np.empty(len(close), dtype=np.float32)

        ha_open[0] = (open[0] + close[0]) / 2
        ha_close[0] = (close[0] + open[0] + high[0] + low[0]) / 4

        for i in range(1, len(close)):
            ha_open[i] = (ha_open[i - 1] + ha_close[i - 1]) / 2
            ha_close[i] = (open[i] + high[i] + low[i] + close[i]) / 4
            ha_high[i] = max(high[i], ha_open[i], ha_close[i])
            ha_low[i] = min(low[i], ha_open[i], ha_close[i])

        return ha_open, ha_close, ha_high, ha_low

    def get_heikin_ashi(self, bar_list, lookback=None, ohlc_data=None):

        symbols = 0
        values = 1
        ha_status_list = [[]] * len(bar_list[symbols])
        ha_ohlc_list = [[]] * len(bar_list[values])
        # np.empty(len(bar_list[symbols]), dtype='U10')

        for symbol, ohlc in enumerate(bar_list[values]):

            open, high, low, close = ohlc['Open'], ohlc['High'], ohlc['Low'], ohlc['Close']

            ha_open, ha_close, ha_high, ha_low = self.heikin_ashi_candles(open, high, low, close)
            candles = self.heikin_ashi_status(ha_open, ha_close)

            if lookback:
                candles = candles[-lookback:]
                ha_open, ha_close, ha_high, ha_low = ha_open[-lookback:], ha_close[-lookback:], ha_high[
                                                                                                -lookback:], ha_low[
                                                                                                             -lookback:]
                # ha_open_close  = [ ha_open[-lookback:] , ha_close[-lookback:] ]

            ha_ohlc_list[symbol] = [ha_open, ha_high, ha_low, ha_close]
            ha_status_list[symbol] = candles

        if ohlc_data == True:
            return ha_ohlc_list

        return ha_status_list

    def normal_to_ha(self, data_list, ha_ohlc_list):

        symbols = 0  # index 0 for symbols
        values = 1  # index 1 for ohlc

        for sym, ohlc in enumerate(data_list[values]):
            ha_open, ha_close = [element for element in ha_ohlc_list[sym][0]], [element for element in
                                                                                ha_ohlc_list[sym][3]]
            ha_high, ha_low = [element for element in ha_ohlc_list[sym][1]], [element for element in
                                                                              ha_ohlc_list[sym][2]]

            ohlc['Close'], ohlc['Open'] = ha_close, ha_open
            ohlc['High'], ohlc['Low'] = ha_high, ha_low
            # lower_band,  upper_band   = atr_bands( close, high, low, multiplier, period  )
        return data_list


# ___________________________________________________________________________________________________

class bollinger_bands(heikin_ashi):

    def __init__(self, refine_list=None):

        self.refine_list = refine_list

    def sma(self, array, period):

        weights = np.ones(period) / period
        arr = np.convolve(array, weights, mode='valid')

        window = period - 1
        sma = np.empty(window + len(arr), dtype=arr.dtype)
        sma[:window] = np.nan * window
        sma[window:] = arr
        sma[np.isnan(sma)] = np.nanmean(arr[:period])

        return sma

    def std_dev(self, array, period):

        # Calculate the squared deviations from the mean
        squared_deviations = (array - self.sma(array, period)) ** 2

        # Calculate the average squared deviations
        average_squared_deviations = self.sma(squared_deviations, period)

        # Calculate the rolling standard deviation
        std_dev = np.sqrt(average_squared_deviations)

        return std_dev

    def run_bollinger_bands(self, refine_list):

        bollinger_bands_list = self.get_bollinger_bands(bar_list=refine_list)
        return bollinger_bands_list

    def bollinger_bands(self, high, low, close, period=20, mult=2.0):

        # bollinger_bands
        typical_price = (high + low + close) / 3
        typical_price_ma = self.sma(typical_price, period)
        std_dev = self.std_dev(typical_price, period)

        upper_band = typical_price_ma + (mult * std_dev)
        lower_band = typical_price_ma - (mult * std_dev)

        return lower_band, upper_band

    def get_bollinger_bands(self, bar_list, lookback=None):

        symbols = 0
        values = 1
        bollinger_bands_list = [[]] * len(bar_list[values])
        # np.empty(len(bar_list[symbols]), dtype='U10')

        for symbol, ohlc in enumerate(bar_list[values]):

            high, low, close = ohlc['High'], ohlc['Low'], ohlc['Close']
            lower_band, upper_band = self.bollinger_bands(high, low, close)

            if lookback:
                lower_band, upper_band = lower_band[-lookback:], upper_band[-lookback:]

            bb_bands = [[lower_band[i], upper_band[i]] for i in range(len(lower_band))]
            bollinger_bands_list[symbol] = bb_bands

        return bollinger_bands_list


class stochastic_oscillator(bollinger_bands):

    def stochastic_oscillator(self, high, low, close, period):

        # calculate %K line
        # low , high , close  = low.reshape(-1,1) , high.reshape(-1,1) , close.reshape(-1,1)

        lowest_low = self.moving_min(low, period)
        highest_high = self.moving_max(high, period)

        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        # calculate %D line
        d_percent = self.sma(k_percent, 3)

        return k_percent, d_percent

    def stochastic_oscillator_lookback(self, bar_list, period=10, lookback=10):

        symbols, values = 0, 1
        stochastic_oscillator_list = [[]] * len(bar_list[values])
        for index, ohlc in enumerate(bar_list[values]):

            high, low, close = ohlc['High'], ohlc['Low'], ohlc['Close']
            k_percent, d_percent = self.stochastic_oscillator(high, low, close, period)

            if lookback:
                k_percent, d_percent = k_percent[-lookback:], d_percent[-lookback:]

            stochastic_oscillator = [[k_percent[i], d_percent[i]] for i in range(len(k_percent))]
            stochastic_oscillator_list[index] = stochastic_oscillator

        return stochastic_oscillator_list


class stochastic_momentum_index(stochastic_oscillator):

    def stochastic_momentum_index(self, high, low, close, period=20, ema_period=5):

        lengthD = ema_period
        lowest_low = self.moving_min(low, period)
        highest_high = self.moving_max(high, period)
        relative_range = close - ((highest_high + lowest_low) / 2)
        highest_lowest_range = highest_high - lowest_low

        relative_range_smoothed = self.smoothed(self.smoothed(relative_range, ema_period), ema_period)
        highest_lowest_range_smoothed = self.smoothed(self.smoothed(highest_lowest_range, ema_period), ema_period)

        smi = [(relative_range_smoothed[i] / (highest_lowest_range_smoothed[i] / 2)) * 100 if
               highest_lowest_range_smoothed[i] != 0 else 0.0
               for i in range(len(relative_range_smoothed))]

        # relative_range = (lowest_low - highest_high) / highest_lowest_range
        # calculate smi with  %D length

        smi_ema = self.ema(smi, ema_period)

        return smi, smi_ema

    def stochastic_momentum_lookback(self, bar_list, period=20, lookback=10, ema_period=5, crossover_direction=False):

        symbols, values = 0, 1

        stochastic_momentum_list = [[]] * len(bar_list[values])
        smi_direction_crossover_list = [[]] * len(bar_list[values])
        crossover_direction = [[]] * lookback

        for index, ohlc in enumerate(bar_list[values]):

            open, high, low, close = ohlc['Open'], ohlc['High'], ohlc['Low'], ohlc['Close']
            smi, smi_ema = self.stochastic_momentum_index(high, low, close, period, ema_period)

            if lookback:
                smi, smi_ema = smi[-lookback:], smi_ema[-lookback:]

            direction, crossover = self.direction_crossover_signal_line(smi, smi_ema)

            stochastic_momentum = [[smi[i], smi_ema[i]] for i in range(len(smi))]
            stochastic_momentum_list[index] = stochastic_momentum
            # stochastic_momentum_direction_crossover = [ [ direction_smi[i], crossover_smi[i]] for i in range( len(direction_smi) )]
            crossover_direction = [[direction[i], crossover[i]] for i in range(len(smi))]
            smi_direction_crossover_list[index] = crossover_direction

        if crossover_direction:
            return smi_direction_crossover_list

        else:
            return stochastic_momentum_list


class access_indicators(stochastic_momentum_index):

    def __init__(self):
        pass


"""
bar_df = indicators_lookback_mode.transform_data_list( refine_list = refined_list, multiplier= 1.7 , atr_period = 5,  adx_period = 8 ,   lookback = 1  , ha_ohlc = True)
print(bar_df)

"""


class indicators_lookback_mode(access_indicators):

    @classmethod
    def transform_data_list(cls, refine_list, multiplier=1.7, atr_period=5, adx_period=8, lookback=10,
                            ema_period=[5, 20], ha_ohlc=True):

        symbols = 0
        values = 1
        indicator = cls()  # universal class of project => adx_indicator

        heikin_ashi = indicator.get_heikin_ashi(bar_list=refine_list, ohlc_data=True)

        # crossover_direction_list  =  adx_atr_bands_indicator.crossover_direction_lookback(bar_list = refine_list, lookback = lookback )
        ha_status_list = indicator.get_heikin_ashi(refine_list, lookback=lookback)
        if ha_ohlc:
            refine_list = indicator.normal_to_ha(data_list=refine_list, ha_ohlc_list=heikin_ashi)

        ha_ohlc_list = indicator.get_heikin_ashi(bar_list=refine_list, lookback=lookback, ohlc_data=True)

        crossover_direction_list = indicator.crossover_direction_lookback(bar_list=refine_list, ema_period=ema_period,
                                                                          lookback=lookback)

        stochastic_momentum_list = indicator.stochastic_momentum_lookback(bar_list=refine_list, period=ema_period[1],
                                                                          lookback=lookback, ema_period=5)

        stochastic_momentum_crossover_list = indicator.stochastic_momentum_lookback(bar_list=refine_list,
                                                                                    period=ema_period[1],
                                                                                    lookback=lookback, ema_period=5,
                                                                                    crossover_direction=True)
        emaz_list = indicator.ema_lookback(bar_list=refine_list, lookback=lookback, ema_period=ema_period)

        atr_bands_list = indicator.atr_bands_lookback(refine_list, multiplier, period=atr_period, lookback=lookback)
        adx_value_list = indicator.adx_lookback(bar_list=refine_list, period=adx_period, lookback=lookback)

        bollinger_bands_list = indicator.get_bollinger_bands(bar_list=refine_list, lookback=lookback)

        # lookback = 10
        dt = np.dtype([('index', 'datetime64[h]'), ('symbol', 'U20'), ('Open', float), ('High', float), ('Low', float),
                       ('Close', float), ('Heikin-Ashi-Status', 'U10'), ('Direction', float),
                       ('Average-Directional-Index', float), ('Crossover', float), \
                       ('Stop_Loss', float), ('Take_Profit', float), ('direction_smi', float), ('crossover_smi', float),
                       ('ema_low', float), ('ema_high', float), ('smi', float), ('smi_ema', float), ('bb_lower', float),
                       ('bb_upper', float), ('atr_lower', float), ('atr_upper', float), ('ha_open', float),
                       ('ha_high', float), ('ha_low', float), ('ha_close', float)])

        column_names = dt.names
        data = [[0]] * len(refine_list[symbols])

        for sym, ohlc in enumerate(refine_list[values]):

            index = ohlc['index'][-lookback:]
            symbol = ohlc['symbol'][-lookback:]
            open = ohlc['Open'][-lookback:]
            high = ohlc['High'][-lookback:]
            low = ohlc['Low'][-lookback:]
            close = ohlc['Close'][-lookback:]

            heikin_ashi_status = [element for element in ha_status_list[sym]]

            # fractal_status  = [ element  for  element in ha_ohlc_list[sym]  ]
            ha_open, ha_close = [element for element in ha_ohlc_list[sym][0]], [element for element in
                                                                                ha_ohlc_list[sym][3]]
            ha_high, ha_low = [element for element in ha_ohlc_list[sym][1]], [element for element in
                                                                              ha_ohlc_list[sym][2]]

            smi = [element[0] for element in stochastic_momentum_list[sym]]
            smi_ema = [element[1] for element in stochastic_momentum_list[sym]]

            direction_smi = [element[0] for element in stochastic_momentum_crossover_list[sym]]
            crossover_smi = [element[1] for element in stochastic_momentum_crossover_list[sym]]

            adx_value = [element for element in adx_value_list[sym]]
            lower_band = [element[0] for element in atr_bands_list[sym]]
            upper_band = [element[1] for element in atr_bands_list[sym]]

            bb_lower = [element[0] for element in bollinger_bands_list[sym]]
            bb_upper = [element[1] for element in bollinger_bands_list[sym]]
            bb_bands = [bb_lower, bb_upper]
            # crossover =   crossover_direction_list[index][dynamic--for next values of crossover of date time index][0-->static for crossover]
            crossover = [element[0] for element in crossover_direction_list[sym]]
            direction = [element[1] for element in crossover_direction_list[sym]]

            short_ema = [element[0] for element in emaz_list[sym]]
            long_ema = [element[1] for element in emaz_list[sym]]
            # ha_ohlc_list[symbol]   =  [ha_open, ha_high, ha_low, ha_close]
            ha_ohlc = [element for element in ha_ohlc_list[sym]]

            ohlc_df = np.empty(len(close), dtype=dt)

            for i in range(0, len(ohlc_df)):

                stop_loss = 0
                take_profit = 0
                if crossover[i] == 1 or direction[i] == 1:
                    stop_loss = lower_band[i]
                    take_profit = upper_band[i]

                elif crossover[i] == -1 or direction[i] == -1:
                    stop_loss = upper_band[i]
                    take_profit = lower_band[i]

                ohlc_df[i] = (
                index[i], symbol[i], open[i], high[i], low[i], close[i], heikin_ashi_status[i], direction[i],
                adx_value[i], \
                crossover[i], stop_loss, take_profit, direction_smi[i], crossover_smi[i], short_ema[i], long_ema[i],
                smi[i], smi_ema[i], bb_lower[i], bb_upper[i], lower_band[i], upper_band[i], ha_open[i], ha_high[i],
                ha_low[i], ha_close[i])
            #

            data[sym] = ohlc_df

        return [column_names, data]


class sorting:
    # define numpy structured array structure
    columns, values = 0, 1

    @classmethod
    def get_signal_data(cls, matches, order_type):

        symbol = matches['symbol'][-1]

        if order_type == 1:
            order = 'buy'
            stop_loss = round(matches['atr_lower'][-1], 5)
            take_profit = round(matches['atr_upper'][-1], 5)

        elif order_type == -1:
            order = 'sell'
            stop_loss = round(matches['atr_upper'][-1], 5)
            take_profit = round(matches['atr_lower'][-1], 5)

        time = matches['index'][-1]
        return symbol, order, take_profit, stop_loss, time

    @classmethod
    def get_signal_data_direction(cls, matches, order_type):

        symbol = matches['symbol'][-1]

        if order_type == 1:
            order = 'buy'
            stop_loss = round(matches['atr_lower'][-1], 5)
            take_profit = round(matches['atr_upper'][-1], 5)

        elif order_type == -1:
            order = 'sell'
            stop_loss = round(matches['atr_upper'][-1], 5)
            take_profit = round(matches['atr_lower'][-1], 5)

        time = matches['index'][-1]
        return symbol, order, take_profit, stop_loss, time

    @classmethod
    def get_signal_data_crossover(cls, matches, order_type):

        symbol = matches['symbol'][-1]

        if order_type == 1:
            order = 'buy'
            stop_loss = round(matches['atr_lower'][-1], 5)
            take_profit = round(matches['atr_upper'][-1], 5)

        elif order_type == -1:
            order = 'sell'
            stop_loss = round(matches['atr_upper'][-1], 5)
            take_profit = round(matches['atr_lower'][-1], 5)

        time = matches['index'][-1]
        return symbol, order, take_profit, stop_loss, time

    @classmethod
    def sort_uptrend_breakout(cls, bar_df, last_candles=10, chart_type=None):

        sort_index, signal_list = [], []
        for index, ohlc in enumerate(bar_df[sorting.values]):

            observe = ohlc[-last_candles:]

            volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] < 25)

            uptrend_bb_band = observe[
                (observe['High'] > observe['bb_upper']) | (observe['Close'] > observe['bb_upper'])]
            uptrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Green'

            # return  [ len(volatile_adx) , len(uptrend_bb_band) ,  ] , len(uptrend_heikin_ashi)

            find = volatile_adx and uptrend_bb_band and uptrend_heikin_ashi

            matches = observe[find]
            if len(matches) > 0:
                sort_index.append(index)
                symbol, order, stop_loss, take_profit, time = cls.get_signal_data(matches, order_type=1)
                signal = [symbol, order, stop_loss, take_profit, time, chart_type]
                signal_list.append(signal)

        sorted_data = [bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index]

        return sorted_data, signal_list

    @classmethod
    def sort_downtrend_breakout(cls, bar_df, last_candles=10, chart_type=None):

        sort_index, signal_list = [], []

        for index, ohlc in enumerate(bar_df[sorting.values]):

            observe = ohlc[-last_candles:]

            volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] < 25)
            downtrend_bb_band = (observe['Low'] < observe['bb_lower']) | (observe['Close'] < observe['bb_lower'])
            downtrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Red'

            find = volatile_adx and downtrend_bb_band and downtrend_heikin_ashi
            matches = observe[find]
            if len(matches) > 0:
                sort_index.append(index)
                symbol, order, stop_loss, take_profit, time = cls.get_signal_data(matches, order_type=-1)
                signal = [symbol, order, stop_loss, take_profit, time, chart_type]
                signal_list.append(signal)

        sorted_data = [bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index]

        return sorted_data, signal_list

    @classmethod
    def adx_stochastic_momentum_crossover(cls, bar_df, last_candles=10, cross_only=False, chart_type=None):
        strategy = "stochastic_momentum_crossover"
        sort_index, sell_signal_list, buy_signal_list = [], [], []
        for index, ohlc in enumerate(bar_df[sorting.values]):

            observe = ohlc[-last_candles:]
            # crossover_smi
            volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] < 25)
            mask_downtrend_crossover = observe['crossover_smi'] == -1.0
            downtrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Red'

            mask_uptrend_crossover = observe['crossover_smi'] == 1.0
            uptrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Green'

            if cross_only:
                find_s, find_b = mask_downtrend_crossover, mask_uptrend_crossover
            else:
                find_s, find_b = volatile_adx & mask_downtrend_crossover & downtrend_heikin_ashi, volatile_adx & mask_uptrend_crossover & uptrend_heikin_ashi
            matches_s = observe[find_s]
            matches_b = observe[find_b]

            if len(matches_s) > 0 and len(matches_b) > 0:
                matches_s, matches_b = cls.clean_duplicate(find_s, find_b, observe)

            if len(matches_s) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data(matches_s, order_type=-1)
                sell_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                sell_signal_list.append(sell_signal)

            if len(matches_b) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data(matches_b, order_type=1)
                buy_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                buy_signal_list.append(buy_signal)

        sorted_data = [bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index]

        return sorted_data, sell_signal_list, buy_signal_list

    @classmethod
    def adx_stochastic_momentum_direction(cls, bar_df, last_candles=10, cross_only=False, chart_type=None):
        strategy = "stochastic_momentum_direction"
        sort_index, sell_signal_list, buy_signal_list = [], [], []
        for index, ohlc in enumerate(bar_df[sorting.values]):

            observe = ohlc[-last_candles:]
            # crossover_smi
            volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] < 25)
            mask_downtrend_crossover = observe['direction_smi'] == -1.0
            downtrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Red'

            mask_uptrend_crossover = observe['direction_smi'] == 1.0
            uptrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Green'

            if cross_only:
                find_s, find_b = mask_downtrend_crossover, mask_uptrend_crossover
            else:
                find_s, find_b = volatile_adx & mask_downtrend_crossover & downtrend_heikin_ashi, volatile_adx & mask_uptrend_crossover & uptrend_heikin_ashi
            matches_s = observe[find_s]
            matches_b = observe[find_b]

            if len(matches_s) > 0 and len(matches_b) > 0:
                matches_s, matches_b = cls.clean_duplicate(find_s, find_b, observe)

            if len(matches_s) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data(matches_s, order_type=-1)
                sell_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                sell_signal_list.append(sell_signal)

            if len(matches_b) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data(matches_b, order_type=1)
                buy_signal = [symbol, order, take_profit, stop_loss, time, strategy, chart_type]
                buy_signal_list.append(buy_signal)

        sorted_data = [bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index]

        return sorted_data, sell_signal_list, buy_signal_list

    @classmethod
    def adx_crossover_ema(cls, bar_df, last_candles=10, cross_only=True, chart_type=None):
        strategy = "ema_crossover"
        sort_index, sell_signal_list, buy_signal_list = [], [], []
        for index, ohlc in enumerate(bar_df[sorting.values]):

            observe = ohlc[-last_candles:]

            volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] < 25)
            mask_downtrend_crossover = observe['Crossover'] == -1.0
            downtrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Red'

            mask_uptrend_crossover = observe['Crossover'] == 1.0
            uptrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Green'

            if cross_only:
                find_s, find_b = mask_downtrend_crossover, mask_uptrend_crossover
            else:
                find_s, find_b = volatile_adx & mask_downtrend_crossover & downtrend_heikin_ashi, volatile_adx & mask_uptrend_crossover & uptrend_heikin_ashi
            matches_s = observe[find_s]
            matches_b = observe[find_b]
            if len(matches_s) > 0 and len(matches_b) > 0:
                matches_s, matches_b = cls.clean_duplicate(find_s, find_b, observe)

            if len(matches_s) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data_crossover(matches_s, order_type=-1)
                sell_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                sell_signal_list.append(sell_signal)

            if len(matches_b) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data_crossover(matches_b, order_type=1)
                buy_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                buy_signal_list.append(buy_signal)

        sorted_data = [bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index]

        return sorted_data, sell_signal_list, buy_signal_list

    @classmethod
    def adx_direction_ema(cls, bar_df, last_candles=10, cross_only=False, chart_type=None):
        strategy = "ema_direction"
        sort_index, sell_signal_list, buy_signal_list = [], [], []
        for index, ohlc in enumerate(bar_df[sorting.values]):

            observe = ohlc[-last_candles:]

            volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] < 25)
            mask_downtrend_crossover = observe['Direction'] == -1.0
            downtrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Red'

            mask_uptrend_crossover = observe['Direction'] == 1.0
            uptrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Green'

            if cross_only:
                find_s, find_b = mask_downtrend_crossover, mask_uptrend_crossover
            else:
                find_s, find_b = volatile_adx & mask_downtrend_crossover & downtrend_heikin_ashi, volatile_adx & mask_uptrend_crossover & uptrend_heikin_ashi
            matches_s = observe[find_s]
            matches_b = observe[find_b]
            if len(matches_s) > 0 and len(matches_b) > 0:
                matches_s, matches_b = cls.clean_duplicate(find_s, find_b, observe)

            if len(matches_s) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data_crossover(matches_s, order_type=-1)
                sell_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                sell_signal_list.append(sell_signal)

            if len(matches_b) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data_crossover(matches_b, order_type=1)
                buy_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                buy_signal_list.append(buy_signal)

        sorted_data = [bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index]

        return sorted_data, sell_signal_list, buy_signal_list



    @classmethod
    def clean_duplicate(cls, find_s, find_b, observe):

        up_index = np.where(find_b)[0]
        down_index = np.where(find_s)[0]

        if up_index[-1] > down_index[-1]:
            matches_s, matches_b = [], observe[find_b]
        elif up_index[-1] < down_index[-1]:
            matches_s, matches_b = observe[find_s], []

        return matches_s, matches_b

    @classmethod
    def sort_trend_change_early_exit(cls, bar_df, last_candles=10):

        sort_index, signal_list, comments = [], [], []
        for index, ohlc in enumerate(bar_df[sorting.values]):

            observe = ohlc[-last_candles:]

            # Filter based on Average Directional Index (ADX)
            volatile_adx = observe['Average-Directional-Index'] > 20

            mask_downtrend_crossover = observe['Crossover'] == -1
            mask_uptrend_crossover = observe['Crossover'] == 1
            down = np.where(mask_downtrend_crossover)
            up = np.where(mask_uptrend_crossover)
            # np.where

            # Combine filters using logical AND
            matches = observe[volatile_adx & mask_downtrend_crossover]
            symbol = observe['symbol'][0]

            if len(up) > 1 or len(down) > 1:
                sort_index.append(index)

                if up[0] < down[0]:
                    comments.append(
                        f" Uptrend came at {observe['index'][up[0]]} but downward-crossover changed situation")
                else:
                    comments.append(
                        f" Downtrend came at {observe['index'][down[0]]} but upward-crossover changed situation")

                if up[0] != up[-1] or down[0] != down[-1]:

                    comments.append(f" Use Higher TimeFrame With 200 EMA/50 and ADX 20 period")

                    if up[-1] < down[-1]:  comments.append(f" Downtrend came at {observe['index'][down[-1]]} situation changed may close buy\
                                                          trades after seeing chart, adx status and heikin ashi candles")

                    if up[-1] > down[-1]:  comments.append(f" Uptrend came at {observe['index'][up[-1]]} situation changed may close sell\
                                                          trades after seeing chart, adx status and heikin ashi candles")
                    signal = [symbol, comments]
                    signal_list.append(signal)


            elif len(up) == 1 and len(down) != 0:
                sort_index.append(index)
                comments.append(f" One up-crossover  Use Higher TimeFrame With 200 EMA/50 and ADX 20 period")

                if up[0] < down[0]:
                    comments.append(
                        f" Uptrend came at {observe['index'][up[0]]} but downward-crossover changed situation")
                else:
                    comments.append(
                        f" Downtrend came at {observe['index'][down[0]]} but upward-crossover changed situation")

                if up[0] != up[-1] or down[0] != down[-1]:
                    comments.append(f" Use Higher TimeFrame With 200 EMA/50 and ADX 20 period")

                    if up[-1] < down[-1]:  comments.append(f" Downtrend came at {observe['index'][down[-1]]} situation changed may close buy\
                                                            trades after seeing chart, adx status and heikin ashi candles")
                    if up[-1] > down[-1]:  comments.append(f" Uptrend came at {observe['index'][up[-1]]} situation changed may close sell\
                                                            trades after seeing chart, adx status and heikin ashi candles")
                signal = [symbol, comments]
                signal_list.append(signal)


            elif len(down) == 1 and len(up) != 0:
                sort_index.append(index)
                comments.append(
                    f" One down-crossover and tried   Use Higher TimeFrame With 200 EMA/50 and ADX 20 period")

                if up[0] < down[0]:
                    comments.append(
                        f" Uptrend came at {observe['index'][up[0]]} but downward-crossover changed situation")
                else:
                    comments.append(
                        f" Downtrend came at {observe['index'][down[0]]} but upward-crossover changed situation")

                if up[0] != up[-1] or down[0] != down[-1]: comments.append(
                    f" Use Higher TimeFrame With 200 EMA/50 and ADX 20 period")

                if up[-1] < down[-1]:  comments.append(f" Downtrend came at {observe['index'][down[-1]]} situation changed may close buy\
                                                         trades after seeing chart, adx status and heikin ashi candles")
                if up[-1] > down[-1]:  comments.append(f" Uptrend came at {observe['index'][up[-1]]} situation changed may close sell\
                                                         trades after seeing chart, adx status and heikin ashi candles")
                signal = [symbol, comments]
                signal_list.append(signal)

            else:
                continue
        sorted_data = [bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index]

        return sorted_data, signal_list



class sorting_indices_crypto(sorting):

    @classmethod
    def adx_direction_ema(cls, bar_df, last_candles=10, cross_only=False, chart_type=None):
        strategy = "ema_direction"
        sort_index, sell_signal_list, buy_signal_list = [], [], []
        for index, ohlc in enumerate(bar_df[sorting.values]):

            observe = ohlc[-last_candles:]
            volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] <= 33)
            mask_downtrend_crossover = observe['Direction'] == -1.0
            downtrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Red'

            mask_uptrend_crossover = observe['Direction'] == 1.0
            uptrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Green'

            if cross_only:
                find_s, find_b = mask_downtrend_crossover, mask_uptrend_crossover
            else:
                find_s, find_b = volatile_adx & mask_downtrend_crossover & downtrend_heikin_ashi, volatile_adx & mask_uptrend_crossover & uptrend_heikin_ashi
            matches_s = observe[find_s]
            matches_b = observe[find_b]
            if len(matches_s) > 0 and len(matches_b) > 0:
                matches_s, matches_b = cls.clean_duplicate(find_s, find_b, observe)

            if len(matches_s) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data_crossover(matches_s, order_type=-1)
                sell_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                sell_signal_list.append(sell_signal)

            if len(matches_b) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data_crossover(matches_b, order_type=1)
                buy_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                buy_signal_list.append(buy_signal)

        sorted_data = [bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index]

        return sorted_data, sell_signal_list, buy_signal_list

    @classmethod
    def adx_crossover_ema(cls, bar_df, last_candles=10, cross_only=False, chart_type=None):
        strategy = "ema_direction"
        sort_index, sell_signal_list, buy_signal_list = [], [], []
        for index, ohlc in enumerate(bar_df[sorting.values]):

            observe = ohlc[-last_candles:]
            volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] <= 33)
            mask_downtrend_crossover = observe['Crossover'] == -1.0
            downtrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Red'

            mask_uptrend_crossover = observe['Crossover'] == 1.0
            uptrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Green'

            if cross_only:
                find_s, find_b = mask_downtrend_crossover, mask_uptrend_crossover
            else:
                find_s, find_b = volatile_adx & mask_downtrend_crossover & downtrend_heikin_ashi, volatile_adx & mask_uptrend_crossover & uptrend_heikin_ashi
            matches_s = observe[find_s]
            matches_b = observe[find_b]
            if len(matches_s) > 0 and len(matches_b) > 0:
                matches_s, matches_b = cls.clean_duplicate(find_s, find_b, observe)

            if len(matches_s) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data_crossover(matches_s, order_type=-1)
                sell_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                sell_signal_list.append(sell_signal)

            if len(matches_b) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data_crossover(matches_b, order_type=1)
                buy_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                buy_signal_list.append(buy_signal)

        sorted_data = [bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index]

        return sorted_data, sell_signal_list, buy_signal_list

    @classmethod
    def adx_stochastic_momentum_direction(cls, bar_df, last_candles=10, cross_only=False, chart_type=None):
        strategy = "stochastic_momentum_direction"
        sort_index, sell_signal_list, buy_signal_list = [], [], []
        for index, ohlc in enumerate(bar_df[sorting.values]):

            observe = ohlc[-last_candles:]
            # crossover_smi
            volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] <= 33)
            mask_downtrend_crossover = observe['direction_smi'] == -1.0
            downtrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Red'

            mask_uptrend_crossover = observe['direction_smi'] == 1.0
            uptrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Green'

            if cross_only:
                find_s, find_b = mask_downtrend_crossover, mask_uptrend_crossover
            else:
                find_s, find_b = volatile_adx & mask_downtrend_crossover & downtrend_heikin_ashi, volatile_adx & mask_uptrend_crossover & uptrend_heikin_ashi
            matches_s = observe[find_s]
            matches_b = observe[find_b]

            if len(matches_s) > 0 and len(matches_b) > 0:
                matches_s, matches_b = cls.clean_duplicate(find_s, find_b, observe)

            if len(matches_s) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data(matches_s, order_type=-1)
                sell_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                sell_signal_list.append(sell_signal)

            if len(matches_b) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data(matches_b, order_type=1)
                buy_signal = [symbol, order, take_profit, stop_loss, time, strategy, chart_type]
                buy_signal_list.append(buy_signal)

        sorted_data = [bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index]

        return sorted_data, sell_signal_list, buy_signal_list

    @classmethod
    def adx_stochastic_momentum_crossover(cls, bar_df, last_candles=10, cross_only=False, chart_type=None):
        strategy = "stochastic_momentum_crossover"
        sort_index, sell_signal_list, buy_signal_list = [], [], []
        for index, ohlc in enumerate(bar_df[sorting.values]):

            observe = ohlc[-last_candles:]
            # crossover_smi
            volatile_adx = (observe['Average-Directional-Index'] > 18) & (observe['Average-Directional-Index'] <= 33)
            mask_downtrend_crossover = observe['crossover_smi'] == -1.0
            downtrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Red'

            mask_uptrend_crossover = observe['crossover_smi'] == 1.0
            uptrend_heikin_ashi = observe['Heikin-Ashi-Status'] == 'Green'

            if cross_only:
                find_s, find_b = mask_downtrend_crossover, mask_uptrend_crossover
            else:
                find_s, find_b = volatile_adx & mask_downtrend_crossover & downtrend_heikin_ashi, volatile_adx & mask_uptrend_crossover & uptrend_heikin_ashi
            matches_s = observe[find_s]
            matches_b = observe[find_b]

            if len(matches_s) > 0 and len(matches_b) > 0:
                matches_s, matches_b = cls.clean_duplicate(find_s, find_b, observe)

            if len(matches_s) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data(matches_s, order_type=-1)
                sell_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                sell_signal_list.append(sell_signal)

            if len(matches_b) > 0:
                sort_index.append(index)
                symbol, order, take_profit, stop_loss, time = cls.get_signal_data(matches_b, order_type=1)
                buy_signal = [symbol, order, take_profit, stop_loss, strategy, time, chart_type]
                buy_signal_list.append(buy_signal)

        sorted_data = [bar_df[sorting.values][i] for i in range(len(bar_df[sorting.values])) if i in sort_index]

        return sorted_data, sell_signal_list, buy_signal_list

