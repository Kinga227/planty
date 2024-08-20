import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

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
            font=("Istok Web", 40, "bold"),
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
    update_content(active_button)  # update content based on active button

def update_content(button):
    content = {
        mine_button: "This is the content for 'Saját'.",
        others_button: "This is the content for 'Más'.",
        calendar_button: "This is the content for the Calendar button."
    }
    content_label.config(text=content.get(button, ""))

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
nav_frame = ctk.CTkFrame(main_frame, fg_color="#C7F1CE")
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

calendar_icon = Image.open("images\\white_calendar.png")
calendar_icon = calendar_icon.resize((calendar_button_width - 10, button_height - 10), Image.Resampling.LANCZOS)
calendar_icon_photo = ImageTk.PhotoImage(calendar_icon)

calendar_button = CustomCTkButton(main_frame, text="", image=calendar_icon_photo, fg_color="#05240A")
calendar_button.grid(row=0, column=2, sticky="nsew")

# set sizes
mine_button.configure(height=button_height, width=buttons_width)
others_button.configure(height=button_height, width=buttons_width)
calendar_button.configure(height=calendar_button_width, width=calendar_button_width)  # ensure square dimensions

# content frame
content_frame = ctk.CTkFrame(main_frame, fg_color="#C7F1CE")
content_frame.grid(row=1, column=0, sticky="nsew", columnspan=3)  # all 3 columns
content_frame.grid_rowconfigure(0, weight=1)
content_frame.grid_columnconfigure(0, weight=1)

# configure sizes for main frame and content frame
main_frame.grid_rowconfigure(1, weight=1)  # allow row 1 to expand
main_frame.grid_columnconfigure(0, weight=1)  # allow column 0 to expand

# content
content_label = tk.Label(content_frame, text="", font=("Istok Web", 24), bg="#C7F1CE", fg="#000000")
content_label.pack(expand=True, fill='both')

# initial button states
active_button = mine_button  # initially mine is active
set_active_button(mine_button)  # set to active

root.mainloop()
