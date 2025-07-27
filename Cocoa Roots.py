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
    id_counter = 1

    def __init__(self, name, weight, source):
        self.log = []  # list of every event occurred in ingredient

        self.id = f"ING-{Ingredient.id_counter:03d}-{name[:3].upper()}"  # ingredient unique identifier
        Ingredient.id_counter += 1

        self.name = name  # common name of batch
        self.weight = weight
        self.source = source  # name of ingredient suppler

        messagebox.showinfo("Notification", f"New Ingredient Added, id: {self.id}")

    def reduce_amount(self, amount):
        calc_weight = self.weight - amount

        if calc_weight >= 0:  # range check
            self.weight = calc_weight

        elif calc_weight < 0:
            raise ValueError(f"There is only {self.weight} grams of this ingredient")


class Batch:
    id_counter = 1

    def __init__(self):
        self.__log = []  # list of every event occurred in batch
        self.__total_weight = 0
        self.__ingredients = {}

        self.id = f"BAT-{Batch.id_counter:03d}"  # Batch unique identifier
        Batch.id_counter += 1

        messagebox.showinfo("Notification", f"New Batch Created, id: {self.id}")

    def add_ingredient(self, date_time, ingredient_id, amount):

        if not (date_time and ingredient_id and amount):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date_time = datetime.strptime(date_time, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        try:
            amount = int(amount)

        except ValueError:
            messagebox.showerror("Type Error", "Amount must be an integer")
            return -1

        if amount < 0:  # range check
            messagebox.showerror("Range Error", "Amount cannot be less than zero")
            return -1

        if ingredient_id not in ingredients:
            messagebox.showinfo("Not Found", "Ingredient ID was not found, please check ID is in format ING-000-AAA")
            return -1
        
        ingredient = ingredients[ingredient_id]
        
        #  increase ingredient amount or add ingredient to dict
        #                              set value to 0 if ingredient not present   V
        self.__ingredients[ingredient_id] = self.__ingredients.get(ingredient_id, 0) + amount

        ingredient.reduce_amount(amount)
        self.__total_weight += amount

        record = {"process": "add_ingredient",
                  "ingredient": ingredient,
                  "amount": amount,
                  "date_time": date_time
                  }

        self.__log.append(record)

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
            amount = int(amount)

        except ValueError:
            messagebox.showerror("Type Error", "Amount must be an integer")
            return -1

        if amount < 0:  # range check
            messagebox.showerror("Range Error", "Amount cannot be less than zero")
            return -1

        additive.reduce_amount(amount)

        #  increase ingredient amount or add ingredient to dict     V set value to 0 if additive not present
        self.__ingredients[additive] = self.__ingredients.get(additive, 0) + amount

        duration = end_dt - start_dt

        record = {"process": "fermentation",
                  "ingredient": additive,
                  "amount": amount,
                  "start_dt": start_dt,
                  "end_dt": end_dt,
                  "duration": duration.days
                  }

        self.__log.append(record)

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
            temperature = int(temperature)

        except ValueError:
            messagebox.showerror("Type Error", "Temperature must be an integer")
            return -1

        duration = end_dt - start_dt

        record = {"process": "drying",
                  "temperature": temperature,
                  "start_dt": start_dt,
                  "end_dt": end_dt,
                  "duration": duration.days
                  }

        self.__log.append(record)

    def winnowing(self, date_time, weight_reduced):

        if not (date_time and weight_reduced):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date_time = datetime.strptime(date_time, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        if weight_reduced > self.__total_weight:  # range check
            messagebox.showerror("Range Error", "Weight reduced cannot be greater than total weight")
            return -1

        record = {"process": "winnowing",
                  "weight_reduced": weight_reduced,
                  "date_time": date_time,
                  }

        self.__log.append(record)

    def grinding(self, date_time, fineness):  # fineness in mm

        if not (date_time and fineness):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date_time = datetime.strptime(date_time, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        if fineness < 0:  # range check
            messagebox.showerror("Range Error", "Fineness cannot be less than zero")
            return -1

        record = {"process": "grinding",
                  "fineness": fineness,
                  "date_time": date_time,
                  }

        self.__log.append(record)

    def conching(self, date_time, temperature):

        if not (date_time and temperature):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date_time = datetime.strptime(date_time, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", f"Date must be inputted in the format DD/MM/YYYY")
            return -1

        try:
            temperature = int(temperature)

        except ValueError:
            messagebox.showerror("Type Error", "Temperature must be an integer")
            return -1

        record = {"process": "conching",
                  "temperature": temperature,
                  "date_time": date_time,
                  }

        self.__log.append(record)

    def tempering_molding(self, date_time, melting_temp, cooling_temp, working_temp, molding_dimension, weight_per_bar):

        if not (date_time and melting_temp and cooling_temp and working_temp and molding_dimension and weight_per_bar):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date_time = datetime.strptime(date_time, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        try:
            melting_temp = int(melting_temp)
            cooling_temp = int(cooling_temp)
            working_temp = int(working_temp)
            molding_dimension = int(molding_dimension)
            weight_per_bar = int(weight_per_bar)

        except ValueError:
            messagebox.showerror("Type Error", "Temperature and weight feilds must be an integer")
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
                  "date_time": date_time,
                  }

        self.__log.append(record)

    def finalise(self, date_time, verification_num):

        if not (date_time and verification_num):
            messagebox.showerror("Existence Error", "Please complete all fields")
            return -1

        try:
            date_time = datetime.strptime(date_time, "%d/%m/%Y")

        except ValueError:
            messagebox.showerror("Type Error", "Date must be inputted in the format DD/MM/YYYY")
            return -1

        record = {"process": "finalise",
                  "verification_num": verification_num,
                  "date_time": date_time,
                  }

        ...  # close ... write more

        self.__log.append(record)

    def get_log(self):
        return self.__log


def save():
    # condense data to one object to save
    file_data = {"ingredients": ingredients, "batches": batches,
                 "batch_id_counter": Batch.id_counter, "ingredient_id_counter": Ingredient.id_counter}

    with open(FILE_NAME, "wb") as file:
        pickle.dump(file_data, file)  # save data to file

    window.destroy()


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
# GUI INTERFACE
# -----------------------------------------------------------------------------

# main tkinter setup
class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Call save function on closing tkinter window
        self.protocol("WM_DELETE_WINDOW", lambda: save())
        load()  # load file content

        self.logo = ImageTk.PhotoImage(Image.open("Resources/Bean_Logo.png"))

        # adjust window features
        self.config(bg="blue")
        self.geometry("400x600")  # window dimensions
        self.title("Cocoa Roots")
        self.grid_columnconfigure(1, weight=1)  # make expandable with screen
        self.grid_rowconfigure(2, weight=1)

        style = ttk.Style()  # set ttk style (to format scroll bars)
        style.theme_use('clam')

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

        for page in [UserPage, WorkerPage, ConsumerPage, IngredientPage,
                     WorkerBatchPage, ConsumerBatchPage]:  # for every page within content
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

        self.scroll_area = ScrollableBatches(content_frame, parent, "worker")
        self.scroll_area.pack(fill="both", expand=True, pady=3, padx=3)

    def add_batch(self):
        instance = Batch()
        instance_id = instance.id

        batches[instance_id] = instance  # add batch instance to dictionary
        self.scroll_area.update_batch_list()  # reload worker page batch list
        self.parent.pages[ConsumerPage].scroll_area.update_batch_list()  # reload user page batch list


class ScrollableBatches(tk.Canvas):
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

        if self.user_type == "worker":  # if scroll area in user section of GUI
            self.grandparent.navigate(WorkerBatchPage)
            self.grandparent.pages[WorkerBatchPage].update_page(batch_id)  # update page

        elif self.user_type == "consumer":  # if scroll area in consumer section of GUI
            self.grandparent.navigate(ConsumerBatchPage)
            self.grandparent.pages[ConsumerBatchPage].update_page(batch_id)  # update page


class ConsumerPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=20, borderwidth=1, relief="solid")

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
        content_frame.grid(row=3, column=1, sticky="nsew", padx=10)

        self.scroll_area = ScrollableBatches(content_frame, parent, "consumer")
        self.scroll_area.pack(fill="both", expand=True, pady=3, padx=3)

    def search(self):
        search_value = self.search_bar.get()

        if not search_value:
            messagebox.showerror("Existence Error", "Please enter batch id into the searchbar")
            return -1

        if search_value not in batches:
            messagebox.showinfo("Batch not found", "Batch id was not found, please check id is in format BAT-000")
            return -1

        self.parent.navigate(ConsumerBatchPage)
        self.parent.pages[ConsumerBatchPage].update_page(search_value)  # update page


class ConsumerBatchPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=20, borderwidth=1, relief="solid")

        self.batch_id = ""  # current batch
        self.log_labels = []  # logs of applied processes to show consumer

        self.grid_columnconfigure(1, weight=1)

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

        self.details_label = tk.Label()

        # __________ Page Content __________

    def update_page(self, instance_id):
        self.batch_id = instance_id  # change page title
        self.title_label.config(text=instance_id)

        for widget in self.log_labels:  # clear content before reloading
            widget.destroy()

        row = 2
        for process in batches[instance_id].get_log():  # for every action taken in batch log
            process_label = tk.Label(self, text=str(process))  # load each action as label to show consumer
            process_label.grid(row=row, column=1)

            self.log_labels.append(process_label)
            row += 1


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
                                command=lambda: self.create_ingredient
                                )
        back_button.grid(column=1, row=4, pady=20, padx=10)

    def create_ingredient(self):
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


class WorkerBatchPage(tk.Frame):
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

        scroll_area = ScrollableBatchContent(content_frame, self)
        scroll_area.pack(expand=True, pady=3, padx=3)

    def update_page(self, instance_id):
        self.batch_id = instance_id
        self.title_label.config(text=instance_id)

    def alter_batch(self, method_str):
        method_func = getattr(batches[self.batch_id], method_str)

        method_entries = self.method_entries[method_str]

        kwargs = {}

        for parameter in method_entries.keys():
            kwargs[parameter] = method_entries[parameter].get()

        method_func(**kwargs)


class ScrollableBatchContent(tk.Canvas):
    def __init__(self, location, parent):
        tk.Canvas.__init__(self, location, bg=DARK_BLUE)

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
        self.batch_methods = [method for method in dir(Batch)
                              if method[:2] != "__"
                              and method not in ["id_counter", "save"]
                              ]

        method_row = 2
        for method_str in self.batch_methods:
            method_func = getattr(Batch, method_str)
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
                                      command=lambda arg=method_str: parent.alter_batch(arg)
                                      )
            submit_button.grid(row=1, column=4, sticky="e", padx=5)

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


window = Window()

window.mainloop()
