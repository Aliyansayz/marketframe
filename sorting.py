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
