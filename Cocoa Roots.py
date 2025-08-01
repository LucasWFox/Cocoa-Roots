import pickle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

# lists of classes and objects
# these associative arrays are global
ingredients = {}
batches = {}

FILE_NAME = "data.pkl"

# global colours
BLACK = "#000000"  # string
RED = "#B3152A"
ORANGE = "#F6A482"
DARK_ORANGE = "#ED652D"
LIGHT_ORANGE = "#FEDBC7"
LIGHT_BLUE = "#D1E5F0"
DARK_BLUE = "#8EC4DE"
BACKGROUND = "#F5F0ED"
ERROR_GREEN = "#46F274"  # This colour should only be on hidden elements


# -----------------------------------------------------------------------------
# SAVE AND LOAD
# -----------------------------------------------------------------------------

def save():
    # condense data to one object to save
    file_data = {"ingredients": ingredients, "batches": batches,
                 "batch_id_counter": Batch.id_counter, "ingredient_id_counter": Ingredient.id_counter}

    with open(FILE_NAME, "wb") as file:
        pickle.dump(file_data, file)  # save data to file

    window.destroy()  # close window


def load():
    try:
        file = open(FILE_NAME, "rb")
        content = pickle.load(file)

    except FileNotFoundError:  # if file does not exist

        open(FILE_NAME, "wb")  # create file
        return -1  # finish load()

    # if file content matches format
    if list(content.keys()) == ["ingredients", "batches", "batch_id_counter", "ingredient_id_counter"]:

        ingredients.update(content["ingredients"])
        batches.update(content["batches"])

        Batch.id_counter = content["batch_id_counter"]
        Ingredient.id_counter = content["ingredient_id_counter"]

    else:
        messagebox.showerror("Import Error", "There was an error loading content")


# -----------------------------------------------------------------------------
# CLASS FUNCTIONALITY
# -----------------------------------------------------------------------------

class Ingredient:
    id_counter = {}  # associative array counter, keys will be 3 character ingredient codes, key_values will be int

    # data comes from create_ingredient method of IngredientPage class, submitted by the user to the GUI
    # name: str, weight: float, source: str
    def __init__(self, name, weight, source):
        code = name[:3].upper()
        code_counter = Ingredient.id_counter.get(code, 1)

        self.id = f"ING-{code}-{code_counter:03d}"  # ingredient unique identifier
        Ingredient.id_counter[code] = code_counter + 1

        self.name = name  # common name of batch
        self.weight = weight
        self.__source = source  # name of ingredient suppler, private information

    # data comes from add_ingredient method of Batch class
    # amount: float
    def reduce_amount(self, amount):
        calc_weight = self.weight - amount

        # if-elif-else control structure used for validation of data
        if calc_weight > 0:  # range check
            self.weight = calc_weight
            return 1

        elif calc_weight < 0:
            messagebox.showinfo("Notification", f"There is only {self.weight} of this ingredient")
            return -1

        else:
            del ingredients[self.id]


