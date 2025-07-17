# import pickle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# lists of classes and objects
# these associative arrays are global
ingredients = {}
batches = {}
tickets = {}

# global colours
BLACK = "#000000"
RED = "#B3152A"
ORANGE = "#F6A482"
DARK_ORANGE = "#ED652D"
LIGHT_ORANGE = "#FEDBC7"
LIGHT_BLUE = "#D1E5F0"
DARK_BLUE = "#8EC4DE"
BACKGROUND = "#F5F0ED"
ERROR_GREEN = "#46F274"  # This colour should only be on hidden elements


# -----------------------------------------------------------------------------
# FUNCTIONALITY
# -----------------------------------------------------------------------------

class Ingredient:
    ID_counter = 1

    def __init__(self, name, weight, source):
        self.log = []  # list of every event occurred in ingredient

        self.ID = f"ING-{Ingredient.ID_counter:03d}-{name[:3].upper()}"  # ingredient unique identifier
        Ingredient.ID_counter += 1

        self.name = name  # common name of batch
        self.weight = weight
        self.source = source  # name of ingredient suppler

        messagebox.showinfo("Notification", f"New Ingredient Added, ID: {self.ID}")

    def reduce_amount(self, amount):
        calc_weight = self.weight - amount

        if calc_weight >= 0:  # range check
            self.weight = calc_weight

        elif calc_weight < 0:
            raise ValueError(f"There is only {self.weight} grams of this ingredient")


class Batch:
    ID_counter = 1

    def __init__(self):
        self.log = []  # list of every event occurred in batch

        self.ID = f"BAT-{Batch.ID_counter:03d}"  # Batch unique identifier
        Batch.ID_counter += 1

        self.total_weight = 0

        messagebox.showinfo("Notification", f"New Batch Created, ID: {self.ID}")

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
            raise ValueError("weight reduced cannot be greater than total weight")

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
    def __init__(self):
        self.ID = ""

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
class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.logo = ImageTk.PhotoImage(Image.open("Resources/Bean_Logo.png"))

        self.config(bg="blue")
        self.geometry("400x600")  # window dimensions
        self.title("Cocoa Roots")
        self.grid_columnconfigure(1, weight=1)  # make expandable with screen
        self.grid_rowconfigure(2, weight=1)

        style = ttk.Style()
        style.theme_use('clam')

        # list the options of the style
        # (Argument should be an element of TScrollbar, e.g. "thumb", "trough", ...)
        print(style.element_options("Horizontal.TScrollbar.thumb"))

        # configure the style
        style.configure("Horizontal.TScrollbar", gripcount=0,
                        background="Green", darkcolor="DarkGreen", lightcolor="LightGreen",
                        troughcolor="gray", bordercolor="blue", arrowcolor="white")

        # titlebar
        self.title_bar = tk.Frame(height=4, bg=ORANGE)
        self.title_bar.grid(row=1, column=1, sticky="ew")

        logo_label = tk.Label(self.title_bar, image=self.logo, bg=ORANGE)
        logo_label.pack(side=tk.LEFT)

        title_text = tk.Label(self.title_bar, text="Cocoa Roots", font=("Bernard MT Condensed", 25), bg=ORANGE)
        title_text.pack(side=tk.LEFT)

        content = Content(self)
        content.grid(row=2, column=1, sticky="nsew")


class Content(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, bg=BACKGROUND, height=20, borderwidth=1, relief="solid")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.back_track = {}
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

        for page in [UserPage, WorkerPage, ConsumerPage, IngredientPage, BatchPage]:  # for every page within content
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
        self.batch_ID = ""

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
                                   command=lambda: [parent.pages[BatchPage].create_batch(), parent.navigate(BatchPage)]
                                   )
        batches_button.grid(row=1, column=2, sticky="e", padx=5)


class ConsumerPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=20, borderwidth=1, relief="solid")

        self.search_icon = ImageTk.PhotoImage(Image.open("Resources/Search_entry.png").resize((30, 30)))

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
                                  image=self.search_icon,
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
                                command=self.create_ingredient
                                )
        back_button.grid(column=1, row=4, pady=20, padx=10)

    def create_ingredient(self):
        name = self.name_entry.get()
        weight = self.weight_entry.get()
        source = self.source_entry.get()

        try:
            weight = float(weight)

        except ValueError:
            messagebox.showerror("Type Error", "Weight must be a number")

        else:
            if (not name) or (not weight) or (not source):
                messagebox.showerror("Existence Error", "Please complete all fields")

            elif weight <= 0:
                messagebox.showerror("Range Error", "Weight must be a positive number")

            else:
                instance = Ingredient(name, weight, source)
                instance_ID = instance.ID
                ingredients[instance_ID] = instance
                print(ingredients)


class BatchPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=20, borderwidth=1, relief="solid")

        self.batch_ID = ""

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
        content_frame = tk.Frame(self, bg=BLACK)
        content_frame.grid(row=2, column=1, sticky="nsew", pady=10, padx=10)

        scroll_area = ScrollableBatchContent(content_frame)
        scroll_area.pack(expand=True, pady=3, padx=3)

    def create_batch(self):
        instance = Batch()
        instance_ID = instance.ID

        batches[instance_ID] = instance
        print(batches)

        self.batch_ID = instance_ID
        self.title_label.config(text=instance_ID)


class ScrollableBatchContent(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self, parent)

        self.content = tk.Frame(self, bg=DARK_BLUE)

        for i in range(1, 11):
            self.content.grid_rowconfigure(i, weight=1)
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
        batch_methods = [method for method in dir(Batch)
                         if method[:2] != "__"
                         and method not in ["ID_counter", "save", "make_ticket"]
                         ]

        method_row = 2
        for method_str in batch_methods:
            method_func = getattr(Batch, method_str)
            parameters = list(method_func.__code__.co_varnames)
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

            ingredient_button = tk.Button(method_frame,
                                          bg=LIGHT_ORANGE,
                                          text="Submit",
                                          padx=5,
                                          command=lambda: parent.navigate(IngredientPage)
                                          )
            ingredient_button.grid(row=1, column=4, sticky="e", padx=5)

            row = 2
            for parameter in parameters:
                name_label = tk.Label(method_frame, text=parameter)
                name_label.grid(column=1, row=row, padx=5)

                name_entry = tk.Entry(method_frame)
                name_entry.grid(column=2, columnspan=3, row=row, pady=10, padx=10, sticky="ew")

                row += 1

            """i = 1
            for c in ["blue", "green", "red", "black"]:
                tk.Label(method_frame, bg=c).grid(row=3, column=i, sticky="ew")
                i +=1"""

            method_row += 1


window = Window()

window.mainloop()
