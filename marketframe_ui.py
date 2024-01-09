from marketframe  import  get_clean_data
from marketframe  import  resample_data
from marketframe  import  access_indicators
from marketframe  import  indicators_lookback_mode

from marketframe  import  sorting
from marketframe  import  sorting_indices_crypto


class marketframe_run:
    strategy_list = ["ema_crossover_direction", "stochastic_crossover_direction"]
    market_source = None
    market_data   = None
    market_info   = None
    string_args, num_args = None , None
    buy_signal_list, sell_signal_list = [] , []
    @classmethod
    def get_clean_data_resample_data(cls,string_args, num_args):

        # cls.symbols, cls.timeframe , cls.period
        # bar_list = get_clean_data.get_data_np_df(symbols, interval='1H', period='7d')
        # string_args = [symbols, timeframe, hour, minute, period, timezone, ha_ohlc, strategy_list]
        # num_args = [step, lower_ema, higher_ema, atr_period, atr_multiplier, adx_period, last_candles, cross_check_only ]
        pass
        symbols, timeframe,  period =  string_args[0], string_args[1] ,string_args[4]
        hour, minute  = string_args[2], string_args[3]
        timezone = string_args[5]
        step = int(num_args[0])
        pass
        cls.ema_period = [int(num_args[1]), int(num_args[2])]
        cls.atr_period, cls.atr_multiplier, cls.adx_period = int(num_args[3]), float(num_args[4]), int(num_args[5])
        cls.last_candles = int(num_args[7])
        cls.lookback     = int(num_args[6])
        cls.ha_ohlc      = int(string_args[-2])
        cls.cross_only   = int(num_args[-1])
        pass
        # cls.strategy_list = string_args[-1]
        # ha_ohlc, strategy
        if timeframe == "Hour":
            interval = str(hour[:2])
            cls.chart_type = str(int(int(hour[0]) * step)) + str(f"{hour[-1]}")

        else:
            interval = str(minute)+"m"
            interval = str(hour[:2])
            cls.chart_type = str(int(int(minute) * step)) + str(f"{interval[-1]}")

        if timezone == "gmt": format = None
        else: format = timezone

        bar_list = get_clean_data.get_data_np_df(symbols = symbols, interval=interval , period=period )

        resample = resample_data( data_list=bar_list, step= step , rotate = False , format = format )        # resample = resample_data( data_list=bar_list , step=4 , rotate = False)
        cls.market_data = resample.run_resample_data()
        # chart = str(menu_hour.get()[:2])
        # if menu_timeframe.get() == "Hour":
        #     chart = str(menu_hour.get()[:2])
        #
        # elif menu_timeframe.get() == "Minute":
        #     chart = str(menu_minute.get()[:2])
        #
        # interval = chart
        # step = int(combobox_step.get())
        # chart_type = str(int(int(chart[0]) * step)) + str(f"{chart[-1]}")
        # selected_symbols = cls.get_selected_pairs()

        # bar_list = get_clean_data.get_data_np_df(symbols, interval='1H', period='7d')
        # resample = resample_data( data_list=bar_list , step=4 , rotate = True , format = 'pkt'  )
        # resample = resample_data(data_list=bar_list, step=1, rotate=False, format='pkt')
        # resample_list = resample.run_resample_data()
        # cls.resample_list = resample_list
    @classmethod
    def set_args(cls, num_args, string_args):
        cls.ema_period = [int(num_args[1]), int(num_args[2])]
        cls.atr_period, cls.atr_multiplier, cls.adx_period = int(num_args[3]), float(num_args[4]), int(num_args[5])
        cls.last_candles = int(num_args[7])
        cls.lookback = int(num_args[6])
        cls.ha_ohlc = int(string_args[-2])
        cls.cross_only = int(num_args[-1])

        if cls.cross_only == 1:  cls.cross_only = True
        else: cls.cross_only = False

        if cls.ha_ohlc == 1:  cls.ha_ohlc = True
        else:  cls.ha_ohlc = False

    @classmethod
    def get_market_info(cls):

        set_args(cls.num_args, cls.string_args)
        cls.market_info = indicators_lookback_mode.transform_data_list(refine_list=cls.market_data, multiplier=cls.atr_multiplier,
                                                                       atr_period=cls.atr_period , adx_period=cls.adx_period,
                                                                       lookback=cls.lookback,
                                                                       ema_period=cls.ema_period , ha_ohlc=cls.ha_ohlc)

    @classmethod
    def get_signals(cls, try_again= False) :

        if cls.market_info == None or try_again == True:
            cls.set_args(cls.num_args, cls.string_args)
            cls.market_info = indicators_lookback_mode.transform_data_list(refine_list=cls.market_data, multiplier=cls.atr_multiplier,
                                                                           atr_period=cls.atr_period, adx_period=cls.adx_period,
                                                                           lookback=cls.lookback,  ema_period=cls.ema_period,
                                                                           ha_ohlc=cls.ha_ohlc)

        sell_signal_list, buy_signal_list = [] , []
        for strategy in cls.strategy_list:
            if  strategy  == "ema_crossover_direction" :
                pass
                sorted_data, sell_signal, buy_signal = sorting.adx_crossover_ema(cls.market_info, last_candles=cls.last_candles, cross_only=cls.cross_only, chart_type=cls.chart_type)
                sell_signal_list.append(sell_signal), buy_signal_list.append(buy_signal)
                sorted_data, sell_signal, buy_signal = sorting.adx_direction_ema(cls.market_info,last_candles=cls.last_candles, cross_only=cls.cross_only, chart_type=cls.chart_type)
                sell_signal_list.extend(sell_signal), buy_signal_list.extend(buy_signal)

            elif strategy  == "stochastic_crossover_direction":
                pass
                sorted_data, sell_signal, buy_signal = sorting.adx_stochastic_momentum_crossover(cls.market_info, last_candles=cls.last_candles, cross_only=False, chart_type=cls.chart_type)
                sell_signal_list.append(sell_signal), buy_signal_list.append(buy_signal)
                sorted_data, sell_signal, buy_signal = sorting.adx_stochastic_momentum_direction(cls.market_info, last_candles=cls.last_candles,cross_only=cls.cross_only, chart_type=cls.chart_type)
                sell_signal_list.extend(sell_signal), buy_signal_list.extend(buy_signal)

        cls.sell_signal_list , cls.buy_signal_list = sell_signal_list, buy_signal_list
        print(sell_signal_list)
        print(buy_signal_list)

    @classmethod
    def get_signals_indices_crypto(cls, try_again= False) :

        if cls.market_info == None or try_again == True:
            cls.market_info = indicators_lookback_mode.transform_data_list(refine_list=cls.market_data, multiplier=cls.atr_multiplier,
                                                                           atr_period=cls.atr_period, adx_period=cls.adx_period,
                                                                           lookback=cls.lookback,  ema_period=cls.ema_period,
                                                                           ha_ohlc=cls.ha_ohlc)

        sell_signal_list, buy_signal_list = [], []
        for strategy in cls.strategy_list:
            if strategy == "ema_crossover_direction":
                pass
                sorted_data, sell_signal, buy_signal = sorting_indices_crypto.adx_crossover_ema(cls.market_info,last_candles=cls.last_candles,cross_only=cls.cross_only,chart_type=cls.chart_type)
                sell_signal_list.append(sell_signal), buy_signal_list.append(buy_signal)
                sorted_data, sell_signal, buy_signal = sorting_indices_crypto.adx_crossover_ema(cls.market_info,last_candles=cls.last_candles,cross_only=cls.cross_only,chart_type=cls.chart_type)
                sell_signal_list.extend(sell_signal), buy_signal_list.extend(buy_signal)

            elif strategy == "stochastic_crossover_direction":
                pass
                sorted_data, sell_signal, buy_signal = sorting_indices_crypto.adx_stochastic_momentum_crossover(cls.market_info,last_candles=cls.last_candles,cross_only=False,chart_type=None)
                sell_signal_list.append(sell_signal), buy_signal_list.append(buy_signal)
                sorted_data, sell_signal, buy_signal = sorting_indices_crypto.adx_stochastic_momentum_direction(cls.market_info,last_candles=cls.last_candles,cross_only=cls.cross_only,chart_type=cls.chart_type)
                sell_signal_list.extend(sell_signal), buy_signal_list.extend(buy_signal)

        cls.sell_signal_list, cls.buy_signal_list = sell_signal_list, buy_signal_list

    @classmethod
    def show_results(cls):

        # strategy_list = [[]] * len(cls.strategy_list)
        sell_textbox.delete("1.0", "end")
        buy_textbox.delete("1.0", "end")
        for index, buy_s in enumerate(cls.buy_signal_list):
                buy_textbox.insert("end", buy_s)
                buy_textbox.insert("end", "\n")

        for index, sell_s in enumerate(cls.sell_signal_list):
                sell_textbox.insert("end", sell_s)
                sell_textbox.insert("end", "\n")

    # @classmethod
    # def show_results(cls):
    #
    #     strategy_list = [ [] ] * len(cls.strategy_list)
    #     sell_textbox.delete("1.0", "end")
    #     buy_textbox.delete("1.0" , "end")
    #     for index, strategy in enumerate(cls.strategy_list):
    #
    #         buy_textbox.insert("end", f"\n#{strategy}#\n")
    #         sell_textbox.insert("end", f"\n#{strategy}#\n")
    #
    #         buy_s = [[]] * len(cls.buy_signal_list[index])
    #         for i,signal in enumerate(cls.buy_signal_list[index]):
    #             buy_s[i] = [f"\nsymbol: {signal[0]}\n", f"order_type: {signal[1]}\n",
    #                      f"take_profit: {signal[2]}\n" + f"stop_loss: {signal[3]}\n" +
    #                      f"strategy: {signal[4]}\n", f"time: {signal[5]}\n"]
    #
    #         sell_s = [[]] * len(cls.sell_signal_list[index])
    #         for i,signal in enumerate(cls.sell_signal_list[index]):
    #             sell_s[i] = [f"\nsymbol: {signal[0]}\n", f"order_type: {signal[1]}\n",
    #                      f"take_profit: {signal[2]}\n" + f"stop_loss: {signal[3]}\n" +
    #                      f"strategy: {signal[4]}\n", f"time: {signal[5]}\n", ]
    #
    #         if strategy == "ema_crossover_direction":
    #
    #             buy_textbox.insert("end", buy_s)
    #             buy_textbox.insert("end", "\n")
    #             sell_textbox.insert("end", sell_s)
    #             sell_textbox.insert("end", "\n")
    #
    #         elif strategy == "stochastic_crossover_direction":
    #             buy_textbox.insert("end", buy_s)
    #             buy_textbox.insert("end", "\n")
    #             sell_textbox.insert("end", sell_s)
    #             sell_textbox.insert("end", "\n")

    @classmethod
    def reset_app(cls):

        cls.market_source = None
        cls.market_data   = None
        cls.market_info   = None

                # strategy_list[index] =
        # bar_df = indicators_lookback_mode.transform_data_list(refine_list=resample_list, multiplier=1.7, \
        #                                                       atr_period=5, adx_period=8, lookback=14,
        #                                                       ema_period=[5, 20], ha_ohlc=True)