class Batch:
    id_counter = 1  # int counter

    def __init__(self):
        self.__log = []  # list of every event occurred in batch
        self.__total_weight = 0  # batch data private
        self.__ingredients = {}

        self.id = f"BAT-{Batch.id_counter:03d}"  # Batch unique identifier
        Batch.id_counter += 1

        messagebox.showinfo("Notification", f"New Batch Created, id: {self.id}")

    # __________ Batch Methods __________
    # the data for these methods comes from alter_batch method from EditBatchPage class
    # submitted by the user to the GUI

    # date: str, ingredient_id: str (as it contains both characters and numerals), amount: float
    def add_ingredient(self, date, ingredient_id, amount):

        if not (date and ingredient_id and amount):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date = datetime.strptime(date, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        try:
            amount = float(amount)

        except ValueError:
            messagebox.showerror("Type Error", "Amount must be an floating point")
            return -1

        if amount < 0:  # range check
            messagebox.showerror("Range Error", "Amount cannot be less than zero")
            return -1

        if ingredient_id not in ingredients:
            messagebox.showinfo("Not Found", "Ingredient ID was not found, please check ID is in format ING-000-AAA")
            return -1

        ingredient = ingredients[ingredient_id]

        e = ingredient.reduce_amount(amount)  # e variable checking for error
        if e == -1:  # if error
            return -1

        self.__total_weight += amount

        #  increase ingredient amount or add ingredient to dict
        #                              set value to 0 if ingredient not present   V
        self.__ingredients[ingredient_id] = self.__ingredients.get(ingredient_id, 0) + amount

        record = {"process": "add_ingredient",
                  "ingredient": ingredient_id,
                  "amount": amount,
                  "date": date.strftime("%d/%m/%Y")
                  }

        self.__log.append(record)

    # start_dt: datetime, end_dt: datetime, additive: str,
    # amount: float (amount is float for more precise measurement than int)
    def fermentation(self, start_dt, end_dt, additive, amount):

        if not (start_dt and end_dt and additive and amount):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            start_dt = datetime.strptime(start_dt, "%d/%m/%Y")
            end_dt = datetime.strptime(end_dt, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        try:
            amount = float(amount)

        except ValueError:
            messagebox.showerror("Type Error", "Amount must be an floating point")
            return -1

        if amount < 0:  # range check
            messagebox.showerror("Range Error", "Amount cannot be less than zero")
            return -1

        #  increase ingredient amount or add ingredient to dict     V set value to 0 if additive not present
        self.__ingredients[additive] = self.__ingredients.get(additive, 0) + amount

        duration = end_dt - start_dt

        record = {"process": "fermentation",
                  "ingredient": additive,
                  "amount": amount,
                  "start_dt": start_dt.strftime("%d/%m/%Y"),
                  "end_dt": end_dt.strftime("%d/%m/%Y"),
                  "duration": duration.days
                  }

        self.__log.append(record)

    # start_dt: datetime, end_dt: datetime, additive: str,
    # temperature: float (temperature is float for more precise measurement than int)
    def drying(self, start_dt, end_dt, temperature):

        if not (start_dt and end_dt and temperature):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            start_dt = datetime.strptime(start_dt, "%d/%m/%Y")
            end_dt = datetime.strptime(end_dt, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        try:
            temperature = float(temperature)

        except ValueError:
            messagebox.showerror("Type Error", "Temperature must be an floating point")
            return -1

        duration = end_dt - start_dt

        record = {"process": "drying",
                  "temperature": temperature,
                  "start_dt": start_dt.strftime("%d/%m/%Y"),
                  "end_dt": end_dt.strftime("%d/%m/%Y"),
                  "duration": duration.days
                  }

        self.__log.append(record)

    # date: datetime, weight_reduced: float
    def winnowing(self, date, weight_reduced):

        if not (date and weight_reduced):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date = datetime.strptime(date, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        if weight_reduced > self.__total_weight:  # range check
            messagebox.showerror("Range Error", "Weight reduced cannot be greater than total weight")
            return -1

        record = {"process": "winnowing",
                  "weight_reduced": weight_reduced,
                  "date": date.strftime("%d/%m/%Y"),
                  }

        self.__log.append(record)

    # date: datetime, fineness: float
    def grinding(self, date, fineness):  # fineness in mm

        if not (date and fineness):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date = datetime.strptime(date, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        if fineness < 0:  # range check
            messagebox.showerror("Range Error", "Fineness cannot be less than zero")
            return -1

        record = {"process": "grinding",
                  "fineness": fineness,
                  "date": date.strftime("%d/%m/%Y"),
                  }

        self.__log.append(record)

    # date: datetime, temperature: float
    def conching(self, date, temperature):

        if not (date and temperature):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date = datetime.strptime(date, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", f"Date must be inputted in the format DD/MM/YYYY")
            return -1

        try:
            temperature = float(temperature)

        except ValueError:
            messagebox.showerror("Type Error", "Temperature must be an floating point")
            return -1

        record = {"process": "conching",
                  "temperature": temperature,
                  "date": date.strftime("%d/%m/%Y"),
                  }

        self.__log.append(record)

    # date: datetime, melting_temp: float, cooling_temp: float, working_temp: float, molding_dimension: str (string
    # used as molding dimensions include multiple numeric values and other shape descriptions), weight_per_bar: float
    def tempering_molding(self, date, melting_temp, cooling_temp, working_temp, molding_dimension, weight_per_bar):

        if not (date and melting_temp and cooling_temp and working_temp and molding_dimension and weight_per_bar):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date = datetime.strptime(date, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        try:
            melting_temp = float(melting_temp)
            cooling_temp = float(cooling_temp)
            working_temp = float(working_temp)
            weight_per_bar = float(weight_per_bar)

        except ValueError:
            messagebox.showerror("Type Error", "Temperature and weight feilds must be an floating point")
            return -1

        if weight_per_bar < 0:  # range check
            messagebox.showerror("Range Error", "Weight per bar cannot be less than zero")
            return -1

        record = {"process": "tempering_molding",
                  "melting_temp": melting_temp,
                  "cooling_temp": cooling_temp,
                  "working_temp": working_temp,
                  "molding_dimension": molding_dimension,
                  "weight_per_bar": weight_per_bar,
                  "date": date.strftime("%d/%m/%Y"),
                  }

        self.__log.append(record)

    # date: datetime, verification_num: str (str used for verification_num as it does not need to
    # undergo numeric operations and may contain non-numeric characters)
    def finalise(self, date, verification_num):

        if not (date and verification_num):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date = datetime.strptime(date, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        record = {"process": "finalise",
                  "verification_num": verification_num,
                  "date": date.strftime("%d/%m/%Y"),
                  }

        self.__log.append(record)

    # log getter
    def get_log(self):
        return self.__log


# -----------------------------------------------------------------------------
# GUI INTERFACE
# -----------------------------------------------------------------------------

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.logo = ImageTk.PhotoImage(Image.open("Resources/Bean_Logo.png"))

        # adjust window features
        self.config(bg="blue")
        self.geometry("400x600")  # window dimensions
        self.title("Cocoa Roots")
        self.grid_columnconfigure(1, weight=1)  # make expandable with screen
        self.grid_rowconfigure(2, weight=1)

        style = ttk.Style()  # set ttk style (to format scroll bars)
        style.theme_use("clam")

        # titlebar
        self.title_bar = tk.Frame(height=4, bg=ORANGE)
        self.title_bar.grid(row=1, column=1, sticky="ew")

        logo_label = tk.Label(self.title_bar, image=self.logo, bg=ORANGE)
        logo_label.pack(side=tk.LEFT)

        title_text = tk.Label(self.title_bar, text="Cocoa Roots", font=("Bernard MT Condensed", 25), bg=ORANGE)
        title_text.pack(side=tk.LEFT)

        # Put content below titlebar
        content = Content(self)
        content.grid(row=2, column=1, sticky="nsew")


class Content(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, bg=BACKGROUND, height=20, borderwidth=1, relief="solid")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.back_track = {}  # keep track of page navigation
        # place button in titlebar
        self.back_button = tk.Button(parent.title_bar,
                                     text="<",
                                     width=7,
                                     height=2,
                                     bg=LIGHT_ORANGE,
                                     borderwidth=1,
                                     relief="solid",
                                     command=lambda: self.go_back()
                                     )

        self.pages = {}  # dictionary of sub-frames within content

        # use of for loop control structure to minimise repetition in code
        for page in [UserPage, WorkerPage, ConsumerPage, IngredientPage,
                     EditBatchPage, ViewBatchPage]:  # for every page within content
            page_class = page(parent=self)  # create frame class

            self.pages[page] = page_class

            page_class.grid(row=1, column=1, sticky="nsew")

        self.current_page = UserPage
        self.switch_page(UserPage)

    def navigate(self, page_name):  # user navigation that records previous page
        self.back_track[page_name] = self.current_page
        self.switch_page(page_name)

    def go_back(self):  # switches to previous page
        last_page = self.back_track[self.current_page]
        self.switch_page(last_page)

    def switch_page(self, page_name):
        if page_name in self.back_track:  # if there is a page before current
            self.back_button.pack(padx=10, side=tk.RIGHT)  # show back button
        else:
            self.back_button.pack_forget()  # hide back button

        self.current_page = page_name
        page = self.pages[page_name]
        page.tkraise()  # bring frame to front (switch page)


class UserPage(tk.Frame):  # menu to select user type
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

        self.batch_id = ""
        self.parent = parent

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=2)

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

        ingredient_frame.grid_propagate(False)  # keep specified dimensions
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

        batches_frame.grid_propagate(False)  # keep specified dimensions
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
                                   command=lambda: self.add_batch()
                                   )
        batches_button.grid(row=1, column=2, sticky="e", padx=5)

        # __________ Existing Batches __________

        content_frame = tk.Frame(self, bg=BLACK)  # black frame to create boarder
        content_frame.grid(row=3, column=1, sticky="nsew", pady=(0, 20), padx=10)

        self.scroll_area = ScrollableBatchList(content_frame, parent, "worker")
        self.scroll_area.pack(fill="both", expand=True, pady=3, padx=3)

    def add_batch(self):
        instance = Batch()
        instance_id = instance.id

        batches[instance_id] = instance  # add batch instance to dictionary
        self.scroll_area.update_batch_list()  # reload worker page batch list
        self.parent.pages[ConsumerPage].scroll_area.update_batch_list()  # reload user page batch list


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
        content_frame.grid(column=1, row=2, sticky="nsew")

        content_frame.grid_columnconfigure(2, weight=1)

        name_label = tk.Label(content_frame, text="Name: ")
        name_label.grid(column=1, row=1, padx=5)

        self.name_entry = tk.Entry(content_frame)
        self.name_entry.grid(column=2, row=1, pady=10, padx=10, sticky="ew")

        weight_label = tk.Label(content_frame, text="Weight: ")
        weight_label.grid(column=1, row=2, padx=5)

        self.weight_entry = tk.Entry(content_frame)
        self.weight_entry.grid(column=2, row=2, pady=10, padx=10, sticky="ew")

        source_label = tk.Label(content_frame, text="Source: ")
        source_label.grid(column=1, row=3, padx=10)

        self.source_entry = tk.Entry(content_frame)
        self.source_entry.grid(column=2, row=3, pady=10, padx=10, sticky="ew")

        back_button = tk.Button(content_frame,
                                text="Submit",
                                width=10,
                                height=2,
                                bg=LIGHT_ORANGE,
                                borderwidth=1,
                                relief="solid",
                                command=lambda: self.add_ingredient()
                                )
        back_button.grid(column=1, row=4, pady=20, padx=10)

    def add_ingredient(self):
        name = self.name_entry.get()
        weight = self.weight_entry.get()
        source = self.source_entry.get()

        if not (name and weight and source):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            weight = float(weight)

        except ValueError:
            messagebox.showerror("Type Error", "Weight must be a number")
            return -1

        if weight <= 0:
            messagebox.showerror("Range Error", "Weight must be a positive number")
            return -1

        instance = Ingredient(name, weight, source)
        instance_id = instance.id
        ingredients[instance_id] = instance

        messagebox.showinfo("Notification", f"New Ingredient Added, id: {instance_id}")


class EditBatchPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=20, borderwidth=1, relief="solid")

        self.batch_id = ""

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=3)

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

        self.title_label = tk.Label(title_frame,
                                    bg=LIGHT_BLUE,
                                    text="..."
                                    )
        self.title_label.grid(row=1, column=1)

        # __________ Page Content __________
        self.method_entries = {}

        content_frame = tk.Frame(self, bg=BLACK)
        content_frame.grid(row=2, column=1, sticky="nsew", pady=10, padx=10)

        self.scroll_area = ScrollableBatchFunctions(content_frame, self)
        self.scroll_area.pack(expand=True, pady=3, padx=3)

    def update_page(self, instance_id):
        self.batch_id = instance_id
        self.title_label.config(text=instance_id)

        self.scroll_area.notification_text = ("ID                               Weight\n"
                                              "----------------------------------------")

        # for loop control structure used to apply procces to variable amount of ingredients
        for ingredient in ingredients.values():
            self.scroll_area.notification_text += f"\n{ingredient.id}:             {ingredient.weight}"

    def alter_batch(self, method_str):
        method_func = getattr(batches[self.batch_id], method_str)

        method_entries = self.method_entries[method_str]

        kwargs = {}

        for parameter in method_entries:
            kwargs[parameter] = method_entries[parameter].get()

        return method_func(**kwargs)


class ScrollableBatchFunctions(tk.Canvas):
    def __init__(self, location, parent):
        tk.Canvas.__init__(self, location, bg=DARK_BLUE)

        self.parent = parent

        self.content = tk.Frame(self, bg=DARK_BLUE)

        self.content.grid_columnconfigure(1, weight=1)

        # __________ Scrollbar Stuff __________
        scroll_bar = ttk.Scrollbar(location, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=scroll_bar.set)

        scroll_bar.pack(side="right", fill="y")
        self.pack(side="left", fill="both", expand=True)

        self.window_id = self.create_window((0, 0), window=self.content, anchor="nw")

        self.content.bind("<Configure>", lambda event: self.configure(scrollregion=self.bbox("all")))
        self.bind("<Configure>", lambda event: self.itemconfig(self.window_id, width=event.width))

        # __________ Content Stuff __________
        self.batch_methods = [method for method in dir(Batch)  # get Batch methods
                              if method[:2] != "__"  # not including  double underscore methods
                              and method not in ["id_counter", "get_log"]  # and not including non-callable attributes
                              ]                                            # or getter methods

        method_row = 2
        for method_str in self.batch_methods:
            method_func = getattr(Batch, method_str)  # gat callable method from method name

            # get list of function parameters to fill, slice list so parameters with co_argcount so only relevant
            # parameters show not including *args, **kwargs or self
            parameters = list(method_func.__code__.co_varnames[:method_func.__code__.co_argcount])
            parameters.remove("self")

            method_frame = tk.Frame(self.content,
                                    bg=LIGHT_BLUE,
                                    borderwidth=1,
                                    relief="solid"
                                    )
            method_frame.grid(row=method_row, column=1, pady=10, sticky="we")

            method_frame.columnconfigure(3, weight=1)

            self.method_label = tk.Label(method_frame,
                                         bg=LIGHT_ORANGE,
                                         text=method_str
                                         )
            self.method_label.grid(row=1, column=1, columnspan=2, sticky="w")

            submit_button = tk.Button(method_frame,
                                      bg=LIGHT_ORANGE,
                                      text="Submit",
                                      padx=5,
                                      command=lambda arg=method_str: self.submit(arg)
                                      )
            submit_button.grid(row=1, column=4, sticky="e", padx=5)

            # if control structure used to add button to one iteration of a for loop
            if method_str == "add_ingredient":
                self.notification_text = ("ID                               Weight\n"
                                          "----------------------------------------")

                ingredients_button = tk.Button(method_frame,
                                               bg=LIGHT_ORANGE,
                                               text="ingredients",
                                               padx=5,
                                               command=lambda: messagebox.showinfo("Notification",
                                                                                   self.notification_text)
                                               )
                ingredients_button.grid(row=1, column=3, sticky="e", padx=5)

            parameter_entries = {}
            row = 2
            for parameter in parameters:
                name_label = tk.Label(method_frame, text=parameter)
                name_label.grid(column=1, row=row, padx=5)

                name_entry = tk.Entry(method_frame)
                name_entry.grid(column=2, columnspan=3, row=row, pady=10, padx=10, sticky="ew")

                parameter_entries[parameter] = name_entry

                row += 1

            parent.method_entries[method_str] = parameter_entries

            method_row += 1

    def submit(self, method_str):
        e = self.parent.alter_batch(method_str)  # e variable checking for error
        if not e == -1:
            for widget in self.parent.method_entries[method_str].values():
                widget.delete(0, tk.END)  # clear text from affected entries

        self.parent.update_page(self.parent.batch_id)


class ConsumerPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=20, borderwidth=1, relief="solid")

        self.rowconfigure(2, weight=1)

        self.parent = parent

        self.search_icon = ImageTk.PhotoImage(Image.open("Resources/Search_entry.png").resize((30, 30)))

        self.grid_columnconfigure(1, weight=1)

        search_background = tk.Frame(self, bg=LIGHT_ORANGE, borderwidth=1, relief="solid")
        search_background.grid(row=1, column=1, pady=20, ipady=5, padx=(15, 50), sticky="we")
        search_background.grid_columnconfigure(1, weight=1)

        self.search_bar = tk.Entry(search_background,
                                   borderwidth=1,
                                   relief="solid",
                                   font=("Calabi", 12)
                                   )
        self.search_bar.grid(row=1, column=1, pady=(10, 0), ipady=7, padx=20, sticky="we")

        search_button = tk.Button(search_background,
                                  image=self.search_icon,
                                  bg=LIGHT_ORANGE,
                                  height=25,
                                  borderwidth=1,
                                  relief="ridge",
                                  command=self.search
                                  )
        search_button.grid(row=1, column=2, padx=(0, 20), pady=(10, 0), ipady=3)

        content_frame = tk.Frame(self, bg=BLACK)  # black border frame
        content_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=(0, 20))

        self.scroll_area = ScrollableBatchList(content_frame, parent, "consumer")
        self.scroll_area.pack(fill="both", expand=True, pady=3, padx=3)

    def search(self):
        search_value = self.search_bar.get()

        if not search_value:
            messagebox.showerror("Existence Error", "Please enter batch id into the searchbar")
            return -1

        if search_value not in batches:
            messagebox.showinfo("Batch not found", "Batch id was not found, please check id is in format BAT-000")
            return -1

        self.parent.navigate(ViewBatchPage)
        self.parent.pages[ViewBatchPage].update_page(search_value)  # update page


class ViewBatchPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=20, borderwidth=1, relief="solid")

        self.batch_id = ""  # current batch

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # __________ Page Title __________
        title_frame = tk.Frame(self,
                               bg=LIGHT_BLUE,
                               height=50,
                               width=50,
                               borderwidth=1,
                               relief="solid"
                               )
        title_frame.grid(row=1, column=1, padx=15, pady=10, sticky="we")

        title_frame.grid_propagate(False)
        title_frame.rowconfigure(1, weight=1)
        title_frame.columnconfigure(1, weight=1)

        self.title_label = tk.Label(title_frame,  # to be updated when page is loaded
                                    bg=LIGHT_BLUE,
                                    text="..."  # show ... if no other title in loaded
                                    )
        self.title_label.grid(row=1, column=1)

        # __________ Page Content __________
        content_frame = tk.Frame(self, bg=BLACK)
        content_frame.grid(row=2, column=1, sticky="nsew", pady=10, padx=10)

        self.scroll_area = ScrollableBatchLView(content_frame)
        self.scroll_area.pack(expand=True, pady=3, padx=3)

    def update_page(self, instance_id):
        self.batch_id = instance_id  # change page title
        self.title_label.config(text=instance_id)

        self.scroll_area.update_page(instance_id)


class ScrollableBatchLView(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=DARK_BLUE, **kwargs)

        self.content = tk.Frame(self, bg=DARK_BLUE)  # main content area

        self.content.grid_columnconfigure(1, weight=1)

        # __________ Scrollbar Stuff __________
        scroll_bar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=scroll_bar.set)

        scroll_bar.pack(side="right", fill="y")
        self.pack(side="left", fill="both", expand=True)

        self.window_id = self.create_window((0, 0), window=self.content, anchor="nw")

        self.content.bind("<Configure>", lambda event: self.configure(scrollregion=self.bbox("all")))
        self.bind("<Configure>", lambda event: self.itemconfig(self.window_id, width=event.width))

    def update_page(self, instance_id):
        for widget in self.content.winfo_children():  # clear content before reloading
            widget.destroy()

        process_row = 1
        for process in batches[instance_id].get_log():  # for every action taken in batch log
            process = process.copy()
            process_frame = tk.Frame(self.content,
                                     bg=LIGHT_BLUE,
                                     borderwidth=1,
                                     relief="solid"
                                     )
            process_frame.grid(row=process_row, column=1, padx=10, pady=10, sticky="we")

            process_frame.columnconfigure(2, weight=1)

            process_title = tk.Label(process_frame,
                                     bg=LIGHT_ORANGE,
                                     text=process["process"]
                                     )
            process_title.grid(row=1, column=1, columnspan=2, sticky="w")
            del process["process"]

            date_label = tk.Label(process_frame,
                                  bg=LIGHT_ORANGE,
                                  text="...",
                                  padx=5,
                                  )
            date_label.grid(row=1, column=2, sticky="e", padx=5)

            if "date" in process:
                date_label.config(text=process["date"])
                del process["date"]
            else:
                date_label.config(text=f"{process['start_dt']}-{process['end_dt']}")
                del process["start_dt"]
                del process["end_dt"]

            key_row = 2
            for key in process:
                # load each action as label to show consumer
                attribute_title = tk.Label(process_frame, bg=LIGHT_BLUE, text=f"{key}:")
                attribute_title.grid(row=key_row, column=1, sticky="n")

                attribute_value = tk.Label(process_frame, bg=LIGHT_BLUE, text=f"{process[key]}")
                attribute_value.grid(row=key_row, column=2, sticky="e")

                key_row += 1

            process_row += 1


