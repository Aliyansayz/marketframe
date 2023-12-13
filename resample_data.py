from datetime import datetime
import pytz

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

  def __init__(self, data_list , step = None, rotate = True , format = None  ):

    self.data_list = data_list
    self.step = step
    self.rotate = rotate
    self.format = str(format)

    # self.symbols = 0
    # self.values  = 1

  def run_resample_data(self ):
      bar_list = self.chart_version( bar_list = self.data_list , step= self.step, rotate = self.rotate , format = self.format )

      return bar_list

  def chart_version(self, bar_list, step=3, rotate = True, format = None ):

    symbols = 0  # index 0 for symbols
    values  = 1  # index 1 for ohlc

    if rotate == True:

        if format == 'pkt':
            # Set the time zone to Pakistan Standard Time (Asia/Karachi)
            pakistan_time_zone = pytz.timezone('Asia/Karachi')
            # Get the current time in Pakistan
            current_time = datetime.now(pakistan_time_zone)

        else:
             current_time = datetime.now()

        version    = int(current_time.strftime('%H')) % step

        for index , _ in enumerate (bar_list[values]):

              bar_list[values][index] = bar_list[values][index][version:]
    #   bar_list[values][index] as it is

    bar_list = self.aggregate_interval(bar_list= bar_list , step=step, format= self.format)
    return  bar_list


  def aggregate_interval(self , bar_list, step=3, timezone= None, format = None ):

      # step = 3
      symbols = 0  # index 0 for symbols
      values  = 1  # index 1 for ohlc

      bar_list_resampled = [ [] ] * 2
      bar_list_resampled[symbols] = [[]]  * len(bar_list[symbols])
      bar_list_resampled[values]  = [[]]  * len(bar_list[symbols])

      dt = np.dtype([ ('index', 'datetime64[h]' ), ('symbol', 'object'), ('Open', float), ('High', float), ('Low', float), ('Close', float) ])

      for symbol, ohlc in enumerate(bar_list[values]):

        if format :
          date_index = self.change_time( np.datetime_as_string(ohlc['index'], unit='s'), format= format)

        else :
          date_index = np.array(ohlc['index'] , dtype='datetime64[h]' )


        if step > 1 :
            resampled = date_index[::step]

        elif step == 1 :
            resampled = date_index

        # date_objects = [np.datetime64(date_str) for date_str in resampled ]
        # resampled_dates =  np.array(date_objects, dtype='datetime64[h]')
        select_open  = []
        select_high  = []
        select_low   = []
        select_close = []

        # step = 4 # i = 4 # 4 -4 # 5-4 # 8-4

        for i in range(0, len(bar_list[values][symbol]), step): # logic re solved for 'step' to 'step-1'


            select_open.append(ohlc['Open'][i:i+step][0])
            select_high.append(max(ohlc['High'][i:i+step]))
            select_low.append(min(ohlc['Low'][i:i+step]))
            select_close.append(ohlc['Close'][i:i+step][-1])

        data = np.empty(len(resampled), dtype=dt)

        # return select_close
        # return resampled
        for  i in range(len(resampled)):

            data[i] = ( resampled[i] ,  bar_list[symbols][symbol],   select_open[i],   select_high[i],  select_low[i], select_close[i] )

        bar_list_resampled[values][symbol]  =    data
        bar_list_resampled[symbols][symbol] =  bar_list[symbols][symbol]

      return bar_list_resampled


  def change_time(self, date_time_index, format= None):

      def convert_to_local_time(datetime_str, timezone  ):
          utc_zone = pytz.timezone('UTC')
          timezone_zone = pytz.timezone(f'{timezone}')
          utc_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
          utc_datetime = utc_zone.localize(utc_datetime)
          local_datetime = utc_datetime.astimezone(timezone_zone)

          return local_datetime.strftime('%Y-%m-%dT%H:%M:%S')

      if format == 'pkt': timezone = 'Asia/Karachi'
      else :     timezone = 'Asia/Karachi'
      vectorized_conversion = np.vectorize(convert_to_local_time , excluded=['timezone'] )

      converted = vectorized_conversion(date_time_index , timezone=timezone )
      formatted_datetime = np.array( converted , dtype='datetime64[h]' )

      return formatted_datetime
