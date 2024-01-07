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
        # print(bar_list)
        bar_list = cls.refined_df(bar_list)

        return bar_list

    @classmethod
    def refined_df(cls, bar_list):

        symbols = 0  # index 0 for symbols
        values = 1  # index 1 for ohlc
        df_to_remove = [ ]
        for index, df in enumerate(bar_list[values]):
            if  df.empty:
                df_to_remove.append(index)
                continue
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
        df_to_remove.sort(reverse=True)

        for df_index in df_to_remove:
            bar_list[values].pop(df_index)
            bar_list[symbols].pop(df_index)

        # print(df_to_remove)
        return bar_list
