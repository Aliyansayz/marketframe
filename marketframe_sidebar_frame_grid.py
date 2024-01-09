import customtkinter as ctk
from marketframe_ui import  forex_ui_groups , crypto_ui_groups, indices_ui_groups
from marketframe_ui import ui_store , marketframe_store

# ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"


# kashmir fg_color=("#614385" , "#516395") ugly blue sky



class app_frame_store(marketframe_store):

    @classmethod
    def sidebar(cls, root):
        global  sidebar
        side_button_colors = [["#eacda3 ", "#d6ae7b"], ["#aa076b", "#61045f"]]  # wood, violet like
        # Create the sidebar
        sidebar = ctk.CTkFrame(root, width=140, corner_radius=0, fg_color="black")
        sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        sidebar.grid_rowconfigure(4, weight=1)
        cls.sidebar_button(sidebar)

    @classmethod
    def sidebar_button(cls, root):
        side_button_colors = ["#6B5B95", "#45B8AC", "#DD4124", "#009B77",
                              "#45B8AC"]  # Ultra Violet, Mimosa #EFC050,Tangerine Tango,  Emerald
        side_button_text_colors = ["#39FF14", "#fe4005", "#04d9ff", "#FFDF00", "#6B5B95"]

        asset_type = ['FOREX', 'INDICES', 'CRYPTO', 'STOCKS']

        sidebar_buttons = []
        for i, asset in enumerate(asset_type):
            button = ctk.CTkButton(root, text=asset, width=120, height=35, font=ctk.CTkFont(size=15, weight="normal"),
                                   text_color="#39FF14"  # "#39FF14"
                                   , fg_color="black", hover_color="#AFA274", border_color="white")

            button.configure(hover_color="#1D5D99")#1D5D99")  # fg_color="lightblue", hover_color="lightgreen" )
            button.grid(row=i, column=0, padx=20, pady=(0, 10), sticky="nsew")
            sidebar_buttons.append(button)

        for i, button in enumerate(sidebar_buttons):
            asset = asset_type[i]

            button.bind("<Button-1>", lambda e, asset=asset: cls.switch_frame(asset))

    @classmethod
    def change_appearance_mode_event(cls, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    @classmethod
    def appearance_mode_button(cls, root):
        appearance_mode_label = ctk.CTkLabel(root, text="Appearance Mode:", anchor="w", )
        appearance_mode_label.grid(row=5, column=0, rowspan=4, padx=20, pady=(10, 0))
        appearance_mode_optionmenu = ctk.CTkOptionMenu(root, values=["Light", "Dark", "System"],
                                                       command=cls.change_appearance_mode_event)
        appearance_mode_optionmenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        appearance_mode_optionmenu.set("Dark")


class create_asset_frame(app_frame_store):

    @classmethod
    def create_frame(cls, root):
        global frame

        frame = ctk.CTkScrollableFrame(root)
        frame.grid_columnconfigure(1, weight=0)
        frame.grid_columnconfigure((2, 3), weight=0)
        frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)

        frame.grid(row=0, column=1, rowspan=4, padx=(7, 7), pady=(5, 5), sticky="nsew")

        return frame

    @classmethod
    def asset_frame(cls, frame, asset):

            # frame = ctk.CTkFrame(root)
            frame.title = asset


            print(cls.asset_state["asset_type"][cls.current_asset]["asset_last_state"])

            if asset=="FOREX":
                forex_ui_groups.forex_ui(frame, cls.current_asset )
                cls.previous_asset = str(asset).lower()

            elif asset=="CRYPTO":
                crypto_ui_groups.crypto_ui(frame, cls.current_asset )
                cls.previous_asset = str(asset).lower()

            elif asset == "INDICES":
                indices_ui_groups.indices_ui(frame, cls.current_asset )
                cls.previous_asset = str(asset).lower()

######################## Will Decide To Remove Asset Type From Dictionary OR Not
    @classmethod
    def switch_frame(cls, asset):

        if cls.asset_state["asset_type"][cls.previous_asset]["asset_last_state"] == True:
            cls.string_args, cls.num_args = cls.input_args()
            cls.store_asset_state(cls.previous_asset)

                 # store previous_asset state
        cls.current_asset = str(asset).lower()
        cls.asset_frame(frame, asset)



class run_app(create_asset_frame):

    @classmethod
    def run_app(cls):

        ctk.set_default_color_theme("blue")
        # Create the main window
        root = ctk.CTk()
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure((2, 3), weight=0)
        root.grid_rowconfigure((0, 1, 2), weight=1)
        root.geometry(f"{1100}x{580}")


        cls.sidebar(root)
        cls.appearance_mode_button( sidebar)
        frame = cls.create_frame(root)

        asset_type = ['FOREX', "CRYPTO", 'INDICES', 'STOCKS COMMODITIES']

        print(cls.current_asset)

        # cls.asset_frame(f"{asset_type[0]}", frame)

        root.mainloop()




def change_appearance_mode_event(new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)

run_app.run_app()

# appearance_mode_label = ctk.CTkLabel(sidebar, text="Appearance Mode:", anchor="w",  )
# appearance_mode_label.grid(row=5, column=0, rowspan=4, padx=20, pady=(10, 0))
# appearance_mode_optionmenu = ctk.CTkOptionMenu(sidebar, values=["Light", "Dark", "System"],
#                             command=change_appearance_mode_event)
# appearance_mode_optionmenu.grid(row=7, column=0, padx=20, pady=(10, 10))
# appearance_mode_optionmenu.set("Dark")

# sidebar2 = ctk.CTkFrame(root)
# sidebar2.grid(row=0, column=0, sticky="ns")
# Function to create a frame for a specific asset type
# create_asset_frame.asset_frame(f"{asset_type[0]}" )

# def switch_frame( asset):
#     global asset_frame
#     asset_frame.grid_forget()  # Hide the current frame
#     asset_frame = create_asset_frame(f"{asset}", lambda: print(f"Button clicked in Frame {asset}"))
#     asset_frame.grid(row=0, column=1, sticky="nsew")



# sidebar.pack(side="left", fill="y")
# side_button_colors = [  "#6B5B95", "#45B8AC" , "#DD4124", "#009B77", "#45B8AC" ]   # Ultra Violet, Mimosa #EFC050,Tangerine Tango,  Emerald
# side_button_text_colors = [ "#39FF14", "#fe4005", "#04d9ff", "#FFDF00", "#6B5B95" ]
#
# sidebar_buttons = []
# for i,asset in enumerate(asset_type):
#     button = ctk.CTkButton(sidebar, text=asset, width=120, height=35, font=ctk.CTkFont(size=15, weight="normal"), text_color=side_button_text_colors[2]  #"#39FF14"
#                            , fg_color="black", hover_color="#45B8AC", border_color= "white" )
#
#     button.configure(hover_color="#006792" )                       # fg_color="lightblue", hover_color="lightgreen" )
#     button.grid(row=i, column=0,  padx=20, pady=(0,10) , sticky="nsew" )
#     sidebar_buttons.append(button)
#
#
# for i, button in enumerate(sidebar_buttons):
#     asset = asset_type[i]
#     button.bind("<Button-1>", lambda e, asset=asset: switch_frame(asset))

