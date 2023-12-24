import customtkinter as ctk



class forex_ui_groups :
    # Function to update the text area based on selected checkboxes
    @classmethod
    def forex_ui(cls, root):

        global all_checkbox, forex_pairs, checkboxes, textbox


        forex_pairs = [
        'AUDCAD=X', 'AUDCHF=X', 'AUDJPY=X', 'AUDNZD=X', 'AUDUSD=X',
        'CADCHF=X','CADJPY=X' ,
        'CHFJPY=X',
        'EURAUD=X', 'EURCAD=X', 'EURCHF=X', 'EURGBP=X', 'EURJPY=X', 'EURNZD=X', 'EURUSD=X',
        'GBPAUD=X', 'GBPCAD=X', 'GBPCHF=X', 'GBPJPY=X', 'GBPUSD=X',  'GBPNZD=X',
        'NZDCAD=X', 'NZDCHF=X', 'NZDJPY=X', 'NZDUSD=X',
        'USDCHF=X', 'USDCAD=X', 'USDJPY=X'
    ]
        # Number of columns for checkboxes
        columns = 4

          # Placed first
        textbox = ctk.CTkTextbox(root, width=250)
        textbox.grid(row=0, column=4, sticky="nsew")  # Placed to the right

        scrollable_frame = ctk.CTkScrollableFrame(root, label_text="Available Symbols List")
        scrollable_frame.grid(row=1, column=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        scrollable_frame.grid_columnconfigure(0, weight=2)

        # Create an "All Symbols" checkbox
        all_checkbox = ctk.CTkCheckBox(master=scrollable_frame, text="All Symbols")
        all_checkbox.configure(command=cls.toggle_checkboxes)
        all_checkbox.grid(row=0, columnspan=columns, sticky="w")
        # all_checkbox.grid(row=len(forex_pairs) // columns + 1, columnspan=columns,
        #                   sticky="w")  # Use grid for "All Symbols" checkbox

        # Create the text box
        # textbox.grid(row=len(forex_pairs) // columns + 2, columnspan=columns)  # Use grid for text area

        checkboxes = []
        for i, pair in enumerate(forex_pairs):
            row = i  + 1
            col = 0
            checkbox = ctk.CTkCheckBox(master=scrollable_frame, text=forex_pairs[i][:6])
            checkbox.configure(command=lambda pair=pair: cls.update_textbox())
            checkboxes.append(checkbox)
            checkbox.grid(row=row, column=col, sticky="nw")  # Use grid for checkboxes


        # Create a "Run" button
        save_button = ctk.CTkButton(root, text="SAVE", width=70, command=cls.fetch_and_update_data)

        save_button.grid(row=4, column=1  , columnspan=3)

        import_button = ctk.CTkButton(root, text="IMPORT", width=70, command=cls.fetch_and_update_data)

        import_button.grid(row=4, column=0, columnspan=3)

        pass
        cls.chart_tab(root)
        # cls.chart_tab(root)
        pass
        cls.indicators_strategy(root)
        #
        #

        # option_last_candles.set("14")
        # menu_atr_multiplier.set("1.7")
        # menu_atr_period.set("5")
        # menu_adx_period.set("10")
        # menu_lower_ema.set("5")
        # menu_higher_ema.set("20")
         # label_tab_2 = ctk.CTkLabel(master=tabview.tab(timezone_tab), text="CTkLabel on Tab 2")
        # label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # placeholder_period = "Select Period Lookback..."  # Placeholder text
        # option_menu_period = ctk.CTkComboBox(master=tabview.tab(indicators_tab),
        #                                      values=[placeholder_period, "7d", "1d"])
        # option_menu_period.grid(row=0, column=0, padx=0, pady=(10, 10))
        # option_menu_period.configure(command=cls.toggle_timeframes)
        # option_menu_period.set("14")
        #
        # option_menu_period.bind("<<ComboboxSelected>>", lambda event: option_menu_period.set("")
        #                     if option_menu_period.get() == placeholder_period else None)
        #
        #
        # # switch_ha.select()
        # # switch_ha.configue()
        # print(switch_ha.get())
        # if switch_ha.get() == 1 : print(True)

        # entry = ctk.CTkEntry(master=tabview.tab("CTkTabview"), placeholder_text="Time value")
        # entry.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # string_input_button = customtkinter.CTkButton(master=tabview.tab("CTkTabview"), text="Open CTkInputDialog",
        #                                                    command=self.open_input_dialog_event)
        # string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
    @classmethod
    def indicators_strategy(cls, root):

        global menu_strategy, option_last_candles, cross_only_check, menu_lower_ema, \
            menu_higher_ema, menu_atr_period, menu_adx_period, menu_atr_multiplier, switch_ha

        tabview = ctk.CTkTabview(root, width=250)
        tabview.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        indicators_tab, strategy_tab, indicators_tab = "Indicators", "Strategy", "Indicators"
        tabview.add(indicators_tab)
        tabview.add(strategy_tab)
        tabview.tab(indicators_tab).grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        tabview.tab(strategy_tab).grid_columnconfigure(0, weight=1)

        button = ctk.CTkButton(tabview, text="GET SIGNALS", command=lambda: print(1))
        button.grid(row=9, column=0, padx=7, pady=7)
        scrollable_tab_indicator = ctk.CTkScrollableFrame(master=tabview.tab(indicators_tab),
                                                          label_text="Indicators Input")
        scrollable_tab_indicator.grid(row=0, column=4, padx=(7, 7), pady=(5, 5), sticky="nsew")

        scrollable_tab_strategy = ctk.CTkScrollableFrame(master=tabview.tab(strategy_tab),
                                                         label_text="Define Strategy")
        scrollable_tab_strategy.grid(row=0, column=4, padx=(7, 7), pady=(5, 5), sticky="nsew")

        placeholder_hour = "Select Hour Chart..."
        label_ema = ctk.CTkLabel(master=scrollable_tab_indicator, text="Lower/Higher EMA")
        label_ema.grid(row=0, column=0, padx=20, pady=(10, 10))

        lower_ema, higher_ema = "Type Lower EMA", "Type Higher EMA"
        menu_lower_ema = ctk.CTkComboBox(master=scrollable_tab_indicator,
                                         values=[lower_ema, "5", "7", "9"])
        menu_higher_ema = ctk.CTkComboBox(master=scrollable_tab_indicator,
                                          values=[higher_ema, "20", "21", "34"])

        menu_lower_ema.grid(row=1, column=0, padx=20, pady=(10, 10))
        menu_higher_ema.grid(row=2, column=0, padx=20, pady=(10, 10))
        # .grid_forget()

        label_atr = ctk.CTkLabel(master=scrollable_tab_indicator, text="ATR Period With Multiplier")
        label_atr.grid(row=3, column=0, padx=20, pady=(10, 10))

        atr_text, adx_text = "Type ATR Period", "Type ADX Period"
        menu_atr_period = ctk.CTkComboBox(master=scrollable_tab_indicator,
                                          values=[atr_text, "5", "7", "3"])
        menu_atr_period.grid(row=4, column=0, padx=20, pady=(10, 10))

        placeholder_atr = "Select ATR Multiplier..."
        menu_atr_multiplier = ctk.CTkComboBox(master=scrollable_tab_indicator,
                                              values=["1.7", placeholder_atr, "2.0", "3.0", "1.9", "1.8"])
        menu_atr_multiplier.grid(row=5, column=0, padx=20, pady=(10, 10))

        menu_adx_period = ctk.CTkComboBox(master=scrollable_tab_indicator,
                                          values=[adx_text, "8", "10", "14"])
        label_adx = ctk.CTkLabel(master=scrollable_tab_indicator, text="ADX Period")
        label_adx.grid(row=6, column=0, padx=20, pady=(10, 10))

        menu_adx_period.grid(row=7, column=0, padx=20, pady=(10, 10))

        switch_ha = ctk.CTkSwitch(master=scrollable_tab_indicator, text="Switch To Heikin Ashi ")
        switch_ha.grid(row=8, column=0, padx=10, pady=(0, 20))
        switch_ha.select()

        placeholder_strategy = "Select Your Strategy Type..."  # Placeholder text

        menu_strategy = ctk.CTkOptionMenu(master=scrollable_tab_strategy,
                                          values=[placeholder_strategy, "stochastic", "ema_crossover", "both"])
        menu_strategy.grid(row=0, column=0, padx=0, pady=(10, 10))
        # option_menu_strategy.configure(command=cls.select_strategy)

        placeholder_last_candles = "Select Last Candles To Filter..."
        option_last_candles = ctk.CTkComboBox(master=scrollable_tab_strategy,
                                              values=[placeholder_last_candles, "15", "30"])
        option_last_candles.grid(row=1, column=0, padx=20, pady=(10, 10))

        cross_only_check = ctk.CTkCheckBox(master=scrollable_tab_strategy, text="Cross Check Only")
        cross_only_check.grid(row=2, column=0, padx=20, pady=(10, 10))

        option_last_candles.set("14")
        menu_atr_multiplier.set("1.7")
        menu_atr_period.set("5")
        menu_adx_period.set("10")
        menu_lower_ema.set("5")
        menu_higher_ema.set("20")

    @classmethod
    def select_strategy(*args):

        smi_buy, smi_sell = None , None
        ema_buy, ema_sell = None , None
        # if  == "both"
        # elif  ==  "stochastic"
        # elif  == "ema_crossover"
        pass

    @classmethod
    def get_indicators_args(cls):
        if  switch_ha.get() == 1 : ha_ohlc = True
        else :    ha_ohlc = False



    @classmethod
    def chart_tab(cls, root):

        global combobox_step, option_menu_timeframe, option_menu_minute, \
        option_menu_hour, option_menu_period, option_menu_timezone

        tabview = ctk.CTkTabview(root, width=250)
        tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        tab_chart, timezone_tab = "Chart", "Timezone"
        tabview.add(tab_chart)
        tabview.add(timezone_tab)
        tabview.tab(tab_chart).grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        placeholder_timeframe = "Select Timeframe Type..."  # Placeholder text

        option_menu_timeframe = ctk.CTkOptionMenu(master=tabview.tab(tab_chart),
                                                 values=[placeholder_timeframe, "Hour", "Minute"])
        option_menu_timeframe.grid(row=0, column=0, padx=0, pady=(10, 10))
        option_menu_timeframe.configure(command=cls.toggle_timeframes)

        option_menu_timeframe.bind("<<ComboboxSelected>>", lambda event: option_menu_timeframe.set("")
        if option_menu_timeframe.get() == placeholder_timeframe else None)

        placeholder_minute = "Select Minute Chart..."
        option_menu_minute = ctk.CTkOptionMenu(master=tabview.tab(tab_chart),
                                              values=[placeholder_minute, "15", "30"])
        option_menu_minute.grid(row=1, column=0, padx=20, pady=(10, 10))
        option_menu_minute.bind("<<ComboboxSelected>>", lambda event: option_menu_minute.set("")
        if option_menu_minute.get() == placeholder_minute else None)

        placeholder_hour = "Select Hour Chart..."
        option_menu_hour = ctk.CTkOptionMenu(master=tabview.tab(tab_chart),
                                            values=[placeholder_hour, "1Hour", "4Hour", "Day"])
        option_menu_hour.grid(row=2, column=0, padx=20, pady=(10, 10))
        option_menu_hour.bind("<<ComboboxSelected>>", lambda event: option_menu_hour.set("")
        if option_menu_hour.get() == placeholder_hour else None)
        # .grid_forget()

        placeholder_step = "Select Step Value..."
        combobox_step = ctk.CTkComboBox(master=tabview.tab(tab_chart),
                                        values=["1", placeholder_step, "2", "3", "4", "5"])
        combobox_step.grid(row=3, column=0, padx=20, pady=(10, 10))
        combobox_step.bind("<<ComboboxSelected>>", lambda event: combobox_step.set("1")
        if combobox_step.get() == placeholder_step else None)

        # label_tab_2 = ctk.CTkLabel(master=tabview.tab(timezone_tab), text="CTkLabel on Tab 2")
        # label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        placeholder_period = "Select Period Lookback..."  # Placeholder text
        option_menu_period = ctk.CTkComboBox(master=tabview.tab(timezone_tab),
                                                values=[placeholder_period, "7d", "1d"])
        option_menu_period.grid(row=0, column=0, padx=0, pady=(10, 10))
        option_menu_period.configure(command=cls.toggle_timeframes)
        option_menu_period.set("7d")

        option_menu_period.bind("<<ComboboxSelected>>", lambda event: option_menu_period.set("")
        if option_menu_period.get() == placeholder_period else None)

        placeholder_timezone =  "Select Timezone Type.."
        option_menu_timezone = ctk.CTkOptionMenu(master=tabview.tab(timezone_tab),
                                                values=[placeholder_timezone, "gmt", "pkt"])
        option_menu_timezone.grid(row=1, column=0, padx=0, pady=(10, 10))
        option_menu_timezone.configure(command=cls.toggle_timeframes)
        option_menu_timezone.set("pkt")

        option_menu_timezone.bind("<<ComboboxSelected>>", lambda event: option_menu_timezone.set("pkt")
                            if option_menu_timezone.get() == placeholder_timezone else None)

    @classmethod
    def get_data_args(cls):

        chart = str(option_menu_hour.get()[:2])
        if option_menu_timeframe.get() == "Hour":
            chart = str(option_menu_hour.get()[:2])

        elif option_menu_timeframe.get() == "Minute":
            chart = str(option_menu_minute.get()[:2])

        interval = chart
        step = int(combobox_step.get())
        chart_type = str(int(int(chart[0]) * step)) + str(f"{chart[-1]}")
        selected_symbols = cls.get_selected_pairs()

        timezone = str(option_menu_timezone.get())

        return selected_symbols, interval, timezone, chart_type

    @classmethod
    def toggle_timeframes(*args):
        if option_menu_timeframe.get() =="Minute":
            # print("Minute True")
            option_menu_hour.configure(state="disabled")
                # .configure(state="disabled")
            option_menu_minute.configure(state="normal")

        elif option_menu_timeframe.get() =="Hour":
            # print("Hour True")
            option_menu_minute.configure(state="disabled")
            option_menu_hour.configure(state="normal")
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
            values_text = "\n".join(forex_pairs)
        else:
            # Otherwise, show only selected pairs
            for checkbox in checkboxes:
                if checkbox.get():
                    values_text += checkbox.cget("text") + "=X\n" #Added "=X" for
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
    def fetch_and_update_data(cls):

        selected_pairs = cls.get_selected_pairs()
        if selected_pairs:
        #     # pass
            print(selected_pairs)
        # ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X']
    @classmethod
    def get_selected_pairs(cls):
        if all_checkbox.get():
            return forex_pairs
        else:
            return [pair for checkbox, pair in zip(checkboxes, forex_pairs) if checkbox.get()]