import customtkinter as ctk
import tkinter.filedialog as filedialog
import pickle

class ui_store(marketframe_run):

    @classmethod
    def get_default(cls, filename):
        pass
        try:
            # file_default : pass            # code_default
            with open("data.bin", "rb") as file:
                loaded_data = pickle.load(file)
            ctk.showinfo("Data Loaded", f"Loaded data: {loaded_data}")
        except FileNotFoundError:
            ctk.showerror("Error", "Data file not found.")

    @classmethod
    def show_hide_output_log(cls, root):
        # .configure(command=lambda pair=pair: cls.update_textbox())
        # scrollable_frame = ctk.CTkScrollableFrame(root, label_text="Available Symbols List")
        # scrollable_frame.grid(row=1, column=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # scrollable_frame.grid_columnconfigure(0, weight=2)

        global output_log

        def show_log():
            if log_checkbox.get():
                output_log.grid(row=5, column=2, padx=(2, 2), pady=(0, 0) )
            else:
                output_log.grid_forget()

        log_checkbox = ctk.CTkCheckBox(root, text="Show Logs", height=3, width=7,  hover_color="#39FF14" )
        log_checkbox.configure(command=show_log)
        log_checkbox.grid(row=5, column=4, columnspan=5, padx=(2, 2), pady=(1, 1))

        output_log = ctk.CTkTextbox(root, height=40, width=300)
        # output_log.grid(row=5, column=2)
        output_log.grid_forget()

    # @classmethod
    # def select_strategy(*args):
    #
    #     if menu_strategy.get() == "both":
    #         strategies = ["ema_crossover", "stochastic" ]
    #
    #     if menu_strategy.get() ==  "stochastic" :
    #         strategies = [ "stochastic" ]
    #
    #     if menu_strategy.get() == "ema_crossover":
    #         strategies = [ "ema_crossover" ]
    #
    #     print(menu_strategy.get())
        # pass



    @classmethod
    def show_popup(cls):
        popup = ctk.CTkToplevel()  # Create a new top-level window
        popup.geometry("300x200")  # Set its size
        popup.title("Popup Dialog")

        # Add labels, buttons, or other widgets to the popup
        label = ctk.CTkLabel(popup, text="This is a popup dialog!")
        label.grid()

        # Add a button to close the popup
        close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.grid()

    @classmethod
    def signal_popup(cls):
        popup = ctk.CTkToplevel()  # Create a new top-level window
        popup.geometry("500x500")  # Set its size
        popup.title("Popup Dialog")

        # Add labels, buttons, or other widgets to the popup
        label = ctk.CTkLabel(popup, text="This is a popup dialog!")
        label.grid()

        # Add a button to close the popup
        close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.grid()

    @classmethod
    def signals_textbox(cls, root, strategy, row, column, signal_type):

        result_frame = ctk.CTkScrollableFrame(master=root, label_text=signal_type)

        result_frame.grid(row=row, column=column, pady=(8, 8), sticky="nsew")
        if signal_type == "Buy Signal": color = "yellow"
        else : color = "white"

        textbox = ctk.CTkTextbox(result_frame, width=250, text_color=color,  font=ctk.CTkFont(size=20, weight="bold"), fg_color="black" )
        textbox.grid(row=0, column=0, sticky="nsew")  # Placed to the right

    @classmethod
    def sell_signal_textbox(cls, root, row, column):
        global sell_textbox
        sell_signal_textbox = ctk.CTkScrollableFrame(master=root, width=270, label_text="Sell Signal")

        sell_signal_textbox.grid(row=row, column=column, pady=(8, 8), sticky="nsew")
        color = "white"

        sell_textbox = ctk.CTkTextbox(sell_signal_textbox, width=270, text_color=color,
                                 font=ctk.CTkFont(size=20, weight="bold"), fg_color="black")
        sell_textbox.grid(row=0, column=0, sticky="nsew")  # Placed to the right

    @classmethod
    def buy_signal_textbox(cls, root, row, column):
        global  buy_textbox

        buy_signal_textbox = ctk.CTkScrollableFrame(master=root, width=270, label_text="Buy Signal")

        buy_signal_textbox.grid(row=row,  column=column, pady=(8, 8), sticky="nsew")
        color = "yellow"
        buy_textbox = ctk.CTkTextbox(buy_signal_textbox, width=270, text_color=color,
                                 font=ctk.CTkFont(size=20, weight="bold"), fg_color="black")
        buy_textbox.grid(row=0, column=0, sticky="nsew")  # Placed to the right

    @classmethod
    def set_state(cls, filename):
        pass

