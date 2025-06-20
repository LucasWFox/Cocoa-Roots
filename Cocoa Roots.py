import tkinter as tk
import tkinter.ttk as ttk
import pickle

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

# titlebar
title = tk.Label(height=4, bg=ORANGE)
title.grid(row=0, column=0, sticky="ew")
window.grid_columnconfigure(0, weight=1)

# background
content = tk.Label(bg="#f5f0ed")
content.grid(row=1, column=0, sticky="nsew")
window.grid_rowconfigure(1, weight=1)

item = tk.Label(content, bg=LIGHT_BLUE)
item.pack()

window.mainloop()
