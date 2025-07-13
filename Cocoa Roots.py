import tkinter as tk
import tkinter.ttk as ttk
import pickle
from PIL import Image, ImageTk

# lists of classes and objects
# these lists are global
ingredients = []
batches = []
tickets = []

# global colours
RED = "#b3152a"
ORANGE = "#F6A482"
DARK_ORANGE = "#ed652d"
LIGHT_ORANGE = "#FEDBC7"
LIGHT_BLUE = "#D1E5F0"
DARK_BLUE = "#8EC4DE"
BACKGROUND = "#f5f0ed"
ERROR_GREEN = "#46f274"  # This colour should only be on hidden elements


# -----------------------------------------------------------------------------
# FUNCTIONALITY
# -----------------------------------------------------------------------------

class Ingredient:
    def __init__(self, name, weight, source):
        self.log = []  # list of every event occurred in ingredient
        self.ID = 1  # ingredient unique identifier
        self.name = name  # common name of batch
        self.weight = weight
        self.source = source  # name of ingredient suppler

    def reduce_amount(self, amount):
        calc_weight = self.weight - amount

        if calc_weight >= 0:  # range check
            self.weight = calc_weight

        elif calc_weight < 0:
            raise ValueError(f"There is only {self.weight} grams of this ingredient")


class Batch:
    def __init__(self, ID):
        self.log = []  # list of every event occurred in batch
        self.total_weight = 0
        self.ID = ID  # batch unique identifier

    def add_ingredient(self, date_time, ingredient, amount):
        ingredient.reduce_amount(amount)
        self.total_weight += amount

        record = {"process": "add_ingredient",
                  "ingredient": ingredient,
                  "amount": amount,
                  "date_time": date_time
                  }

        self.log.append(record)

    def fermentation(self, start_dt, end_dt, additive, amount):
        additive.reduce_amount(amount)

        duration = end_dt - start_dt

        record = {"process": "fermentation",
                  "ingredient": additive,
                  "amount": amount,
                  "start_dt": start_dt,
                  "end_dt": end_dt,
                  "duration": duration
                  }

        self.log.append(record)

    def drying(self, start_dt, end_dt, temperature):
        duration = end_dt - start_dt

        record = {"process": "drying",
                  "temperature": temperature,
                  "start_dt": start_dt,
                  "end_dt": end_dt,
                  "duration": duration
                  }

        self.log.append(record)

    def winnowing(self, date_time, weight_reduced):

        if weight_reduced > self.total_weight:  # range check
            raise ValueError("weight_reduced cannot be greater than total weight")

        record = {"process": "winnowing",
                  "weight_reduced": weight_reduced,
                  "date_time": date_time,
                  }

        self.log.append(record)

    def grinding(self, date_time, fineness):  # fineness in mm

        if fineness < 0:  # range check
            raise ValueError("fineness cannot be less than zero")

        record = {"process": "grinding",
                  "fineness": fineness,
                  "date_time": date_time,
                  }

        self.log.append(record)

    def conching(self, date_time, temperature):

        record = {"process": "conching",
                  "temperature": temperature,
                  "date_time": date_time,
                  }

        self.log.append(record)

    def tempering_molding(self, date_time, melting_temp, cooling_temp, working_temp, molding_dimension, weight_per_bar):

        record = {"process": "tempering_molding",
                  "melting_temp": melting_temp,
                  "cooling_temp": cooling_temp,
                  "working_temp": working_temp,
                  "molding_dimension": molding_dimension,
                  "weight_per_bar": weight_per_bar,
                  "date_time": date_time,
                  }

        self.log.append(record)

    def finalise(self, date_time, verification_num):

        record = {"process": "finalise",
                  "verification_num": verification_num,
                  "date_time": date_time,
                  }

        ...  # close ... write more

        self.log.append(record)

    def make_ticket(self):

        ...

    def save(self):
        ...