class checkbox(ui_store):

    @classmethod
    def strategy_checkbox(cls, root, strategy_list):
        global all_strategy, strategy_checkboxes, strategy_values

        strategy_values = strategy_list
        all_strategy = ctk.CTkCheckBox(root, text="All Strategies")
        all_strategy.configure(command=cls.toggle_strategy_checkboxes )
        all_strategy.grid(row=0, columnspan=4, sticky="we")

        strategy_checkboxes = []
        for i, pair in enumerate(strategy_values):
            row_strategy = i + 1
            col = 0
            checkbox_strat = ctk.CTkCheckBox(master=root, text=str(strategy_values[i]) )
            checkbox_strat.configure(command=lambda pair=pair: cls.update_strategy_textbox )
            strategy_checkboxes.append(checkbox_strat)
            checkbox_strat.grid(row=row_strategy, column=col, columnspan=4, pady=(5, 0), sticky="nw")

    @classmethod
    def update_strategy_textbox(cls):
            values_text = ""
            if all_strategy.get():
                # If "All Symbols" is checked, show all pairs
                values_text = "\n".join(strategy_values)
            else:
                # Otherwise, show only selected pairs
                for checkbox_strat in strategy_checkboxes:
                    if checkbox_strat.get():
                        values_text += checkbox_strat.cget("text") + "\n"  #
            output_log.delete("1.0", "end")
            output_log.insert("end", values_text)
            print(values_text)

    @classmethod
    def toggle_strategy_checkboxes(cls):
        for checkbox in strategy_checkboxes:
            if all_strategy.get():
                checkbox.configure(state="disabled")
            else:
                checkbox.configure(state="normal")
        cls.update_strategy_textbox()  # Update the text area after toggling

    @classmethod
    def get_selected_strategies(cls):
        if all_checkbox.get():
            return strategy_values
        else:
            return [pair for checkbox, pair in zip(strategy_checkboxes, strategy_values) if checkbox.get()]

    @classmethod
    def symbols_checkbox(cls, root, symbols, row, symbols_checked= None ): # row --> 1
        global all_checkbox, checkboxes, textbox
        columns = 4
        # Placed first
        textbox = ctk.CTkTextbox(root, width=250 , font=ctk.CTkFont(size=15, weight="bold"))
        textbox.grid(row=0, column=4, sticky="nsew")  # Placed to the right
        time_to_trade = []
        aus_time = "Sydney Session (Australia)\n Opens at 10:00 PM GMT\n Closes at 7:00 AM GMT\n"
        jp_time  = "Tokyo Session (Japan):\n Opens at 12:00 AM GMT\n Closes at 9:00 AM GMT\n"
        eur_uk_time =  "London Session (United Kingdom):\n Opens at 8:00 AM GMT\n Closes at 5:00 PM GMT\n"
        us_time = "New York Session (United States):\n Opens at 1:00 PM GMT\n Closes at 10:00 PM GMT\n"
        time_to_trade.append(aus_time) ,  time_to_trade.append(jp_time)
        time_to_trade.append(eur_uk_time), time_to_trade.append(us_time)
        textbox.insert("1.0", time_to_trade)

        cls.forex_sessions_info = time_to_trade
        # time_to_trade = "1:00PM ->  10:00PM \nPST "

        scrollable_frame = ctk.CTkScrollableFrame(root, label_text="Available Symbols List")
        scrollable_frame.grid(row=row, column=4, padx=(20, 20), pady=(20, 0), sticky="nsew")
        scrollable_frame.grid_columnconfigure(0, weight=2)

        # Create an "All Symbols" checkbox
        all_checkbox = ctk.CTkCheckBox(master=scrollable_frame, text="All Symbols", fg_color="#39FF14",  hover_color="#39FF14" )
        all_checkbox.configure(command=cls.toggle_checkboxes)
        all_checkbox.grid(row=0, columnspan=columns, sticky="w")

        checkboxes = []
        for i, pair in enumerate(symbols):
            row = i + 1
            col = 0
            checkbox = ctk.CTkCheckBox(master=scrollable_frame, text=symbols[i][:6], fg_color="#39FF14",  hover_color="#39FF14" )
            checkbox.configure(command=lambda pair=pair: cls.update_textbox())
            if symbols_checked :
                if len(symbols_checked) == len(symbols) : cls.toggle_checkboxes()
                if checkbox.cget("text") in symbols_checked:
                    checkbox.select()
                    cls.update_textbox()
                    # values_text += checkbox.cget("text") + "\n"
                    # textbox.delete("1.0", "end")
                    # textbox.insert("end", values_text)

            checkboxes.append(checkbox)
            checkbox.grid(row=row, column=col, sticky="nw")

            # if  checkbox.cget("text") in symbols_checked:
            #     checkbox.select()


    @classmethod
    def toggle_checkboxes(cls):
        for checkbox in checkboxes:
            if all_checkbox.get():
                checkbox.configure(state="disabled")
            else:
                checkbox.configure(state="normal")
        cls.update_textbox()  # Update the text area after toggling


    @classmethod
    def update_textbox(cls):

        values_text = ""
        if all_checkbox.get():
            # If "All Symbols" is checked, show all pairs
            values_text = "\n".join(symbols)
        else:
            # Otherwise, show only selected pairs
            for checkbox in checkboxes:
                if checkbox.get():
                    values_text += checkbox.cget("text") + "\n"  # Added "=X" for
        textbox.delete("1.0", "end")
        textbox.insert("end", values_text)
        # cls.asset_state["asset_type"][f"{asset_type}"]["symbols_checkbox"] = #####


    @classmethod
    def get_selected_pairs(cls):
        if all_checkbox.get():
            return symbols
        else:
            return [pair for checkbox, pair in zip(checkboxes, symbols) if checkbox.get()]

    @classmethod
    def fetch_and_update_data(cls):

        selected_pairs = cls.get_selected_pairs()
        if selected_pairs:
            #     # pass
            print(selected_pairs)
        # ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X']

    @classmethod
    def symbols_name_checkbox(cls, root, symbols, row, names):  # row --> 1
        global all_checkbox, checkboxes, textbox
        columns = 4
        symbol_name = [str(symbols[i]) + " " + str(names[i]) for i in range(len(symbols))]
        # Placed first
        textbox = ctk.CTkTextbox(root, width=250, font=ctk.CTkFont(size=20, weight="bold"))
        textbox.grid(row=0, column=4, sticky="nsew")  # Placed to the right
        time_to_trade = "1:00PM ->  10:00PM \nPST "
        textbox.insert("1.0", time_to_trade)
        scrollable_frame = ctk.CTkScrollableFrame(root, label_text="Available Symbols List")
        scrollable_frame.grid(row=row, column=4, padx=(20, 20), pady=(20, 0), sticky="nsew")
        scrollable_frame.grid_columnconfigure(0, weight=2)

        # Create an "All Symbols" checkbox
        all_checkbox = ctk.CTkCheckBox(master=scrollable_frame, text="All Symbols", fg_color="#39FF14",  hover_color="#39FF14")
        all_checkbox.configure(command=cls.toggle_checkboxes)
        all_checkbox.grid(row=0, columnspan=columns, sticky="w")

        checkboxes = []
        for i, pair in enumerate(symbols):
            row = i + 1
            col = 0
            checkbox = ctk.CTkCheckBox(master=scrollable_frame, text=symbol_name[i], fg_color="#39FF14",  hover_color="#39FF14")
            checkbox.configure(command=lambda pair=pair: cls.update_textbox())
            checkboxes.append(checkbox)
            checkbox.grid(row=row, column=col, sticky="nw")


    @classmethod
    def symbols_name_checkbox_crypto(cls, root, symbols, row, names):  # row --> 1
        global all_checkbox, checkboxes, textbox
        columns = 4
        symbol_name = [str(symbols[i]) + " " + str(names[i]) for i in range(len(symbols))]
        # Placed first
        textbox = ctk.CTkTextbox(root, width=250, font=ctk.CTkFont(size=20, weight="bold"))
        textbox.grid(row=0, column=4, sticky="nsew")  # Placed to the right
        time_to_trade = "1:00PM ->  10:00PM \nPST For Crypto "
        textbox.insert("1.0", time_to_trade)
        scrollable_frame = ctk.CTkScrollableFrame(root, label_text="Available Symbols List")
        scrollable_frame.grid(row=row, column=4, padx=(20, 20), pady=(20, 0), sticky="nsew")
        scrollable_frame.grid_columnconfigure(0, weight=2)

        # Create an "All Symbols" checkbox
        all_checkbox = ctk.CTkCheckBox(master=scrollable_frame, text="All Symbols", fg_color="#39FF14",  hover_color="#39FF14")
        all_checkbox.configure(command=cls.toggle_checkboxes)
        all_checkbox.grid(row=0, columnspan=columns, sticky="w")

        checkboxes = []
        for i, pair in enumerate(symbols):
            row = i + 1
            col = 0
            checkbox = ctk.CTkCheckBox(master=scrollable_frame, text=symbol_name[i][:-3], fg_color="#39FF14",  hover_color="#39FF14")
            checkbox.configure(command=lambda pair=pair: cls.update_textbox())
            checkboxes.append(checkbox)
            checkbox.grid(row=row, column=col, sticky="nw")