class ScrollableBatchList(tk.Canvas):
    def __init__(self, parent, grandparent, user_type, **kwargs):
        super().__init__(parent, bg=DARK_BLUE, **kwargs)

        self.user_type = user_type
        self.parent = parent
        self.grandparent = grandparent

        self.content = tk.Frame(self, bg=DARK_BLUE)  # main content area

        self.content.grid_columnconfigure(1, weight=1)

        # __________ Scrollbar Stuff __________
        scroll_bar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=scroll_bar.set)

        scroll_bar.pack(side="right", fill="y")
        self.pack(side="left", fill="both", expand=True)

        self.window_id = self.create_window((0, 0), window=self.content, anchor="nw")

        self.content.bind("<Configure>", lambda event: self.configure(scrollregion=self.bbox("all")))
        self.bind("<Configure>", lambda event: self.itemconfig(self.window_id, width=event.width))

        # __________ Content Stuff __________
        self.update_batch_list()

    def update_batch_list(self):  # reload content in scrollbar
        for widget in self.content.winfo_children():  # get all content children
            widget.destroy()  # delete children

        batch_row = 1
        for batch in batches.values():  # for every saved batch (list of classes)
            batch_frame = tk.Frame(self.content,
                                   bg=LIGHT_BLUE,
                                   borderwidth=1,
                                   relief="solid"
                                   )
            batch_frame.grid(row=batch_row, column=1, pady=10, sticky="we")

            batch_frame.columnconfigure(3, weight=1)

            batch_label = tk.Label(batch_frame,
                                   bg=LIGHT_ORANGE,
                                   text=batch.id
                                   )
            batch_label.grid(row=1, column=1, columnspan=2, sticky="w")

            submit_button = tk.Button(batch_frame,
                                      bg=LIGHT_ORANGE,
                                      text=">",
                                      padx=5,
                                      command=lambda arg=batch.id: self.navigate_batch(arg)
                                      )
            submit_button.grid(row=1, column=4, sticky="e", padx=5)
            batch_row += 1

    def navigate_batch(self, batch_id):

        # if-elif control structure used for checking user type
        if self.user_type == "worker":  # if scroll area in user section of GUI
            self.grandparent.navigate(EditBatchPage)
            self.grandparent.pages[EditBatchPage].update_page(batch_id)  # update page

        elif self.user_type == "consumer":  # if scroll area in consumer section of GUI
            self.grandparent.navigate(ViewBatchPage)
            self.grandparent.pages[ViewBatchPage].update_page(batch_id)  # update page


if __name__ == "__main__":
    # call load function
    load()

    window = Window()

    # Call save function on closing tkinter window
    window.protocol("WM_DELETE_WINDOW", lambda: save())

    window.mainloop()
