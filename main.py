import customtkinter as ctk
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image
import openpyxl


def load_data():
    path = ".\\plants.xlsx"
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    
    list_values = list(sheet.values)
    headers = list_values[0]
    plant_data = list_values[1:]

    return headers, plant_data


def display_plant_data(headers, plant_data):
    if active_button == calendar_button:
        return      # do nothing on calendar page for now

    for widget in content_frame.winfo_children():
        widget.destroy()

    row_number = 0
    for plant in plant_data:
        if (plant[5] == 0 and active_button == mine_button) or (plant[5] == 1 and active_button == others_button):
            border_frame = ctk.CTkFrame(content_frame, fg_color="#D3D3D3", width=220, height=205)
            border_frame.grid(row=row_number, column=0, sticky="ew", padx=(75, 95), pady=(5, 0))
            
            plant_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF")
            plant_frame.grid(row=row_number, column=0, sticky="ew", padx=(70, 100), pady=5)

            # image of plant
            plant_img = ctk.CTkImage(light_image=Image.open(f"images\\{plant[0]}"),
                                    dark_image=Image.open(f"images\\{plant[0]}"),
                                    size=(150, 150))

            plant_label_img = ctk.CTkLabel(plant_frame, image=plant_img, text="")
            plant_label_img.grid(row=0, column=0, rowspan=5, padx=50, pady=25, sticky="n")

            details = [
                f"{plant[1]}",
                f"{headers[3]}: {plant[3]}",
                "Következő öntözés: ",
                f"{headers[4]}: {plant[4]}",
            ]

            # defining font styles for details
            font_bigger_bold = tkfont.Font(family="Istok Web", size=22, weight="bold")
            font_bold = tkfont.Font(family="Istok Web", size=18, weight="bold")
            font_regular = tkfont.Font(family="Istok Web", size=18, weight="normal")

            # applying font styles
            label_styles = [
                font_bigger_bold,   # name
                font_regular,       # watered
                font_bold,          # next watering
                font_regular        # needed light
            ]

            for i, (detail, style) in enumerate(zip(details, label_styles)):
                pady_value = 0
                font_color = "#000000"
                if i == 0:  # above name
                    pady_value = (20, 0)
                    font_color = "#0A4714"
                elif i == len(details) - 1: # below light
                    pady_value = (0, 10)
                else:   # between details
                    pady_value = (0, 0)

                tk.Label(plant_frame, text=detail, font=style, bg="#FFFFFF", fg=font_color).grid(
                            row=i, column=1, sticky="w", padx=5, pady=pady_value)

            row_number +=1


