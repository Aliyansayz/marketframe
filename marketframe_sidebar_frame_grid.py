import customtkinter as ctk
from marketframe_ui import forex_ui


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")
# Create the main window


root = ctk.CTk()
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=1)

root.geometry(f"{1100}x{580}")


# Create the sidebar
sidebar = ctk.CTkFrame(root, width=140, corner_radius=0)
sidebar.grid(row=2, column=0, rowspan=4, sticky="nsew")
sidebar.grid_rowconfigure(4, weight=1)


def create_asset_frame( asset, command =None):
    if asset:
        frame = ctk.CTkFrame(root)
        frame.grid(row=0, column=1, sticky="nsew")
        frame.title = asset

        # Customize the frame's content based on asset_type
        # (Add labels, buttons, data visualizations, etc.)
        label = ctk.CTkLabel(frame, text=f"Content for {asset}")
        label.grid(row=1, column=0, pady=20)

        if asset=="Forex":
            forex_ui.forex_ui(frame)

        # button = ctk.CTkButton(frame, text=f"{asset}", command=command)
        # button.grid(row=2, column=0, padx=20, pady=10)

        return frame


asset_type = ['Forex', 'Indices', 'Stocks', 'Metals']
asset_frame = create_asset_frame(f"{asset_type[0]}", lambda: print("Button clicked in Frame 1"))


def change_appearance_mode_event(self, new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)


appearance_mode_label = ctk.CTkLabel(sidebar, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
appearance_mode_optionemenu = ctk.CTkOptionMenu(sidebar, values=["Light", "Dark", "System"],
                            command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

# sidebar2 = ctk.CTkFrame(root)
# sidebar2.grid(row=0, column=0, sticky="ns")
# Function to create a frame for a specific asset type




def switch_frame( asset):
    global asset_frame
    asset_frame.pack_forget()  # Hide the current frame
    asset_frame = create_asset_frame(f"{asset}", lambda: print(f"Button clicked in Frame {asset}"))
    asset_frame.grid(row=0, column=1, sticky="nsew")






# sidebar.pack(side="left", fill="y")

sidebar_buttons = []
for i,asset in enumerate(asset_type):
    button = ctk.CTkButton(sidebar, text=asset)
    button.grid(row=i, column=0,  padx=20, pady=10)
    sidebar_buttons.append(button)


for i, button in enumerate(sidebar_buttons):
    asset = asset_type[i]
    button.bind("<Button-1>", lambda e, asset=asset: switch_frame(asset))

root.mainloop()