class Ticket:
    def __init__(self, ID):
        self.ID = ID

    def access_ticket(self):
        ...

    def save(self):
        ...


def load():
    ...


# -----------------------------------------------------------------------------
# GUI INTERFACE
# -----------------------------------------------------------------------------

# main tkinter setup
window = tk.Tk()
window.config(bg="blue")
window.geometry("400x600")  # window dimensions
window.title("Cocoa Roots")
window.grid_columnconfigure(1, weight=1)  # make expandable with screen
window.grid_rowconfigure(2, weight=1)

# Images
search_icon = ImageTk.PhotoImage(Image.open("Resources/Search_entry.png").resize((30, 30)))
logo = ImageTk.PhotoImage(Image.open("Resources/Bean_Logo.png"))

# titlebar
title_bar = tk.Frame(height=4, bg=ORANGE)
title_bar.grid(row=1, column=1, sticky="ew")

logo_label = tk.Label(title_bar, image=logo, bg=ORANGE)
logo_label.pack(side=tk.LEFT)

title_text = tk.Label(title_bar, text="Cocoa Roots", font=("Bernard MT Condensed", 25), bg=ORANGE)
title_text.pack(side=tk.LEFT)


class Content(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self, bg=BACKGROUND, height=20, borderwidth=1, relief="solid")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.back_track = {}
        self.back_button = tk.Button(title_bar,
                                     text="<",
                                     width=7,
                                     height=2,
                                     bg=LIGHT_ORANGE,
                                     borderwidth=1,
                                     relief="solid",
                                     command=lambda: self.go_back()
                                     )

        self.pages = {}  # dictionary of sub-frames within content

        for page in [UserPage, WorkerPage, ConsumerPage, IngredientPage]:  # for every page within content
            page_class = page(parent=self)  # create frame class

            self.pages[page] = page_class

            page_class.grid(row=1, column=1, sticky="nsew")

        self.current_page = UserPage
        self.switch_page(UserPage)

    def navigate(self, page_name):
        self.back_track[page_name] = self.current_page
        self.switch_page(page_name)

    def go_back(self):
        last_page = self.back_track[self.current_page]
        self.switch_page(last_page)

    def switch_page(self, page_name):
        if page_name in self.back_track:
            self.back_button.pack(padx=10, side=tk.RIGHT)
        else:
            self.back_button.pack_forget()

        self.current_page = page_name
        page = self.pages[page_name]
        page.tkraise()


class UserPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=BACKGROUND, height=20, borderwidth=1, relief="solid")
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

        worker_button = tk.Button(self,
                                  text="Worker",
                                  bg=LIGHT_BLUE,
                                  height=7,
                                  width=30,
                                  borderwidth=1,
                                  relief="solid",
                                  command=lambda: parent.navigate(WorkerPage)
                                  )
        worker_button.grid(row=1, column=1)

        consumer_button = tk.Button(self,
                                    text="Consumer",
                                    bg=LIGHT_BLUE,
                                    height=7,
                                    width=30,
                                    borderwidth=1,
                                    relief="solid",
                                    command=lambda: parent.navigate(ConsumerPage)
                                    )
        consumer_button.grid(row=2, column=1)


class WorkerPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=20, borderwidth=1, relief="solid")
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=4)

        self.grid_columnconfigure(1, weight=1)

        # __________ Ingredient Frame __________
        ingredient_frame = tk.Frame(self,
                                    bg=LIGHT_BLUE,
                                    height=50,
                                    width=50,
                                    borderwidth=1,
                                    relief="solid"
                                    )
        ingredient_frame.grid(row=1, column=1, padx=15, sticky="we")

        ingredient_frame.grid_propagate(False)
        ingredient_frame.rowconfigure(1, weight=1)
        ingredient_frame.columnconfigure(1, weight=1)

        ingredient_label = tk.Label(ingredient_frame,
                                    bg=LIGHT_BLUE,
                                    text="Add Ingredient"
                                    )
        ingredient_label.grid(row=1, column=1, sticky="w", padx=5)

        ingredient_button = tk.Button(ingredient_frame,
                                      bg=LIGHT_ORANGE,
                                      text="+",
                                      font=("Calabi", 12),
                                      padx=5,
                                      command=lambda: parent.navigate(IngredientPage)
                                      )
        ingredient_button.grid(row=1, column=2, sticky="e", padx=5)

        # __________ Batches Frame __________
        batches_frame = tk.Frame(self,
                                 bg=LIGHT_BLUE,
                                 height=50,
                                 width=50,
                                 borderwidth=1,
                                 relief="solid"
                                 )
        batches_frame.grid(row=2, column=1, padx=15, sticky="nwe")

        batches_frame.grid_propagate(False)
        batches_frame.rowconfigure(1, weight=1)
        batches_frame.columnconfigure(1, weight=1)

        batches_label = tk.Label(batches_frame,
                                 bg=LIGHT_BLUE,
                                 text="Add Batch"
                                 )
        batches_label.grid(row=1, column=1, sticky="w", padx=5)

        batches_button = tk.Button(batches_frame,
                                   bg=LIGHT_ORANGE,
                                   text="+",
                                   font=("Calabi", 12),
                                   padx=5,
                                   command=self.add_ingredient
                                   )
        batches_button.grid(row=1, column=2, sticky="e", padx=5)

    def add_ingredient(self):
        print("hello", self.info)


class ConsumerPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=20, borderwidth=1, relief="solid")
        self.grid_columnconfigure(1, weight=1)

        search_background = tk.Frame(self, bg=LIGHT_ORANGE, borderwidth=1, relief="solid")
        search_background.grid(row=1, column=1, pady=20, ipady=5, padx=(15, 50), sticky="we")
        search_background.grid_columnconfigure(1, weight=1)

        search_bar = tk.Entry(search_background,
                              borderwidth=1,
                              relief="solid",
                              font=("Calabi", 12)
                              )
        search_bar.grid(row=1, column=1, pady=(10, 0), ipady=7, padx=20, sticky="we")

        search_button = tk.Button(search_background,
                                  image=search_icon,
                                  bg=LIGHT_ORANGE,
                                  height=25,
                                  borderwidth=1,
                                  relief="ridge",
                                  command=self.search
                                  )
        search_button.grid(row=1, column=2, padx=(0, 20), pady=(10, 0), ipady=3)

    def search(self):
        print("search", self.info)


class IngredientPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=20, borderwidth=1, relief="solid")
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=4)

        self.grid_columnconfigure(1, weight=1)

        # __________ Page Title __________
        title_frame = tk.Frame(self,
                               bg=LIGHT_BLUE,
                               height=50,
                               width=50,
                               borderwidth=1,
                               relief="solid"
                               )
        title_frame.grid(row=1, column=1, padx=15, sticky="we")

        title_frame.grid_propagate(False)
        title_frame.rowconfigure(1, weight=1)
        title_frame.columnconfigure(1, weight=1)

        title_label = tk.Label(title_frame,
                               bg=LIGHT_BLUE,
                               text="Add Ingredient"
                               )
        title_label.grid(row=1, column=1)

        # __________ Page Content __________
        content_frame = tk.Frame(self, width=200, height=200)
        content_frame.grid(column=1, row=2, sticky="nesw")

        content_frame.grid_propagate(False)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_rowconfigure(2, weight=2)

        content_frame.grid_columnconfigure(2, weight=1)

        name_label = tk.Label(content_frame, text="Name: ")
        name_label.grid(column=1, row=1)

        name_entry = tk.Entry(content_frame)
        name_entry.grid(column=2, row=1, sticky="ew")


content = Content()
content.grid(row=2, column=1, sticky="nsew")

window.mainloop()