class CustomCTkButton(ctk.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_fg_color = "#FFFFFF"  # default color when inactive (white)
        self.active_color = "#C7F1CE"      # color when active or hovered (light green)
        self.calendar_color = "#05240A"    # color for calendar button (dark green)

        # button appearence config
        self.configure(
            fg_color=self.default_fg_color,
            border_width=0,
            corner_radius=0,
            text_color="#000000",
            font=("Istok Web", 32, "bold"),
            command=self.on_click
        )
        # events for hover
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress>", self.on_press)
        self.bind("<ButtonRelease>", self.on_release)

    def on_hover(self, event):
        self.configure(
            fg_color=self.active_color,
            border_color=self.active_color
        )

    def on_leave(self, event):
        if self == active_button:
            self.configure(fg_color=self.active_color)  # keep color for active button
        elif self == calendar_button:
            self.configure(fg_color=self.calendar_color)  # keep calendar button color (dark green)
        else:
            self.configure(fg_color=self.default_fg_color)  # keep default button color (white)

    def on_release(self, event):
        if self == active_button:
            self.configure(fg_color=self.active_color)  # keep color for active button
        elif self == calendar_button:
            self.configure(fg_color=self.calendar_color)  # keep calendar button color (dark green)
        else:
            self.configure(fg_color=self.default_fg_color)  # keep default button color (white)

    def on_click(self):
        # set as active
        self.configure(fg_color=self.active_color)
        set_active_button(self)

    def on_press(self, event):
        # set to active color
        self.configure(fg_color=self.active_color)

    def set_active(self):
        # set to active color
        self.configure(fg_color=self.active_color)

    def set_inactive(self):
        if self == calendar_button:
            self.configure(fg_color=self.calendar_color)  # set color for calendar button
        else:
            self.configure(fg_color=self.default_fg_color)  # set color for other buttons


def set_active_button(button):
    global active_button
    for btn in [mine_button, others_button, calendar_button]:
        if btn == button:
            btn.set_active()
        else:
            btn.set_inactive()
    active_button = button  # update active button
    
    # clear content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # update the content based on active button
    if active_button in [mine_button, others_button]:
        headers, plant_data = load_data()
        display_plant_data(headers, plant_data)
    else:
        update_content(active_button)


def update_content(button):
    if button == calendar_button:
        if content_label:   # if label exists
            content_label.config(text="This is the content for the calendar button.")
    else:
        if content_label:
            content_label.config(text="")   # clear label for displaying plants


root = ctk.CTk()
root.title("Planty")

# retrieve screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height-80}+-8+0")

# main frame
main_frame = ctk.CTkFrame(root, fg_color="#C7F1CE")
main_frame.pack(fill="both", expand=True)

# frame for navigation buttons
nav_frame = ctk.CTkFrame(main_frame, fg_color="#C7F1CE", height=50)
nav_frame.grid(row=0, column=0, sticky="ew")

# calculate button sizes based on screen size
button_height_ratio = 114 / 1024
button_height = int(screen_height * button_height_ratio)

# set button widths
button_width_ratio = 640 / 1440
calendar_width_ratio = 160 / 1440

buttons_width = int(screen_width * button_width_ratio)
calendar_button_width = button_height  # make calendar button square

# navigation buttons
mine_button = CustomCTkButton(main_frame, text="Saját")
mine_button.grid(row=0, column=0, sticky="nsew")

others_button = CustomCTkButton(main_frame, text="Más")
others_button.grid(row=0, column=1, sticky="nsew")

calendar_icon = ctk.CTkImage(light_image=Image.open("images\\black_calendar.png"),
                                dark_image=Image.open("images\\white_calendar.png"),
                                size=(40, 40))

calendar_button = CustomCTkButton(main_frame, text="", image=calendar_icon, fg_color="#05240A")
calendar_button.grid(row=0, column=2, sticky="nsew")

# set sizes
mine_button.configure(height=button_height, width=buttons_width)
others_button.configure(height=button_height, width=buttons_width)
calendar_button.configure(height=calendar_button_width, width=calendar_button_width)  # ensure square dimensions

# content frame
content_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#C7F1CE")
content_frame.grid(row=1, column=0, sticky="nsew", columnspan=3)  # all 3 columns
content_frame.grid_rowconfigure(0, weight=1)
content_frame.grid_columnconfigure(0, weight=1)

# frame for button to add new plant
button_frame = ctk.CTkFrame(main_frame, fg_color="#C7F1CE", height=40)
button_frame.grid(row=2, column=0, sticky="nsew", columnspan=3)

# button for adding new plant
new_plant_button = ctk.CTkButton(button_frame, text="Új hozzáadása", fg_color="#05240A",
                                height=40, width=180, corner_radius=20, font=(("Istok Web", 14, "bold")))
new_plant_button.pack(expand=True, fill='y', pady=(0, 5))

# configure sizes for main frame and content frame
main_frame.grid_rowconfigure(1, weight=1)  # allow row 1 to expand
main_frame.grid_columnconfigure(0, weight=1)  # allow column 0 to expand

# content
content_label = tk.Label(content_frame, text="", font=("Istok Web", 24), bg="#C7F1CE", fg="#000000")
content_label.pack(expand=True, fill='both')

# initial button states
active_button = mine_button  # initially mine is active
set_active_button(mine_button)  # set to active

headers, plant_data = load_data()
display_plant_data(headers, plant_data)

root.mainloop()
