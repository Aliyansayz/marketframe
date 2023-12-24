import customtkinter as ctk


class forex_ui:
    # Function to update the text area based on selected checkboxes
    @classmethod
    def forex_ui(cls, root):

        global all_checkbox, forex_pairs, checkboxes, textbox

        forex_pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X"]
        # Number of columns for checkboxes
        columns = 4

        # Create an "All Symbols" checkbox
        all_checkbox = ctk.CTkCheckBox(root, text="All Symbols")
        all_checkbox.configure(command=cls.toggle_checkboxes)
        all_checkbox.grid(row=len(forex_pairs) // columns + 1, columnspan=columns,
                          sticky="w")  # Use grid for "All Symbols" checkbox

        textbox = ctk.CTkTextbox(root, width=250)
        textbox.grid(row=len(forex_pairs) // columns + 2, columnspan=columns)  # Use grid for text area

        checkboxes = []

        for i, pair in enumerate(forex_pairs):
            row = i // columns
            col = i % columns
            checkbox = ctk.CTkCheckBox(root, text=forex_pairs[i][:6])
            checkbox.configure(command=lambda pair=pair: cls.update_textbox())
            checkboxes.append(checkbox)
            checkbox.grid(row=row, column=col, sticky="w")  # Use grid for checkboxes

        # Create the text area

        # Create a "Run" button
        run_button = ctk.CTkButton(root, text="Run", command=cls.fetch_and_update_data)
        run_button.grid(row=len(forex_pairs) // columns + 3, columnspan=columns)

        pass

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
                    values_text += checkbox.cget("text") + "\n"
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
    # if selected_pairs:
    #     pass
    #     print(selected_pairs)
        # ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X']
    @classmethod
    def get_selected_pairs(cls):
        if all_checkbox.get():
            return forex_pairs
        else:
            return [pair for checkbox, pair in zip(checkboxes, forex_pairs) if checkbox.get()]