class tab_ui(checkbox):

    @classmethod
    def chart_tab(cls, root, row):
        global combobox_step, menu_timeframe, menu_minute, \
            menu_hour, menu_period, menu_timezone, get_button

        tabview = ctk.CTkTabview(root, width=250 )
        tabview.grid(row=row, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        chart_tab, timezone_tab = "Chart", "Timezone"
        tabview.add(chart_tab)

        tabview.add(timezone_tab)
        tabview.tab(chart_tab).grid_columnconfigure(0, weight=0)  # configure grid of individual tabs

        # get_button = ctk.CTkButton(tabview, text="GET DATA", command=lambda: print(1))
        # get_button.grid(row=9, column=0, padx=7, pady=7)
        scrollable_chart_tab = ctk.CTkScrollableFrame(master=tabview.tab(chart_tab),
                                                      label_text="Indicators Input")
        scrollable_chart_tab.grid(row=0, column=4, padx=(7, 7), pady=(5, 5), sticky="nsew")

        placeholder_timeframe = "Select Timeframe Type..."  # Placeholder text
        label_timeframe = ctk.CTkLabel(master=scrollable_chart_tab, text=placeholder_timeframe)
        label_timeframe.grid(row=0, column=0, padx=20, pady=(10, 10))

        menu_timeframe = ctk.CTkOptionMenu(master=scrollable_chart_tab,
                                           values=["Hour", "Minute"])
        menu_timeframe.grid(row=1, column=0, padx=0, pady=(10, 10))
        menu_timeframe.configure(command=cls.toggle_timeframes)

        placeholder_minute = "Select Minute Chart..."
        label_minute = ctk.CTkLabel(master=scrollable_chart_tab, text=placeholder_minute)
        label_minute.grid(row=2, column=0, padx=20, pady=(10, 10))

        menu_minute = ctk.CTkOptionMenu(master=scrollable_chart_tab, values=["15", "30"])
        menu_minute.grid(row=3, column=0, padx=20, pady=(10, 10))
        menu_minute.set("15")

        placeholder_hour = "Select Hour Chart..."
        label_hour = ctk.CTkLabel(master=scrollable_chart_tab,  text=placeholder_hour)
        label_hour.grid(row=4, column=0, padx=20, pady=(10, 10))

        menu_hour = ctk.CTkOptionMenu(master=scrollable_chart_tab,
                                      values=[placeholder_hour, "1Hour", "4Hour", "Day"])
        menu_hour.grid(row=5, column=0, padx=20, pady=(10, 10))
        # .grid_forget()

        placeholder_step = "Select Step Value..."

        label_step = ctk.CTkLabel(master=scrollable_chart_tab, text=placeholder_step)
        label_step.grid(row=6, column=0, padx=20, pady=(10, 10))

        combobox_step = ctk.CTkComboBox(master=scrollable_chart_tab,
                                        values=["1", "2", "3", "4", "5"])
        combobox_step.grid(row=7, column=0, padx=20, pady=(10, 10))

        placeholder_period = "Select Period..."  # Placeholder text
        label_period = ctk.CTkLabel(master=scrollable_chart_tab, text=placeholder_period)
        label_period.grid(row=8, column=0, padx=20, pady=(10, 10))

        menu_period = ctk.CTkComboBox(master=scrollable_chart_tab,
                                      values=["7d", "1d"])
        menu_period.grid(row=9, column=0, padx=0, pady=(10, 10))
        # menu_period.configure(command=cls.toggle_timeframes)

        scrollable_timezone_tab = ctk.CTkScrollableFrame(master=tabview.tab(timezone_tab),
                                                         label_text="Define Strategy")
        scrollable_timezone_tab.grid(row=0, column=4, padx=(7, 7), pady=(5, 5), sticky="nsew")

        placeholder_timezone = "Select Timezone Type.."
        label_timezone = ctk.CTkLabel(master=scrollable_timezone_tab, text=placeholder_timezone)
        label_timezone.grid(row=0, column=0, padx=20, pady=(10, 10))

        menu_timezone = ctk.CTkOptionMenu(master=scrollable_timezone_tab,
                                          values=["gmt", "pkt"])
        menu_timezone.grid(row=1, column=0, padx=0, pady=(10, 10))

        # menu_timeframe.set("Hour")
        # combobox_step.set("1")
        # menu_hour.set("1Hour")
        # menu_period.set("7d")
        # menu_timezone.set("pkt")

    @classmethod
    def toggle_timeframes(cls, *args):
        if menu_timeframe.get() == "Minute":
            # print("Minute True")
            menu_hour.configure(state="disabled")
            # .configure(state="disabled")
            menu_minute.configure(state="normal")

        elif menu_timeframe.get() == "Hour":
            # print("Hour True")
            menu_minute.configure(state="disabled")
            menu_hour.configure(state="normal")

    @classmethod
    def indicators_strategy_tab(cls, root, row):
        global  menu_strategy, option_last_candles, cross_only_check, menu_lower_ema, \
            menu_higher_ema, menu_atr_period, menu_adx_period, menu_atr_multiplier, switch_ha, menu_lookback_period

        tabview = ctk.CTkTabview(root, width=250)
        tabview.grid(row=row, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        indicators_tab, strategy_tab = "Indicators", "Strategy"
        tabview.add(indicators_tab)
        tabview.add(strategy_tab)
        tabview.tab(indicators_tab).grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        tabview.tab(strategy_tab).grid_columnconfigure(0, weight=1)

        # signal_button = ctk.CTkButton(tabview, text="GET SIGNALS", command=lambda: print(1))
        # signal_button.grid(row=9, column=0, padx=7, pady=7)
        scrollable_indicator_tab = ctk.CTkScrollableFrame(master=tabview.tab(indicators_tab),
                                                          label_text="Indicators Input")
        scrollable_indicator_tab.grid(row=0, column=4, padx=(7, 7), pady=(5, 5), sticky="nsew")

        scrollable_strategy_tab = ctk.CTkScrollableFrame(master=tabview.tab(strategy_tab),
                                                         label_text="Define Strategy")
        scrollable_strategy_tab.grid(row=0, column=4, padx=(7, 7), pady=(5, 5), sticky="nsew")

        placeholder_hour = "Select Hour Chart..."
        label_ema = ctk.CTkLabel(master=scrollable_indicator_tab, text="Lower/Higher EMA")
        label_ema.grid(row=0, column=0, padx=20, pady=(10, 10))

        lower_ema, higher_ema = "Type Lower EMA", "Type Higher EMA"
        menu_lower_ema = ctk.CTkComboBox(master=scrollable_indicator_tab,
                                         values=[lower_ema, "5", "7", "9"])
        menu_higher_ema = ctk.CTkComboBox(master=scrollable_indicator_tab,
                                          values=[higher_ema, "20", "21", "34"])

        menu_lower_ema.grid(row=1, column=0, padx=20, pady=(10, 10))
        menu_higher_ema.grid(row=2, column=0, padx=20, pady=(10, 10))
        # .grid_forget()

        label_atr = ctk.CTkLabel(master=scrollable_indicator_tab, text="ATR Period With Multiplier")
        label_atr.grid(row=3, column=0, padx=20, pady=(10, 10))

        atr_text, adx_text = "Type ATR Period", "Type ADX Period"
        menu_atr_period = ctk.CTkComboBox(master=scrollable_indicator_tab,
                                          values=[atr_text, "5", "7", "3"])
        menu_atr_period.grid(row=4, column=0, padx=20, pady=(10, 10))

        placeholder_atr = "Select ATR Multiplier..."
        menu_atr_multiplier = ctk.CTkComboBox(master=scrollable_indicator_tab,
                                              values=["1.7", placeholder_atr, "2.0", "3.0", "1.9", "1.8"])
        menu_atr_multiplier.grid(row=5, column=0, padx=20, pady=(10, 10))

        menu_adx_period = ctk.CTkComboBox(master=scrollable_indicator_tab,
                                          values=[adx_text, "8", "10", "14"])
        label_adx = ctk.CTkLabel(master=scrollable_indicator_tab, text="ADX Period")
        label_adx.grid(row=6, column=0, padx=20, pady=(10, 10))

        menu_adx_period.grid(row=7, column=0, padx=20, pady=(10, 10))

        cross_only_check = ctk.CTkCheckBox(master=scrollable_indicator_tab, text="Cross Check Only")
        cross_only_check.grid(row= 8 , column=0, padx=10, pady=(10, 10))


        placeholder_last_candles = "Select Lookback And Last Candles Filter"
        label_last_candles = ctk.CTkLabel(master=scrollable_indicator_tab, text=placeholder_last_candles)
        label_last_candles.grid(row=9, column=0, padx=20, pady=(10, 10))
        menu_lookback_period = ctk.CTkComboBox(master=scrollable_indicator_tab, values=["14", "21", "35"])
        menu_lookback_period.grid(row=10, column=0, padx=20, pady=(10, 10))

        option_last_candles = ctk.CTkComboBox(master=scrollable_indicator_tab,
                                              values=["15", "30"])
        option_last_candles.grid(row=11, column=0, padx=20, pady=(10, 10))

        switch_ha = ctk.CTkSwitch(master=scrollable_indicator_tab, text="Switch To Heikin Ashi ")
        switch_ha.grid(row=12, column=0, padx=10, pady=(0, 20))

        # strategy_values = ["ema_crossover", "stochastic"]
        strategy_values = cls.strategy_list
        # cls.strategy_values = strategy_values

        cls.strategy_checkbox(scrollable_strategy_tab, strategy_values )
        # placeholder_strategy = "Select Your Strategy Type"  # Placeholder text

        # all_strategy = ctk.CTkCheckBox(master=scrollable_strategy_tab, text="All Strategies")
        # all_strategy.configure(command=cls.toggle_strategy_checkboxes)
        # all_strategy.grid(row=0, columnspan=4, sticky="we")
        #
        # strategy_checkboxes = []
        # for i, pair in enumerate(strategy_values):
        #     row_strategy = i + 1
        #     col = 0
        #     checkbox = ctk.CTkCheckBox(master=scrollable_strategy_tab, text= strategy_values[i] )
        #     checkbox.configure(command=lambda pair=pair: cls.update_strategy_textbox )
        #     strategy_checkboxes.append(checkbox)
        #     checkbox.grid(row=row_strategy, column=col, columnspan=4, pady=(5, 0),  sticky="nw")

        # menu_lookback_period.set("21")
        # option_last_candles.set("14")
        # menu_atr_multiplier.set("1.7")
        # menu_atr_period.set("5")
        # menu_adx_period.set("10")
        # menu_lower_ema.set("5")
        # menu_higher_ema.set("20")
        # switch_ha.select()




class access_ui(tab_ui):
    pass

class marketframe_store(access_ui):
    previous_asset, current_asset = "forex", ""
    string_args, num_args = [], []
    asset_last_state = None
    asset_state = {
        "asset_type": {
            "forex": {
                "asset_last_state": False, "market_data": [], "sell_textbox": "", "buy_textbox": "", "symbols_checkbox": [],
                "strategy_checkbox": [],
                "num_args": 0, "step": "", "adx_period": "", "atr_period_multiplier": [], "lower_higher_ema": [],
                "lookback_last_candles": [], "chart_period": "", "channel_strength": ""
            },
            "crypto": {
                "asset_last_state": False, "sell_textbox": "", "buy_textbox": "", "symbols_checkbox": [],
                "strategy_checkbox": [],
                "num_args": 0, "step": "", "adx_period": "", "atr_period_multiplier": [], "lower_higher_ema": [],
                "lookback_last_candles": [], "chart_period": "", "channel_strength": ""
            },
            "stocks": {
                "asset_last_state": False, "sell_textbox": "", "buy_textbox": "", "symbols_checkbox": [],
                "strategy_checkbox": [],
                "num_args": 0, "step": "", "adx_period": "", "atr_period_multiplier": [], "lower_higher_ema": [],
                "lookback_last_candles": [], "chart_period": ""},
            "indices": {
                "asset_last_state": False, "sell_textbox": "", "buy_textbox": "", "symbols_checkbox": [],
                "strategy_checkbox": [],
                "num_args": 0, "step": "", "adx_period": "", "atr_period_multiplier": [], "lower_higher_ema": [],
                "lookback_last_candles": [], "chart_period": ""}

        }
    }

    @classmethod
    def retrieve_asset_state(cls,root, asset_type):

        cls.symbols_checked = cls.asset_state["asset_type"][f"{asset_type}"]["symbols_checkbox"]
        # print(cls.symbols_checked)
        ## TO BE REMOVED # cls.symbols_checkbox(root, symbols, row=1, symbols_checked=cls.symbols_checked)


        # for i, checkbox in enumerate(checkboxes):
        #     if  checkbox.cget("text") in cls.symbols_checked:
        #         checkbox.select()

        # strategy_checked = cls.asset_state["asset_type"][f"{asset_type}"]["strategy_checkbox"]
        # for checkbox, strategy in zip(strategy_checkboxes, strategy_values):
        #     if checkbox.cget("text") in strategy_checked: checkbox.select()

        # menu_timeframe.set("Hour"), \
        lookback_last_candles = cls.asset_state["asset_type"][f"{asset_type}"]["lookback_last_candles"]
        atr_period_multiplier = cls.asset_state["asset_type"][f"{asset_type}"]["atr_period_multiplier"]
        lower_higher_ema = cls.asset_state["asset_type"][f"{asset_type}"]["lower_higher_ema"]
        adx_period = cls.asset_state["asset_type"][f"{asset_type}"]["adx_period"]


        combobox_step.set("1"), menu_hour.set("1Hour"),
        menu_period.set("7d"), menu_timezone.set("pkt")
        pass
        menu_lookback_period.set(str(lookback_last_candles[0])), \
        option_last_candles.set(str(lookback_last_candles[1])), \
        menu_atr_period.set(atr_period_multiplier[0]), menu_atr_multiplier.set(atr_period_multiplier[1])

        menu_adx_period.set(adx_period), \
        menu_lower_ema.set(str(lower_higher_ema[0])), menu_higher_ema.set(str(lower_higher_ema[1])),
        switch_ha.select()

        sell_text = cls.asset_state["asset_type"][f"{asset_type}"]["sell_textbox"]
        buy_text  = cls.asset_state["asset_type"][f"{asset_type}"]["buy_textbox"]

        try:
            sell_textbox.insert("end", sell_text)
            buy_textbox.insert("end", buy_text)
            cls.market_data = cls.asset_state["asset_type"][f"{asset_type}"]["market_data"]
        except:
            pass

    # ["asset_type"]["forex"]["symbols_checkbox"] = buy_textbox
    @classmethod
    def store_asset_state(cls, asset_type):

        cls.asset_state["asset_type"][f"{asset_type}"]["asset_last_state"] = True
        cls.asset_state["asset_type"][f"{asset_type}"]["symbols_checkbox"] = cls.string_args[0]
        cls.asset_state["asset_type"][f"{asset_type}"]["strategy_checkbox"] = cls.string_args[-1]

        cls.asset_state["asset_type"][f"{asset_type}"]["step"] = cls.num_args[0]

        cls.asset_state["asset_type"][f"{asset_type}"]["adx_period"] = cls.num_args[5]

        cls.asset_state["asset_type"][f"{asset_type}"]["atr_period_multiplier"] = [cls.num_args[3], cls.num_args[4]]

        cls.asset_state["asset_type"][f"{asset_type}"]["lower_higher_ema"] = [cls.num_args[1], cls.num_args[2]]

        cls.asset_state["asset_type"][f"{asset_type}"]["lookback_last_candles"] = [cls.num_args[6], cls.num_args[7]]

        # step, lookback = combobox_step.get(), menu_lookback_period.get()
        # atr_period, atr_multiplier, adx_period = menu_atr_period.get(), menu_atr_multiplier.get(), menu_adx_period.get()
        # lower_ema, higher_ema, last_candles

        try:
            cls.asset_state["asset_type"][f"{asset_type}"]["sell_textbox"] = sell_textbox.get("1.0", "end")
            cls.asset_state["asset_type"][f"{asset_type}"]["buy_textbox"]  = buy_textbox.get("1.0", "end")
            cls.asset_state["asset_type"][f"{asset_type}"]["market_data"]  = cls.market_data
        except:
            pass


    @classmethod
    def input_args(cls):

        timeframe, hour, minute = menu_timeframe.get(), menu_hour.get(), menu_minute.get()
        period, timezone, ha_ohlc = menu_period.get(), menu_timezone.get(), switch_ha.get()
        strategy_list = cls.get_selected_strategies()
        step, lookback = combobox_step.get() , menu_lookback_period.get()
        atr_period, atr_multiplier, adx_period = menu_atr_period.get(), menu_atr_multiplier.get(), menu_adx_period.get()
        lower_ema, higher_ema, last_candles = menu_lower_ema.get(), menu_higher_ema.get(), option_last_candles.get()
        symbols = cls.get_selected_pairs()
        cross_check_value = cross_only_check.get()
        string_args = [symbols, timeframe, hour, minute, period, timezone, ha_ohlc, strategy_list]
        num_args    = [step, lower_ema, higher_ema, atr_period, atr_multiplier, adx_period, lookback, last_candles, cross_check_value ]

        cls.string_args, cls.num_args = string_args, num_args

        return  string_args, num_args

    @classmethod
    def set_default_args(cls):

        menu_timeframe.set("Hour"), combobox_step.set("1"), menu_hour.set("1Hour"),
        menu_period.set("7d"),      menu_timezone.set("pkt")
        menu_lookback_period.set("21"), option_last_candles.set("14"), menu_atr_multiplier.set("1.7")
        menu_atr_period.set("5"),menu_adx_period.set("10"), menu_lower_ema.set("5"),
        menu_higher_ema.set("20"), switch_ha.select()


    @classmethod
    def set_crypto_default_args(cls):

        menu_timeframe.set("Minute"), combobox_step.set("1"), menu_hour.set("1Hour"),
        menu_period.set("1d"),  menu_timezone.set("gmt")
        menu_lookback_period.set("21"), option_last_candles.set("14"), menu_atr_multiplier.set("1.7")
        menu_atr_period.set("5"),  menu_adx_period.set("20"), menu_lower_ema.set("20"),
        menu_higher_ema.set("50"), switch_ha.select()

    @classmethod
    def result_args(cls):
        pass

    @classmethod
    def run_get_signal_indices_crypto(cls):
        string_args, num_args = cls.input_args()
        if cls.market_data != None:
            cls.get_signals_indices_crypto()

        else:
            cls.get_clean_data_resample_data(string_args, num_args)
            cls.get_signals_indices_crypto()

        cls.show_results()


    @classmethod
    def run_try_again_indices_crypto(cls, *args):

        string_args, num_args = cls.input_args()
        if cls.market_data != None:
            cls.get_signals(try_again=True)

        cls.show_results()


    @classmethod
    def run_get_signal_forex(cls, *args):

        string_args, num_args = cls.input_args()
        if cls.market_data != None:
            cls.get_signals()

        else:
            cls.get_clean_data_resample_data(string_args, num_args)
            cls.get_signals()

        cls.show_results()

    @classmethod
    def run_reset_app(cls):
        cls.reset_app()


    @classmethod
    def run_get_signal(cls, *args):

        string_args, num_args = cls.input_args()
        if cls.market_data != None:
            cls.get_signals()

        else:
            cls.get_clean_data_resample_data(string_args, num_args)
            cls.get_signals()

        cls.show_results()

    @classmethod
    def run_try_again(cls, *args):

        string_args, num_args = cls.input_args()
        if cls.market_data != None:
            cls.get_signals(try_again=True)

        cls.show_results()


    @classmethod
    def retrieve_state(cls):
        pass



class forex_ui_groups(marketframe_store) :

    @classmethod
    def forex_ui(cls, root, asset_type ):

        # global all_checkbox, forex_pairs, checkboxes, textbox

        def browse_files():
            filename = filedialog.askopenfilename()
            if filename:
                # Process the selected file
                print("Selected file:", filename)

        commodities = ["GC=F"]
        indices = [ "^IXIC", "^GSPC", "^DJI" ,  "^NYA" ,"^VIX", "^N100", "^DJI" ,"^FTSE" , "^N225",  "^BFX", "^STOXX50E", "^HSI", "^GDAXI", "^FCHI", "^RUT"  ]
        # Nasdaq , S&P 500,  DOW jones, NYSE, CBOE Volatility Index,  DOW Jones , UK100 ,  Nikkei Osaka , ^BFX Brussel, Zurich, Hong kong, Germany index
                                                                    #  , Paris , Russell 2000

        forex_pairs = [
            'AUDCAD=X', 'AUDCHF=X', 'AUDJPY=X', 'AUDNZD=X', 'AUDUSD=X',
            'CADCHF=X', 'CADJPY=X',
            'CHFJPY=X',
            'EURAUD=X', 'EURCAD=X', 'EURCHF=X', 'EURGBP=X', 'EURJPY=X', 'EURNZD=X', 'EURUSD=X',
            'GBPAUD=X', 'GBPCAD=X', 'GBPCHF=X', 'GBPJPY=X', 'GBPUSD=X', 'GBPNZD=X',
            'NZDCAD=X', 'NZDCHF=X', 'NZDJPY=X', 'NZDUSD=X',
            'USDCHF=X', 'USDCAD=X', 'USDJPY=X'
        ]

        global  symbols

        symbols = forex_pairs

        pass
        cls.chart_tab(root, row=1)
        # cls.chart_tab(root)
        pass
        cls.symbols_checkbox(root, symbols=symbols, row=1)
        cls.indicators_strategy_tab(root, row=1)

        cls.buy_signal_textbox(root, row=0, column=3)
        cls.sell_signal_textbox(root, row=0, column=2)





        signal_button = ctk.CTkButton(root, text="Get Signal", height=22, width=122, command=cls.run_get_signal )
        signal_button.grid(row=4, column=0, columnspan=3, padx=(2,2), pady=(10, 1) )
        signal_button.configure( text_color="#39FF14" , fg_color="black" )

        try_again_button = ctk.CTkButton(root, text="Try Again", height=22, width=122, command=cls.run_try_again)
        try_again_button.grid(row=4, column=1, columnspan=3, padx=(2, 2), pady=(10, 1))
        try_again_button.configure(text_color="#39FF14", fg_color="black")

        save_button = ctk.CTkButton(root, text="SAVE", height=22, width=122, command=cls.run_reset_app)
        save_button.grid(row=4, column=2, columnspan=3, padx=(2, 2), pady=(10, 1))
        save_button.configure(text_color="#39FF14", fg_color="black")

        reset_button = ctk.CTkButton(root, text="RESET", height=22, width=122, command=cls.run_reset_app )
        reset_button.grid(row=4, column=4, columnspan=3, padx=(2,2), pady=(10, 1) )
        reset_button.configure(text_color="red", fg_color="black")

        cls.show_hide_output_log(root)


        if cls.asset_state["asset_type"][f"{asset_type}"]["asset_last_state"] == False :
            cls.set_default_args()

        if cls.asset_state["asset_type"][f"{asset_type}"]["asset_last_state"] == True :
            cls.retrieve_asset_state(root, asset_type="forex")

        cls.asset_state["asset_type"][f"{asset_type}"]["asset_last_state"] = True



    @classmethod
    def forex_args(cls):

        timeframe, hour, minute   =  menu_timeframe.get(), menu_hour.get(), menu_minute.get()
        period,  timezone, ha_ohlc  =  menu_period.get(), menu_timezone.get(), switch_ha.get()
        strategy = strategies
        step     =  combobox_step.get()
        atr_period, atr_multiplier, adx_period  = menu_atr_period.get(), menu_atr_multiplier.get(), menu_adx_period.get()
        lower_ema, higher_ema, last_candles = menu_lower_ema.get(), menu_higher_ema.get(), option_last_candles.get()
        symbols =     cls.get_selected_pairs()
        string_args = [symbols, timeframe, hour, minute, period,  timezone, ha_ohlc, strategy  ]
        num_args = [step, last_candles, atr_period, adx_period, ]

        menu_timeframe.set("Hour")
        combobox_step.set("1")
        menu_hour.set("1Hour")
        menu_period.set("7d")
        menu_timezone.set("pkt")

        option_last_candles.set("14")
        menu_atr_multiplier.set("1.7")
        menu_atr_period.set("5")
        menu_adx_period.set("10")
        menu_lower_ema.set("5")
        menu_higher_ema.set("20")
        switch_ha.select()

    # @classmethod
    # def symbols_checkbox(cls, root, symbols):
    #
    #     global all_checkbox, checkboxes, textbox
    #
    #     columns = 4
    #
    #     # Placed first
    #     textbox = ctk.CTkTextbox(root, width=250)
    #     textbox.grid(row=0, column=4, sticky="nsew")  # Placed to the right
    #
    #     scrollable_frame = ctk.CTkScrollableFrame(root, label_text="Available Symbols List")
    #     scrollable_frame.grid(row=1, column=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
    #     scrollable_frame.grid_columnconfigure(0, weight=2)
    #
    #     # Create an "All Symbols" checkbox
    #     all_checkbox = ctk.CTkCheckBox(master=scrollable_frame, text="All Symbols")
    #     all_checkbox.configure(command=cls.toggle_checkboxes)
    #     all_checkbox.grid(row=0, columnspan=columns, sticky="w")
    #
    #     # Create the text box
    #     # textbox.grid(row=len(forex_pairs) // columns + 2, columnspan=columns)  # Use grid for text area
    #
    #     checkboxes = []
    #     for i, pair in enumerate(symbols):
    #         row = i + 1
    #         col = 0
    #         checkbox = ctk.CTkCheckBox(master=scrollable_frame, text=symbols[i][:6])
    #         checkbox.configure(command=lambda pair=pair: cls.update_textbox())
    #         checkboxes.append(checkbox)
    #         checkbox.grid(row=row, column=col, sticky="nw")  # Use grid for checkboxes
    #





            # .configure(state="disabled")
        # print("Arguments passed:", args)
        # print(optionmenu_timeframe.get())

    @classmethod
    def update_textbox(cls):
        # global data
        # last_close = data["Close"].iloc[-1]
        values_text = ""
        if all_checkbox.get():
            # If "All Symbols" is checked, show all pairs
            values_text = "\n".join(symbols)
        else:
            # Otherwise, show only selected pairs
            for checkbox in checkboxes:
                if checkbox.get():
                    values_text += checkbox.cget("text") + "=X\n"  # Added "=X" for
        textbox.delete("1.0", "end")
        textbox.insert("end", values_text)

    # textbox.insert( "end", last_close )

    # Function to toggle checkbox states (unchanged)
    @classmethod
    def toggle_checkboxes(cls):
        for checkbox in checkboxes:
            if all_checkbox.get():
                checkbox.configure(state="disabled")
            else:
                checkbox.configure(state="normal")
        cls.update_textbox()  # Update the text area after toggling



    @classmethod
    def get_selected_pairs(cls):
        if all_checkbox.get():
            return symbols
        else:
            return [pair for checkbox, pair in zip(checkboxes, symbols) if checkbox.get()]


class crypto_ui_groups(marketframe_store):

    @classmethod
    def crypto_ui(cls,  root, asset_type ):

        crypto_symbols = [
            "BTC-USD", "ETH-USD", "USDT-USD", "BNB-USD", "SOL-USD", "XRP-USD", "USDC-USD", "ADA-USD", "STETH-USD",
            "AVAX-USD", "DOGE-USD", "DOT-USD", "MATIC-USD", "WTRX-USD", "TRX-USD", "LINK-USD", "TON-USD",
            "WBTC-USD", "SHIB-USD", "LTC-USD", "DAI-USD", "WEOS-USD", "BCH-USD", "UNI-USD", "ICP-USD", "ATOM-USD",
            "LEO-USD", "XLM-USD", "NEAR-USD", "OKB-USD", "OP-USD", "ETC-USD", "APT-USD", "XMR-USD", "IMX-USD",
            "HBAR-USD", "INJ-USD", "WHBAR-USD", "FIL-USD",
            "KAS-USD", "VET-USD", "BXC-USD", "CRO-USD", "LDO-USD", "USDT-USD", "BTCB-USD", "STX-USD", "MNT-USD",
            "USDE-USD", "BSV-USD", "ARB-USD", "TIA-USD", "WBETH-USD", "EGLD-USD", "ALGO-USD", "RUNE-USD", "FDD-USD",
            "GRT-USD", "RNDR-USD", "BTT-USD", "HNT-USD", "BUSD-USD", "KCS-USD", "XTZ-USD", "WEMIX-USD", "FTT-USD",
            "MANA-USD", "NEO-USD", "KAVA-USD", "EOS-USD", "HEX-USD", "BONK-USD", "IOTA-USD", "BEAM-USD", "ROSE-USD",
            "CAKE-USD", "SUI-USD", "GALA-USD", "LUNC-USD", "KLAY-USD", "CHEEL-USD", "BGB-USD", "OSMO-USD",
            "XDC-USD", "WOO-USD"
        ]

        names = [
            "Bitcoin USD", "Ethereum USD", "Tether USD", "BNB USD", "Solana USD", "XRP USD",
            "USD Coin USD", "Cardano USD", "Lido Staked ETH USD", "Avalanche USD", "Dogecoin USD", "Polkadot USD",
            "Polygon USD", "Wrapped TRON USD", "TRON USD", "Chainlink USD", "Toncoin USD", "Wrapped Bitcoin USD",
            "Shiba Inu USD", "Litecoin USD", "Dai USD", "Wrapped EOS USD", "Bitcoin Cash USD", "Uniswap USD",
            "Internet Computer USD", "Cosmos USD", "UNUS SED LEO USD", "Stellar USD", "NEAR Protocol USD",
            "OKB USD", "Optimism USD", "Ethereum Classic USD", "Aptos USD", "Monero USD", "Immutable USD",
            "Hedera USD", "Injective USD", "Wrapped HBAR USD", "Filecoin USD", "Kaspa USD", "VeChain USD",
            "Bitcoin Classic USD", "Cronos USD", "Lido DAO USD", "TrueUSD USD", "Bitcoin BEP2 USD", "Stacks USD",
            "Mantle USD", "Energi Dollar USD", "Bitcoin SV USD", "Arbitrum USD", "Celestia USD",
            "Wrapped Beacon ETH USD", "MultiversX USD", "Algorand USD", "THORChain USD", "First Digital USD USD",
            "The Graph USD", "Render USD", "BitTorrent(New) USD", "Helium USD", "BUSD USD", "KuCoin Token USD",
            "Tezos USD", "WEMIX USD", "FTX Token USD", "Decentraland USD", "Neo USD", "Kava USD", "EOS USD",
            "HEX USD", "Bonk USD", "IOTA USD", "Beam USD", "Oasis Network USD", "PancakeSwap USD", "Sui USD",
            "Gala USD", "Terra Classic USD", "Klaytn USD", "Cheelee USD", "Bitget Token USD", "Osmosis USD",
            "XDC Network USD", "WOO Network USD"
        ]
        global  symbols
        symbols = crypto_symbols

        pass
        cls.chart_tab(root, row=1)
        # cls.chart_tab(root)
        pass
        cls.symbols_name_checkbox_crypto(root, symbols=symbols, row=1, names=names)
        cls.indicators_strategy_tab(root, row=1)

        cls.buy_signal_textbox(root, row=0, column=3)
        cls.sell_signal_textbox(root, row=0, column=2)

        if cls.asset_state["asset_type"][f"{asset_type}"]["asset_last_state"] == False:
            cls.set_crypto_default_args()

        if cls.asset_state["asset_type"][f"{asset_type}"]["asset_last_state"] == True:
            cls.retrieve_asset_state(root, asset_type="crypto")


        signal_button = ctk.CTkButton(root, text="Get Signal", height=22, width=122, command=cls.run_get_signal_indices_crypto )
        signal_button.grid(row=4, column=0, columnspan=3, padx=(2, 2), pady=(10, 1))
        signal_button.configure(text_color="#39FF14", fg_color="black")

        try_again_button = ctk.CTkButton(root, text="Try Again", height=22, width=122, command=cls.run_try_again_indices_crypto )
        try_again_button.grid(row=4, column=1, columnspan=3, padx=(2, 2), pady=(10, 1))
        try_again_button.configure(text_color="#39FF14", fg_color="black")

        save_button = ctk.CTkButton(root, text="SAVE", height=22, width=122, command=cls.run_reset_app)
        save_button.grid(row=4, column=2, columnspan=3, padx=(2, 2), pady=(10, 1))
        save_button.configure(text_color="#39FF14", fg_color="black")

        reset_button = ctk.CTkButton(root, text="RESET", height=22, width=122, command=cls.run_reset_app)
        reset_button.grid(row=4, column=4, columnspan=3, padx=(2, 2), pady=(10, 1))
        reset_button.configure(text_color="red", fg_color="black")

        cls.show_hide_output_log(root)



        cls.asset_state["asset_type"][f"{asset_type}"]["asset_last_state"] = True



class indices_ui_groups(marketframe_store):

        @classmethod
        def indices_ui(cls, root, asset_type ):



            commodities = ["GC=F"]
            indices = [ "GC=F", "^IXIC", "^GSPC", "^DJI", "^NYA", "^VIX", "^N100", "^DJI", "^FTSE", "^N225", "^BFX", "^STOXX50E",
                       "^HSI", "^GDAXI", "^FCHI", "^RUT"]

            indices_name = ["GOLD", "Nasdaq", "S&P 500", "DOW jones", "NYSE", "CBOE Volatility Index", "Euronext 100 Index",
                            "UK100", "Nikkei Osaka",
                            "^BFX Brussel", "Zurich", "EURO STOXX 50 Index", "Hong kong", "Germany index",
                            "CAC 40 Index", "Russell 2000"]

            # Nasdaq , S&P 500,  DOW jones, NYSE, CBOE Volatility Index,  DOW Jones , UK100 ,  Nikkei Osaka , ^BFX Brussel, Zurich, Hong kong, Germany index
            #  , Paris , Russell 2000
            global  symbols


            symbols = indices

            # Create a "Run" button



            signal_button = ctk.CTkButton(root, text="Get Signal", height=22, width=122, command=cls.run_get_signal_indices_crypto )
            signal_button.grid(row=4, column=0, columnspan=3, padx=(2, 2), pady=(10, 1))
            signal_button.configure(text_color="#39FF14", fg_color="black")

            try_again_button = ctk.CTkButton(root, text="Try Again", height=22, width=122, command=cls.run_try_again_indices_crypto)
            try_again_button.grid(row=4, column=1, columnspan=3, padx=(2, 2), pady=(10, 1))
            try_again_button.configure(text_color="#39FF14", fg_color="black")

            save_button = ctk.CTkButton(root, text="SAVE", height=22, width=122, command=cls.run_reset_app)
            save_button.grid(row=4, column=2, columnspan=3, padx=(2, 2), pady=(10, 1))
            save_button.configure(text_color="#39FF14", fg_color="black")

            reset_button = ctk.CTkButton(root, text="RESET", height=22, width=122, command=cls.run_reset_app)
            reset_button.grid(row=4, column=4, columnspan=3, padx=(2, 2), pady=(10, 1))
            reset_button.configure(text_color="red", fg_color="black")
            cls.symbols_name_checkbox(root, symbols=symbols, row=1, names=indices_name)
            pass
            cls.chart_tab(root, row=1)
            # cls.chart_tab(root)
            pass

            cls.indicators_strategy_tab(root, row=1)

            cls.buy_signal_textbox(root, row=0, column=3)
            cls.sell_signal_textbox(root, row=0, column=2)

            if cls.asset_state["asset_type"][f"{asset_type}"]["asset_last_state"] == False:

                cls.set_crypto_default_args()

            if cls.asset_state["asset_type"][f"{asset_type}"]["asset_last_state"] == True:
                cls.retrieve_asset_state(root, asset_type="indices")

            cls.show_hide_output_log(root)
            cls.asset_state["asset_type"][f"{asset_type}"]["asset_last_state"] = True



