import tkinter as tk
from tkinter import ttk
import ShortestDistanceCalculations as sdc
import DataBase as db
import threading

LARGE_FONT = ("Verdana", 12)
XLARGE_FONT = ("Verdana", 18)
MEDIUM_FONT = ("Verdana", 8)
XMEDIUM_FONT = ("Verdana", 10)



class MainClass(tk.Tk):
    frames = {}

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.geometry("600x700")
    
        self.container = tk.Frame(self)
        self.container.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        #container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        """
        #to add pages to the program
        for F in (StartPage, NewLocPage, ConfirmLocationsPage, ChangeLocPage):
            if F == ConfirmLocationsPage:

                frame = F(container, self, NewLocPage.all_entered_locations)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            elif F == ChangeLocPage:

                frame = F(container, self, NewLocPage.all_valid_locations)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")

            else:
                frame = F(container, self)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")
        """
        self.Show_Frame(StartPage)

    def Show_Frame(self, cont):
        for F in (StartPage, NewLocPage, ConfirmLocationsPage, ChangeLocPage, ShortestDistancePage, NameOfInput, PreviusLocationsPage):

            if F == ConfirmLocationsPage:
                frame = F(self.container, self, NewLocPage.all_entered_locations)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")

            elif F == ChangeLocPage:
                frame = F(self.container, self, NewLocPage.all_valid_locations)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")

            elif F == ShortestDistancePage:
                frame = F(self.container, self, ConfirmLocationsPage.all_valid_locations)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")

            else:
                frame = F(self.container, self)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    #0 if old entery 1 if new entery
    new_or_old_entery = 0
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        welcome_label = tk.Label(self, text = "Welcome to FSD Program", width = 0, height = 0, font = XLARGE_FONT,)
        welcome_label.place(relx = 0.1, rely = 0, relwidth = 0.8, relheight = 0.25)

        previus_loc_btn = ttk.Button(self, text = "Previous Inputed Locations", command = self.previous_loc_click)
        previus_loc_btn.place(relx = 0.35, rely = 0.35, relwidth = 0.3, relheight = 0.05)

        new_loc_btn = ttk.Button(self, text="New Input locations", command = self.new_loc_click)
        new_loc_btn.place(relx=0.35, rely=0.45, relwidth=0.3, relheight=0.05)

    def new_loc_click(self):
        StartPage.new_or_old_entery = 1
        self.controller.Show_Frame(NameOfInput)

    def previous_loc_click(self):
        StartPage.new_or_old_entery = 0
        db.crete_table()
        PreviusLocationsPage.find_all_file_names(self)
        self.controller.Show_Frame(PreviusLocationsPage)


class NameOfInput(tk.Frame):
    name_of_input = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        main_label = tk.Label(self, text = "Please Enter The Name Of Your Entery", font = LARGE_FONT)
        main_label.place(relx = 0.1, rely = 0, relwidth = 0.8, relheight = 0.1)

        self.name_input_entery = tk.Entry(self)
        self.name_input_entery.place(relx = 0.2, rely = 0.15, relwidth = 0.6, relheight = 0.05)

        confirm_btn = ttk.Button(self, text ="Confirm", command = self.next_page)
        confirm_btn.place(relx = 0.3, rely = 0.8, relwidth = 0.4, relheight = 0.1)


    def next_page(self):
        NameOfInput.name_of_input = self.name_input_entery.get()
        self.controller.Show_Frame(NewLocPage)

class NewLocPage(tk.Frame):
    all_valid_locations = []
    all_entered_locations = []
    text1 = ""

    @classmethod
    def Next_Page(cls, parent, controller, array):
        text = ""
        list = {""}
        for i in range(len(array)):
            list.add(array[i])

        list.remove("")
        list = sorted(list)
        array = list

        for i in range(len(array)):
            if i % 5 == 0 and i != 0:
                text += str(array[i]) + "\n"
            elif i == len(list) - 1:
                text += str(array[i])
            else:
                text += str(array[i]) + ", "


        cls.text1 = text
        cls.all_valid_locations = array
        ConfirmLocationsPage(parent, controller, array)
        controller.Show_Frame(ConfirmLocationsPage)
        ConfirmLocationsPage.Confirm_Frame(parent, text)



    @classmethod
    def Get_Entered_locatons(cls, array, parent, controller):
        cls.allall_entered_locations = []
        for i in range(len(array)):
            cls.all_entered_locations.append(array[i].get())
        cls.Next_Page(parent, controller, cls.all_entered_locations)



    def __init__(self, parent, controller):
        self.number_of_loc = 0
        self.all_labels_ent = []
        self.all_entery_ent = []
        self.all_btn_ent = []

        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)

        how_many_loc_label = ttk.Label(self, text = "How Many Locations: ", font = LARGE_FONT)
        how_many_loc_label.place(relx = 0, rely = 0, relwidth = 0.3, relheight = 0.05)
        #how_many_loc_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.how_many_loc_entery = tk.Entry(self)
        self.how_many_loc_entery.place(relx = 0.35, rely = 0, relwidth = 0.3, relheight = 0.05)
        #self.how_many_loc_entery.grid(row = 0, column=1, padx = 10, pady = 10)

        how_many_loc_btn = ttk.Button(self, text = "Confirm", command =lambda: self.Return_How_Many_Loc(parent, controller))
        how_many_loc_btn.place(relx = 0.675, rely = 0, relwidth = 0.15, relheight = 0.05)
        #how_many_loc_btn.grid(row = 0, column = 3, padx = 10, pady = 10, ipadx = 25)

        home_btn = ttk.Button(self, text="Back", command = lambda: self.Go_Home_Click(parent, controller))
        home_btn.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.05)
        #clear_btn.grid(row = 0, column = 4, padx = 10, pady = 10)

    def Go_Home_Click(self,parent, controller):
        controller.Show_Frame(StartPage)
        self.number_of_loc = 0
        self.Generate_Enteries(parent, controller)

    def Return_How_Many_Loc(self, parent, controller):
        self.number_of_loc = self.how_many_loc_entery.get()
        self.Generate_Enteries(parent, controller)


    def Generate_Enteries(self,parent,controller):

        if len(self.all_labels_ent) > 0:
            for i in range(len(self.all_labels_ent)):
                self.all_labels_ent[i].destroy()
                self.all_entery_ent[i].destroy()


            self.all_entery_ent = []
            self.all_labels_ent = []

        if len(self.all_btn_ent)>0:
            for i in range(len(self.all_btn_ent)):
                self.all_btn_ent[i].destroy()

            self.all_btn_ent = []

        #cosmetics
        Y_BETWEEN_ENT = 0.055
        X_BETWEEN_ENT = 0.5
        X_BETWEEN_ENT_PAIR = 0.2

        ii = 0
        for i in range(int(self.number_of_loc)):
            if i == 0:
                self.all_labels_ent.append(tk.Label(self, text="Location " + str(i + 1) + ":"))
                #self.all_labels_ent[i].grid(row=i + 1, column=0, sticky = "w")
                self.all_labels_ent[i].place(relx = 0, rely = 0.1, relwidth = 0.2, relheight = 0.05)

                self.all_entery_ent.append(tk.Entry(self))
                #self.all_entery_ent[i].grid(row=i + 1, column=0, sticky = "w")
                self.all_entery_ent[i].place(relx = X_BETWEEN_ENT_PAIR, rely = 0.1, relwidth = 0.2, relheight = 0.05)

            elif not i >= int(self.number_of_loc)/2 :
                self.all_labels_ent.append(tk.Label(self, text = "Location " + str(i+1) + ":"))

                self.all_labels_ent[i].place(relx=0, rely=0.1 +(Y_BETWEEN_ENT*i), relwidth=0.2, relheight=0.05)

                self.all_entery_ent.append(tk.Entry(self))
                self.all_entery_ent[i].place(relx=X_BETWEEN_ENT_PAIR, rely=0.1 + (Y_BETWEEN_ENT*i), relwidth=0.2, relheight=0.05)

            else:

                self.all_labels_ent.append(tk.Label(self, text="Location " + str(i + 1) + ":"))
                self.all_labels_ent[i].place(relx=X_BETWEEN_ENT, rely=0.1 + (Y_BETWEEN_ENT * ii), relwidth=0.2, relheight=0.05)

                self.all_entery_ent.append(tk.Entry(self))
                self.all_entery_ent[i].place(relx=X_BETWEEN_ENT_PAIR + X_BETWEEN_ENT, rely=0.1 + (Y_BETWEEN_ENT * ii),
                                             relwidth=0.2, relheight=0.05)
                ii += 1

            if i+1 == int(self.number_of_loc):
                self.all_btn_ent.append(ttk.Button(self, text = "Generate Shortes Root",
                                                   command = lambda: self.Get_Entered_locatons(self.all_entery_ent, parent, controller)))
                self.all_btn_ent[0].place(relx = 0.3, rely = 0.95, relwidth = 0.4, relheight = 0.05)


class ConfirmLocationsPage(tk.Frame):
    all_valid_locations = []
    text1 = ""
    shortest_distance_list = []


    def __init__(self, parent, controller, all_valid_locations):
        self.text_label = []
        self.text1 = ""
        tk.Frame.__init__(self, parent)

        self.self1 = self
        self.controller = controller
        self.parent = parent
        self.all_valid_locations = all_valid_locations


        main_label = tk.Label(self, text="Is This The Location You Wish To Enter?", font=LARGE_FONT)
        main_label.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        self.save_chek_var = tk.IntVar(value=1)

        make_change_btn = ttk.Button(self, text="Make Changes",
                                     command=lambda: self.Make_Changes_Click(self.all_valid_locations))
        make_change_btn.place(relx=0.1, rely=0.85, relwidth=0.3, relheight=0.1)

        confirm_btn = ttk.Button(self, text="CONFIRM", command= self.Confirm_Click)
        confirm_btn.place(relx=0.45, rely=0.85, relwidth=0.3, relheight=0.1)

        save_chek_chek = tk.Checkbutton(self, text="Save Entery", variable=self.save_chek_var)
        save_chek_chek.place(relx=0.8, rely=0.85, relwidth=0.2, relheight=0.1)


        #self.text_label.append(tk.Label(self, text = NewLocPage.text1 , font = XMEDIUM_FONT ,relief="ridge", borderwidth = 1))
        #self.text_label[0].place(relx = 0.05, rely = 0.1, relwidth = 0.9, relheight = 0.7)


    def Confirm_Frame(self, text):
        text_label = tk.Label(self, text = text, font = XMEDIUM_FONT ,relief="ridge", borderwidth = 1)
        text_label.place(relx = 0.05, rely = 0.1, relwidth = 0.9, relheight = 0.7)


    def Confirm_Click(self):
        #add everything to database and make calculation
        if StartPage.new_or_old_entery == 1:
            #calculations
            number_of_locations = len(self.all_valid_locations)
            matrix_loc_to_loc = sdc.create_matrix_of_pair_names(number_of_locations, self.all_valid_locations)
            matrix_length_distance_between_loc = sdc.create_matrix_length_between_each_location_using_array(number_of_locations, matrix_loc_to_loc)
            all_diffenet_paths = sdc.creates_matrix_with_posible_paths(number_of_locations)
            total_length_of_all_paths = sdc.creates_matrix_with_lengths_of_paths(all_diffenet_paths, matrix_length_distance_between_loc)
            what_way_is_shortest, minimum_distance = sdc.shortest_Root(total_length_of_all_paths, all_diffenet_paths)
            what_way_is_shortest_name = sdc.replaces_Poins_With_Name(number_of_locations, what_way_is_shortest, matrix_loc_to_loc)

            #print("shortest distance is "+ str(what_way_is_shortest_name))
            #print(minimum_distance)

            #To database
            name = NameOfInput.name_of_input
            loc_text = db.convert_list_to_text(self.all_valid_locations)
            loc_loc_text = db.convert_matrix_to_text(matrix_loc_to_loc)
            distance_between_loc_tex = db.convert_matrix_to_text(matrix_length_distance_between_loc)
            shortest_distance_text = db.convert_list_to_text(what_way_is_shortest_name)

            db.crete_table()
            db.insert_locations(name, loc_text, loc_loc_text, distance_between_loc_tex, shortest_distance_text, minimum_distance)

            #gives the shortest distance to ShortestDistance page
            ShortestDistancePage.shortest_distance_list = what_way_is_shortest_name
            ShortestDistancePage.shortest_distance_km = minimum_distance
        elif StartPage.new_or_old_entery == 0:
            ShortestDistancePage.shortest_distance_list = PreviusLocationsPage.shortest_distance_list
            ShortestDistancePage.shortest_distance_km = PreviusLocationsPage.shortest_distance_km

        self.controller.Show_Frame(ShortestDistancePage)



    def Make_Changes_Click(self, all_valid_locations):
        if StartPage.new_or_old_entery == 1:
            self.controller.Show_Frame(ChangeLocPage)
            #ChangeLocPage(self.parent, self.controller, all_valid_locations)
            #ChangeLocPage.all_valid_locations = all_valid_locations
            #ChangeLocPage.Confirm_Frame(parent, text)

            """
            #next = ChangeLocPage(self.parent, self.controller, all_valid_locations)
            s = ChangeLocPage(self.parent, self.controller, all_valid_locations)
            s.all_valid_locations = all_valid_locations
            self.controller.Show_Frame(ChangeLocPage)
            s.Generate_Information
            ChangeLocPage.all_valid_locations = all_valid_locations
            #next.Generate_Information()
            """
class ChangeLocPage(tk.Frame):
    all_valid_locations = []


    def __init__(self, parent, controller, all_valid_locations):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller


        self.all_entery_ent = []
        self.all_labels_ent = []
        self.all_remove_btn_ent = []
        self.all_valid_locations = all_valid_locations
        ChangeLocPage.all_valid_locations = all_valid_locations

        main_label = tk.Label(self, text = "Selected Locations: ", font = LARGE_FONT)
        main_label.place(relx = 0, rely = 0.05, relwidth = 0.3, relheight = 0.05)


        home_btn = ttk.Button(self, text = "Home", command = self.Go_Home_Click)
        home_btn.place(relx = 0.8, rely = 0.05, relwidth = 0.15, relheight = 0.05)

        self.select_btn = ttk.Button(self, text = "Load", command = self.Generate_Information)
        self.select_btn.place(relx = 0.6, rely = 0.05, relwidth = 0.15, relheight = 0.05)

    def Go_Home_Click(self):
        NewLocPage.all_valid_locations = []
        NewLocPage.all_entered_locations = []
        NameOfInput.name_of_input = ""
        #Run_App()
        self.controller.Show_Frame(StartPage)

    def Generate_Information(self):
        self.select_btn["state"] = tk.DISABLED
        #cosmetic
        Y_BETWEEN_ENT = 0.055
        X_BETWEEN_ENT = 0.5
        X_BETWEEN_ENT_PAIR = 0.2

        ii = 0
        for i in range(len(self.all_valid_locations)):

            if i == 0:

                self.all_labels_ent.append(tk.Label(self, text="Location " + str(i + 1) + ":"))
                self.all_labels_ent[i].place(relx=0, rely=0.15, relwidth=0.2, relheight=0.05)

                self.all_entery_ent.append(tk.Entry(self))
                self.all_entery_ent[i].insert(0, self.all_valid_locations[i])
                self.all_entery_ent[i].place(relx=X_BETWEEN_ENT_PAIR, rely=0.15, relwidth=0.2, relheight=0.05)

            elif not i >= int(len(self.all_valid_locations)) / 2:

                self.all_labels_ent.append(tk.Label(self, text="Location " + str(i + 1) + ":"))
                self.all_labels_ent[i].place(relx=0, rely=0.15 + (Y_BETWEEN_ENT * i), relwidth=0.2, relheight=0.05)

                self.all_entery_ent.append(tk.Entry(self))
                self.all_entery_ent[i].insert(0, self.all_valid_locations[i])
                self.all_entery_ent[i].place(relx=X_BETWEEN_ENT_PAIR, rely=0.15 + (Y_BETWEEN_ENT * i), relwidth=0.2,
                                             relheight=0.05)

            else:

                self.all_labels_ent.append(tk.Label(self, text="Location " + str(i + 1) + ":"))
                self.all_labels_ent[i].place(relx=X_BETWEEN_ENT, rely=0.15 + (Y_BETWEEN_ENT * ii), relwidth=0.2,
                                             relheight=0.05)

                self.all_entery_ent.append(tk.Entry(self))
                self.all_entery_ent[i].insert(0, self.all_valid_locations[i])
                self.all_entery_ent[i].place(relx=X_BETWEEN_ENT_PAIR + X_BETWEEN_ENT, rely=0.15 + (Y_BETWEEN_ENT * ii),
                                             relwidth=0.2, relheight=0.05)
                ii += 1

        save_btn = ttk.Button(self, text = "SAVE", command= self.generate_shortest_root_click)
        save_btn.place(relx = 0.2, rely = 0.94, relwidth = 0.3, relheight = 0.05)

        del_shootest_root_btn = ttk.Button(self, text = "DELETE ENTERY", command = "PLACEHOLDER")
        del_shootest_root_btn.place(relx = 0.6, rely = 0.94, relwidth = 0.2, relheight = 0.05)

    def generate_shortest_root_click(self):
        valid_locations = []
        for i in range(len(self.all_entery_ent)):
            valid_locations.append(self.all_entery_ent[i].get())



        list = {""}
        for i in range(len(valid_locations)):
            list.add(valid_locations[i])

        list.remove("")
        list = sorted(list)
        self.all_valid_locations = list
        ChangeLocPage.all_valid_locations = list
        NewLocPage.all_valid_locations = list
        text = ""

        for i in range(len(self.all_valid_locations)):
            if i % 5 == 0 and i != 0:
                text += str(self.all_valid_locations[i]) + "\n"
            elif i == len(self.all_valid_locations):
                text += str(self.all_valid_locations[i])
            else:
                text += str(self.all_valid_locations[i]) + ", "

        ConfirmLocationsPage(self.parent, self.controller, self.all_valid_locations)
        self.controller.Show_Frame(ConfirmLocationsPage)
        ConfirmLocationsPage.Confirm_Frame(self.parent, text)



class ShortestDistancePage(tk.Frame):

    shortest_distance_list = []
    shortest_distance_km = 0
    def __init__(self, parent, controller, all_valid_locations):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller
        self.all_valid_locations = all_valid_locations

        text = ""
        if len(ShortestDistancePage.shortest_distance_list)>0:
            for i in range(len(ShortestDistancePage.shortest_distance_list)):
                if i == len(ShortestDistancePage.shortest_distance_list) -1:
                    text += ShortestDistancePage.shortest_distance_list[i]
                elif i % 3 == 0 and i != 0:
                    text += ShortestDistancePage.shortest_distance_list[i] + " -\n"
                else:
                    text += ShortestDistancePage.shortest_distance_list[i] + " - "

        shortest_distance_list_label_1 = tk.Label(self, text = "Shortest Distance Is The Path", font = XLARGE_FONT)
        shortest_distance_list_label_1.place(relx = 0.05, rely = 0.05, relwidth = 0.9, relheight = 0.05)
        shortest_distance_list_label_2 = tk.Label(self, text=text, font=LARGE_FONT)
        shortest_distance_list_label_2.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.45)

        shortest_distance_km_label_1 = tk.Label(self, text = "Shortest Distance Is(km): " + str(ShortestDistancePage.shortest_distance_km), font = LARGE_FONT, bg = "gray")
        shortest_distance_km_label_1.place(relx = 0.01, rely = 0.5, relwidth = 0.5, relheight = 0.1)

        open_google_maps_btn = ttk.Button(self, text ="Open Maps", command =self.open_google_maps_click)
        open_google_maps_btn.place(relx = 0.05, rely = 0.85, relwidth = 0.2, relheight = 0.1)

        #shortest_distance_km_label_2 = tk.Label(self, text=ShortestDistancePage.shortest_distance_km, font=LARGE_FONT)
        #shortest_distance_km_label_2.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.1)


    def open_google_maps_click(self):
        #open up google maps and type in the locations
        pass



class PreviusLocationsPage(tk.Frame):
    previous_locations_list = ["Select Name of File"]
    shortest_distance_list = []
    shortest_distance_km = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        self.drop_down_list = ttk.Combobox(self, value = PreviusLocationsPage.previous_locations_list)
        self.drop_down_list.set(PreviusLocationsPage.previous_locations_list[0])
        self.drop_down_list.place(relx = 0.05, rely = 0.05, relwidth = 0.7, relheight = 0.05)

        select_btn = ttk.Button(self, text = "Select", command = self.select_click)
        select_btn.place(relx=0.8, rely=0.05, relwidth=0.15, relheight=0.05)


    def select_click(self):
        if self.drop_down_list.get() != "Select Name of File":
            name_of_file = self.drop_down_list.get()
            records = db.get_location_name("'"+name_of_file+"'")
            shortest_dist_text = records[4]
            shortest_dist_list = []
            beg_index = 0
            end_index = 0

            #uses database and makes the shortest distance into list
            for i in range(len(shortest_dist_text)):
                if shortest_dist_text[i] == "-":
                    if beg_index == 0:
                        end_index = i
                        shortest_dist_list.append(shortest_dist_text[beg_index:end_index])
                        beg_index = i+1
                    else:
                        beg_index = i+1

                elif shortest_dist_text[i] == ",":
                    end_index = i
                    shortest_dist_list.append(shortest_dist_text[beg_index:end_index])

                elif i == len(shortest_dist_text)-1:
                    shortest_dist_list.append(shortest_dist_text[beg_index:])


            text = ""
            for i in range(len(shortest_dist_list)):
                if i % 5 == 0 and i != 0:
                    text += str(shortest_dist_list[i]) + "\n"
                elif i == len(shortest_dist_list) - 1:
                    text += str(shortest_dist_list[i])
                else:
                    text += str(shortest_dist_list[i]) + ", "


            PreviusLocationsPage.shortest_distance_km = records[5]
            PreviusLocationsPage.shortest_distance_list = shortest_dist_list
            self.controller.Show_Frame(ConfirmLocationsPage)
            ConfirmLocationsPage.Confirm_Frame(self.parent, text)

    def find_all_file_names(self):
        names_raw = db.query_name()
        names = []

        for i in range(len(names_raw)):
            if i == 0:
                names.append("Select Name of File")
            for ii in range(len(names_raw[i])):
                if ii == 0:
                    names.append(names_raw[i][ii])
                elif ii % 2 == 0:
                    names.append(names_raw[i][ii])


        PreviusLocationsPage.previous_locations_list = names


        #load_btn = ttk.Button(self, text = "Load")




def Run_App():
    app1 = MainClass()
    app1.mainloop()


Run_App()


#entery = NewLocPage.all_entered_locations
#print(entery)
















