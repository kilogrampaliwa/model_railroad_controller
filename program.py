import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk
from PIL import Image, ImageTk
import buttons_mask
import nastawy_semaforow
import przebiegi
import utils
import program_utils
import object_changing

output_ON = False

def Y(): return 350

przebiegi_lista = []

class ImageSwitchApp:

    def __init__(self, root, bg_path, bg_up_path, bg_dw_path):
        self.root = root
        self.root.title("Image Switch App")

        utils.overwrite()
        self.blink = False

        self.__temp_sem_przebieg = False

        self._button_to_seq = []

        self.list_of_sem = ['A', 'B', 'C', 'D', 'G', 'H', 'I', 'J', 'K', 'L', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']
        self.list_of_seg = ['CL1','LC1','LC2','LL1','LL2','LL4','PC4','PP4','PP2','PP1','PC1','PC2','CP1','CC10','CC1','CC2','CC3','CC4','CC6','CC8','PC104','PC108','LL10','LL45','P104','PC21','PC31','PC42','PC64','PC86','LC245','LC454','LC12','LC13','LC21','LC46','LC68']

        self.__wykrawam = przebiegi.wyklucz()

        self._potential_seq= [[False, False],[]]

        self.__sem_nastawy = nastawy_semaforow.nastawy()

        # Load background image
        self.bg_image = Image.open(bg_path)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_up_image = Image.open(bg_up_path)
        self.bg_up_image = ImageTk.PhotoImage(self.bg_up_image)
        self.bg_dw_image = Image.open(bg_dw_path)
        self.bg_dw_image = ImageTk.PhotoImage(self.bg_dw_image)

        # Create canvas with background image
        self.canvas = tk.Canvas(self.root, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_up_image)
        self.canvas.create_image(0, Y(), anchor=tk.NW, image=self.bg_dw_image)

        # Load photos and their coordinates
        self.objects_parameters = program_utils.load_json("databases/cechy/obiekty_zmienne.json")
        self.objects_coordinates = program_utils.load_json("databases/lokalizacje/obiekty_dynamiczne.json")

        #create objects
        self.photos_info = []
        for x in self.objects_parameters.keys():
            self.photos_info.append([self.objects_parameters[x]['type'], self.objects_coordinates[x], self.objects_parameters[x]['blinking'], self.objects_parameters[x]['visibility'], x])

        #create button
        self.buttons_parameters = program_utils.load_json("databases/cechy/przyciski.json")
        self.buttons_coordinates = program_utils.load_json("databases/lokalizacje/przyciski.json")
        #create objects
        self.buttons = []
        self.buttons_info = []
        for x in self.buttons_parameters.keys():
            self.buttons_info.append([x, self.buttons_parameters[x]['address'], self.buttons_coordinates[x], self.buttons_parameters[x]['visibility'], self.buttons_parameters[x]['action']])

        self.load_and_display_photos()
        self.load_and_display_buttons()
        # Schedule photo switching
        self.root.after(1000, self.switch_photo)

    def load_and_display_photos(self):

        self.objects_parameters = program_utils.load_json("databases/cechy/obiekty_zmienne.json")
        # Load photos
        self.photos = []

        for photo_info in self.photos_info:

            photo_path, photo_coords, blink, visibility, res = photo_info
            if  visibility:
                if len(photo_path)==3:
                    if res in ['A', 'B', 'C', 'D', 'R', 'S', 'T', 'U', 'V', 'W']:
                        photo = Image.open("databases/"+photo_path[0])
                        photo = ImageTk.PhotoImage(photo)
                        self.photos.append((photo, [photo_coords[0],photo_coords[1]+Y()]))
                        photo = Image.open("databases/"+photo_path[1])
                        photo = ImageTk.PhotoImage(photo)
                        self.photos.append((photo, [photo_coords[0]+12,photo_coords[1]+Y()]))
                        photo = Image.open("databases/"+photo_path[2])
                        photo = ImageTk.PhotoImage(photo)
                        self.photos.append((photo, [photo_coords[0]+36,photo_coords[1]+Y()]))
                    else:
                        photo = Image.open("databases/"+photo_path[0])
                        photo = ImageTk.PhotoImage(photo)
                        self.photos.append((photo, [photo_coords[0]+48,photo_coords[1]+Y()]))
                        photo = Image.open("databases/"+photo_path[1])
                        photo = ImageTk.PhotoImage(photo)
                        self.photos.append((photo, [photo_coords[0]+24,photo_coords[1]+Y()]))
                        photo = Image.open("databases/"+photo_path[2])
                        photo = ImageTk.PhotoImage(photo)
                        self.photos.append((photo, [photo_coords[0],photo_coords[1]+Y()]))
                else:
                    photo = Image.open("databases/"+photo_path)
                    photo = ImageTk.PhotoImage(photo)
                    self.photos.append((photo, [photo_coords[0],photo_coords[1]+Y()]))

        # Display background
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_up_image)
        self.canvas.create_image(0, 350, anchor=tk.NW, image=self.bg_dw_image)

        # Display photos on canvas
        for photo, coords in self.photos:
            self.canvas.create_image(coords[0], coords[1], anchor=tk.NW, image=photo)

        # Display the initial photo
        #self.current_photo = self.photos[0]

    def load_and_display_buttons(self, mask_not_dafeault=False, known_buttons=False):
        # Load photos

        self._potential_seq, self.list_of_seg, to_load =przebiegi.color_seqs(self._potential_seq, self.list_of_seg)
        self.load_and_display_photos()

        if self.buttons!=[]:
            for x in self.buttons.keys():
                self.buttons[x]['button'].place_forget()

        self.buttons = {}
        self.buttons = {}
        mask=[]
        if mask_not_dafeault:
            mask = buttons_mask.give_buttons(mask_not_dafeault, known_buttons)

            zajete = []
            for x in przebiegi_lista:
                for y in x.show_elements(): zajete.append(y)
            mask = self.__wykrawam.weryfikuj(mask, zajete, self.__temp_sem_przebieg)
        else:
            if utils.is_not_empty():  mask = buttons_mask.give_buttons('Default(full)')
            else:                   mask = buttons_mask.give_buttons('Default(empty)')

        for button_info in self.buttons_info:

            name, photo_path, photo_coords, visibility,  action = button_info
            if  name in mask and visibility:
                row = {}
                row["rw_image"] = Image.open("databases/"+photo_path)
                row["tk_image"] = ImageTk.PhotoImage(row["rw_image"])
                if name[1]=='g':    row["coords"] = photo_coords
                else:    row["coords"] = [photo_coords[0],photo_coords[1]+Y()]
                row["action"] = action
                if row["action"] in ['0', 0, False]:
                    row["button"] = tk.Button(self.canvas, image=row["tk_image"])
                elif row["action"].split(' ')[0]=="przycisk":
                    row_splitted = row["action"].split(' ')
                    if   row_splitted[1] == 'sem':
                        if   row_splitted[2] == "A": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("A"))
                        elif row_splitted[2] == "B": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("B"))
                        elif row_splitted[2] == "C": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("C"))
                        elif row_splitted[2] == "D": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("D"))
                        elif row_splitted[2] == "G": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("G"))
                        elif row_splitted[2] == "H": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("H"))
                        elif row_splitted[2] == "I": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("I"))
                        elif row_splitted[2] == "J": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("J"))
                        elif row_splitted[2] == "K": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("K"))
                        elif row_splitted[2] == "L": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("L"))
                        elif row_splitted[2] == "R": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("R"))
                        elif row_splitted[2] == "S": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("S"))
                        elif row_splitted[2] == "T": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("T"))
                        elif row_splitted[2] == "U": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("U"))
                        elif row_splitted[2] == "V": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("V"))
                        elif row_splitted[2] == "W": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("W"))
                        elif row_splitted[2] == "Y": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("Y"))
                        elif row_splitted[2] == "Z": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_sem("Z"))
                    elif row_splitted[1] == 'tor':
                        if   row_splitted[2] == "p_LL1": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_LL1"))
                        elif row_splitted[2] == "p_LL2": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_LL2"))
                        elif row_splitted[2] == "p_LL3": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_LL45"))
                        elif row_splitted[2] == "p_LL4": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_LL4"))
                        elif row_splitted[2] == "p_PP1": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_PP1"))
                        elif row_splitted[2] == "p_PP2": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_PP2"))
                        elif row_splitted[2] == "p_LC1": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_LC1"))
                        elif row_splitted[2] == "p_LC2": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_LC2"))
                        elif row_splitted[2] == "p_LC3": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_LC3"))
                        elif row_splitted[2] == "p_LC4": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_LC4"))
                        elif row_splitted[2] == "p_LC6": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_LC6"))
                        elif row_splitted[2] == "p_LC8": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_LC8"))
                        elif row_splitted[2] == "p_PC1": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_PC1"))
                        elif row_splitted[2] == "p_PC2": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_PC2"))
                        elif row_splitted[2] == "p_PC3": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_PC3"))
                        elif row_splitted[2] == "p_PC4": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_PC4"))
                        elif row_splitted[2] == "p_PC6": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_PC6"))
                        elif row_splitted[2] == "p_PC8": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._choose_tor("p_PC8"))
                elif row["action"].split(' ')[0]=="usn_przy":
                    row_splitted = row["action"].split(' ')
                    if   row_splitted[2] == "A":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_A"))
                    elif row_splitted[2] == "B":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_B"))
                    elif row_splitted[2] == "C":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_C"))
                    elif row_splitted[2] == "D":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_D"))
                    elif row_splitted[2] == "G":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_G"))
                    elif row_splitted[2] == "H":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_H"))
                    elif row_splitted[2] == "I":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_I"))
                    elif row_splitted[2] == "J":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_J"))
                    elif row_splitted[2] == "K":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_K"))
                    elif row_splitted[2] == "L":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_L"))
                    elif row_splitted[2] == "R":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_R"))
                    elif row_splitted[2] == "S":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_S"))
                    elif row_splitted[2] == "T":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_T"))
                    elif row_splitted[2] == "U":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_U"))
                    elif row_splitted[2] == "V":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_V"))
                    elif row_splitted[2] == "W":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_W"))
                    elif row_splitted[2] == "Y":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_Y"))
                    elif row_splitted[2] == "Z":     row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._del_pg("p_Z"))
                elif row["action"].split(' ')[0]=="g_pop":
                    if   row["action"].split(' ')[1]=='sem':
                        if   row["action"].split(' ')[2] == 'A': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'A'))
                        elif row["action"].split(' ')[2] == 'B': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'B'))
                        elif row["action"].split(' ')[2] == 'C': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'C'))
                        elif row["action"].split(' ')[2] == 'D': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'D'))
                        elif row["action"].split(' ')[2] == 'G': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'G'))
                        elif row["action"].split(' ')[2] == 'H': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'H'))
                        elif row["action"].split(' ')[2] == 'I': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'I'))
                        elif row["action"].split(' ')[2] == 'J': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'J'))
                        elif row["action"].split(' ')[2] == 'K': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'K'))
                        elif row["action"].split(' ')[2] == 'L': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'L'))
                        elif row["action"].split(' ')[2] == 'R': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'R'))
                        elif row["action"].split(' ')[2] == 'S': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'S'))
                        elif row["action"].split(' ')[2] == 'T': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'T'))
                        elif row["action"].split(' ')[2] == 'U': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'U'))
                        elif row["action"].split(' ')[2] == 'V': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'V'))
                        elif row["action"].split(' ')[2] == 'W': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'W'))
                        elif row["action"].split(' ')[2] == 'Y': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'Y'))
                        elif row["action"].split(' ')[2] == 'Z': row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("sem_D", 'Z'))
                    elif row["action"].split(' ')[1]=='zwr':
                        if   row["action"].split(' ')[2] == "z1" : row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z1" ))
                        elif row["action"].split(' ')[2] == "z5" : row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z5" ))
                        elif row["action"].split(' ')[2] == "z15": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z15"))
                        elif row["action"].split(' ')[2] == "z12": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z12"))
                        elif row["action"].split(' ')[2] == "z24": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z24"))
                        elif row["action"].split(' ')[2] == "z27": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z27"))
                        elif row["action"].split(' ')[2] == "z3" : row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z3" ))
                        elif row["action"].split(' ')[2] == "z26": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z26"))
                        elif row["action"].split(' ')[2] == "z2" : row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z2" ))
                        elif row["action"].split(' ')[2] == "z25": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z25"))
                        elif row["action"].split(' ')[2] == "z28": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z28"))
                        elif row["action"].split(' ')[2] == "z10": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z10"))
                        elif row["action"].split(' ')[2] == "z11": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z11"))
                        elif row["action"].split(' ')[2] == "z16": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z16"))
                        elif row["action"].split(' ')[2] == "z17": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z17"))
                        elif row["action"].split(' ')[2] == "z7" : row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("zwr", "z7" ))
                        elif row["action"].split(' ')[2] == "z4ab" : row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("krz", "z4ab"))
                        elif row["action"].split(' ')[2] == "z4cd" : row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("krz", "z4cd"))
                        elif row["action"].split(' ')[2] == "z9ab" : row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("krz", "z9ab"))
                        elif row["action"].split(' ')[2] == "z9cd" : row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("krz", "z9cd"))
                        elif row["action"].split(' ')[2] == "z18ab": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("krz", "z18ab"))
                        elif row["action"].split(' ')[2] == "z18cd": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("krz", "z18cd"))
                        elif row["action"].split(' ')[2] == "z19ab": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("krz", "z19ab"))
                        elif row["action"].split(' ')[2] == "z19cd": row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("krz", "z19cd"))
                        else:
                            row["button"] = tk.Button(self.canvas, image=row["tk_image"])
                    elif row["action"].split(' ')[1]=='tmn':
                        if   row["action"].split(' ')[2] == "Tm1" :    row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("tmn","Tm1" ))
                        elif row["action"].split(' ')[2] == "Tm12":    row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("tmn","Tm12"))
                        elif row["action"].split(' ')[2] == "Tm11":    row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("tmn","Tm11"))
                        elif row["action"].split(' ')[2] == "Tm10":    row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("tmn","Tm10"))
                        elif row["action"].split(' ')[2] == "Tm4" :    row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("tmn","Tm4" ))
                        elif row["action"].split(' ')[2] == "Tm41":    row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._g_pop("tmn","Tm41"))
                elif row["action"].split(' ')[0]=="popup":
                    if   row["action"].split(' ')[1]=="Akc":
                        row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._popup("Akc"))
                    elif row["action"].split(' ')[1]=="Anl":
                        row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._popup("Anl"))
                    elif row["action"].split(' ')[1]=="NDr":
                        row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._popup("NDr"))
                    elif row["action"].split(' ')[1]=="Mod":
                        row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._popup("Mod"))
                    elif row["action"].split(' ')[1]=="Stp":
                        row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._popup("Stp"))
                    elif row["action"].split(' ')[1]=="Usn":
                        row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._popup("Usn"))
                    elif row["action"].split(' ')[1]=="Zak":
                        row["button"] = tk.Button(self.canvas, image=row["tk_image"], command = lambda: self._popup("Zak"))
                    else:
                        row["button"] = tk.Button(self.canvas, image=row["tk_image"])

                self.buttons[name] = row.copy()
                self.buttons[name]["button"].place(x=row["coords"][0],y=row["coords"][1])

    def switch_photo(self):

        self._potential_seq, self.list_of_seg, to_load =przebiegi.color_seqs(self._potential_seq, self.list_of_seg)
        self.load_and_display_photos()

        program_utils.send_ardu(output_ON)
        # Hide the current photo
        self.canvas.delete(tk.ALL)

        if self.blink: self.blink=False
        else: self.blink=True
        # Switch to the next photo
        self.photos_info = []
        for x in self.objects_parameters.keys():
            if isinstance(self.objects_parameters[x]['blinking'],bool):
                if self.objects_parameters[x]['blinking'] and self.blink:
                    self.photos_info.append([self.objects_parameters[x]['possible_types'][0], self.objects_coordinates[x], self.objects_parameters[x]['blinking'], self.objects_parameters[x]['visibility'], 'reserve'])
                else:
                    self.photos_info.append([self.objects_parameters[x]['type'], self.objects_coordinates[x], self.objects_parameters[x]['blinking'], self.objects_parameters[x]['visibility'], 'reserve'])
            else:
                table = []
                for n in range(3):
                    if self.objects_parameters[x]['blinking'][n] and self.blink:
                        table.append(self.objects_parameters[x]['possible_types'][n][0])
                    else:
                        table.append(self.objects_parameters[x]['type'][n])
                self.photos_info.append([table, self.objects_coordinates[x], self.objects_parameters[x]['blinking'], self.objects_parameters[x]['visibility'], x])

        self.load_and_display_photos()

        # Schedule the next photo switch
        self.root.after(1000, self.switch_photo)

    def _popup(self, type):
        #Create an instance of Tkinter frame
        win = tk.Tk()
        #Set the geometry of Tkinter frame
        win.geometry("400x300")

        def action_Akc():
            self.load_and_display_buttons()
            win.destroy()
        def action_Anl():
            self.load_and_display_buttons()
            self._potential_seq = [[False, False], []]
            self.__temp_sem_przebieg = False
            win.destroy()
        def action_NDr():
            self.load_and_display_buttons('newLine')
            win.destroy()
        def action_Mod():
            self.load_and_display_buttons()
            win.destroy()
        def action_Stp():
            self.load_and_display_buttons()
            win.destroy()
        def action_Usn():
            odcinki_z_json_osobno = object_changing.podwojne(program_utils.load_json('databases/przebiegi/przebiegi.json'), 0)
            odcinki_z_json = []
            for x in odcinki_z_json_osobno:
                for y in x: odcinki_z_json.append(y)
            self.load_and_display_buttons('delete', object_changing.all_sem(odcinki_z_json))
            win.destroy()
        def action_Zak():
            self._potential_seq = przebiegi.accept_seq(self._potential_seq)
            self.__temp_sem_przebieg = False
            self.load_and_display_buttons()
            win.destroy()
        def action_Non_Pg():
            self._potential_seq = przebiegi.reject_seq(self._potential_seq)
            action_Non()
        def action_Non():
            win.destroy()

        #Create a button in the main Window to open the popup
        if   type=='Akc':
            tk.Label(win, text="Czy akceptujesz zmiany?", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "Tak", command=action_Akc).pack()
            ttk.Button(win, text= "Nie", command=action_Non).pack()
        elif type=='Anl':
            tk.Label(win, text="Chcesz anulowac akcje?", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "Tak", command=action_Anl).pack()
            ttk.Button(win, text= "Nie", command=action_Non).pack()
        elif type=='NDr':
            tk.Label(win, text="Czy chcesz wyznaczyc nowy przebieg?", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "Tak", command=action_NDr).pack()
            ttk.Button(win, text= "Nie", command=action_Non).pack()
        elif type=='Mod':
            tk.Label(win, text="Are you sure?", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "Tak", command=action_Mod).pack()
            ttk.Button(win, text= "Nie", command=action_Non).pack()
        elif type=='Stp':
            tk.Label(win, text="Akceptujesz zatrzymanie?", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "Tak", command=action_Stp).pack()
            ttk.Button(win, text= "Nie", command=action_Non).pack()
        elif type=='Usn':
            tk.Label(win, text="Czy chcesz usunac przebieg?", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "Tak", command=action_Usn).pack()
            ttk.Button(win, text= "Nie", command=action_Non).pack()
        elif type=='Zak':
            tk.Label(win, text="Czy akceptujesz przebieg?", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "Tak", command=action_Zak).pack()
            ttk.Button(win, text= "Nie", command=action_Non_Pg).pack()
        win.mainloop()

    def _g_prev_sem_check(self, which: str, toChange:list):

        table = program_utils.load_json('databases/cechy/obiekty_zmienne.json')


        table = program_utils.load_json('databases/cechy/obiekty_zmienne.json')
        table[which]['type'][0] = table[which]['possible_types'][0][toChange[0][0]]
        table[which]['type'][2] = table[which]['possible_types'][2][toChange[2][0]]
        table[which]['blinking'][0] = toChange[0][1]
        table[which]['blinking'][2] = toChange[2][1]
        if 'blinking_one' not in table[which]:  table[which]['blinking_one'] = ['','','']
        if table[which]['blinking'][0]:
            if    table[which]['type'][0]==table[which]['possible_types'][0][0]: table[which]['blinking_one'][0] = table[which]['type'][0]
            else: table[which]['blinking_one'][0] = table[which]['type'][0]
        if table[which]['blinking'][2]:
            if    table[which]['type'][2]==table[which]['possible_types'][2][0]: table[which]['blinking_one'][2] = table[which]['type'][0]
            else: table[which]['blinking_one'][2] = table[which]['type'][2]
        program_utils.save_json('databases/cechy/obiekty_zmienne.json', table)

    def _g_pop(self, type, name, prev=0):
        #Create an instance of Tkinter frame
        win = tk.Tk()
        #Set the geometry of Tkinter frame
        win.geometry("400x300")

        def action_sem_D(v):
            win.destroy()
            self._g_pop('sem_G', name, v)
        def action_sem_G(v):
            win.destroy()
            self._g_pop('sem_B', name, [prev, v])
        def action_sem_B(v):
            win.destroy()
            object_changing.change_object('sem', name, object_changing.sem_numsig([v, prev[0], prev[1]]))

            # zmiana w pierwszym semaforze jeśli zachodzi w drugim
            if name not in ["A", "B", "C", "D", "Y", "Z"]:
                for x in przebiegi_lista:
                    flag = False
                    pgs_temp = x.show_pgs().copy()
                    for y in pgs_temp:
                        if len(y)==2:
                             if y[0]==name:
                                print(True,  y, "   ", name)
                                flag = y
                             else:              print(False, y, "   ", name)
                    if flag:
                        pgs_temp.remove(y)
                        for y in pgs_temp:
                            self._g_prev_sem_check(y[0], object_changing.sem_numsig([v, prev[0], prev[0]]))
        def action_zwr(n):
            win.destroy()
            object_changing.change_object('zwr', name, n)
        def action_krz(n):
            win.destroy()
            object_changing.change_object('krz', name, n)
        def action_tmn(m):
            win.destroy()
            object_changing.change_object('tmn', name, m)

        #Create a button in the main Window to open the popup
        if   type=='sem_D':
            tk.Label(win, text="Wybierz predkosc dolnej komory.", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "V max", command=lambda: action_sem_D(4)).pack()
            ttk.Button(win, text= "100km/h", command=lambda: action_sem_D(3)).pack()
            ttk.Button(win, text= "60km/h", command=lambda: action_sem_D(2)).pack()
            ttk.Button(win, text= "40km/h", command=lambda: action_sem_D(1)).pack()
            ttk.Button(win, text= "Stoj", command=lambda: action_sem_D(0)).pack()
        elif   type=='sem_G' and prev!=0:
            tk.Label(win, text="Wybierz predkosc gornej komory.", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "V max", command=lambda: action_sem_G(4)).pack()
            ttk.Button(win, text= "100km/h", command=lambda: action_sem_G(3)).pack()
            ttk.Button(win, text= "40-60km/h", command=lambda: action_sem_G(2)).pack()
            ttk.Button(win, text= "Stoj", command=lambda: action_sem_G(1)).pack()
        elif   type=='sem_G' and prev==0:
            action_sem_G(0)
        elif   type=='sem_B':
            tk.Label(win, text="Swiatlo biale.", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "Wlacz", command=lambda: action_sem_B(1)).pack()
            ttk.Button(win, text= "Wylacz", command=lambda: action_sem_B(0)).pack()
        elif type=='zwr':
            tk.Label(win, text="Wybierz kierunek zwrotnicy", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "Prosto", command=lambda: action_zwr(0)).pack()
            ttk.Button(win, text= "W bok", command=lambda: action_zwr(1)).pack()
        elif type=='krz':
            text_krz = f"Wybierz kierune {name[-2:]} rozjazdu krz. {name[:-2]}"
            tk.Label(win, text=text_krz, font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "Prosto", command=lambda: action_krz(0)).pack()
            ttk.Button(win, text= "W bok", command=lambda: action_krz(1)).pack()
        elif type=='tmn':
            tk.Label(win, text="Wybierz wskazanie tarczy manewrowej", font=('Helvetica 14 bold')).pack(pady=20)
            ttk.Button(win, text= "Ms1", command=lambda: action_tmn(1)).pack()
            ttk.Button(win, text= "Ms2", command=lambda: action_tmn(2)).pack()

        win.mainloop()


    def _choose_sem(self, sem, nowy = True):

        if nowy:
            nowy_przebieg = przebiegi.przebieg()
            przebiegi_lista.append(nowy_przebieg)
        self.__temp_sem_przebieg = sem
        possibles = przebiegi.pg_to_objects.give_possible(sem)
        self.load_and_display_buttons('lineTor', possibles)

    def _choose_tor(self, tor):

        t2 = False

        if '\n' in tor: tor = tor[:-1]
        if '\n' in  self.__temp_sem_przebieg: self.__temp_sem_przebieg = self.__temp_sem_przebieg[:-1]

        if 'p_' in tor: tor=tor.split('_')[1]
        if self.__temp_sem_przebieg:
            przebiegi_lista[-1].add_pg(self.__temp_sem_przebieg, tor)
            t2  =  self.__temp_sem_przebieg 
            self.__temp_sem_przebieg = False
        pgs = przebiegi_lista[-1].show_pgs()

        if self._potential_seq[0][0]: self._potential_seq[0][1] = t2+tor[-1]#pgs[1]
        else:           self._potential_seq[0][0]= pgs[0]

        elem = przebiegi_lista[-1].show_elements()
        for x in elem:  self._potential_seq[1].append(x)

        if tor in ['PP1', 'PP2', 'LL1', 'LL2', 'LL3', 'LL4']:
            self.load_and_display_buttons('lineSem', 'end')
        else:
            possibles = przebiegi.pg_to_objects.give_possible(tor)
            przeb = program_utils.load_json('databases/przebiegi/przebiegi.json')
            przeb_zb = []
            for x in przeb:
                for y in x[1]: przeb_zb.append(y)
            possibles2 = []
            for x in possibles:
                trig = True

                elementy = przebiegi.pg_to_objects.give_objects(x+tor[-1], [])
                elem = []

                try:
                    for y in elementy[1:]:
                        for z in y: elem.append(z)

                    for y in elem:
                        if y in przeb_zb: trig=False
                    if trig: possibles2.append(x)
                except: print(f"Brak mozliwych {tor}")

            possibles3 = []
            for x in possibles2: possibles3.append(object_changing.sem_to_but(x))
            if x in ['A','B','C','D']:  self.__temp_sem_przebieg = object_changing.number_to_sem(tor[-1], 'CL')
            else : self.__temp_sem_przebieg = object_changing.number_to_sem(tor[-1], 'CP')

            self.load_and_display_buttons('lineSem', possibles3)

    def _del_pg(self, przy):
    
        #issem : bool
        print(przy)
        if '_' in przy: przy = przy.split('_')[1]
        print(przy)
        przebiegi_json_full = program_utils.load_json('databases/przebiegi/przebiegi.json')
        przebiegi_json = object_changing.podwojne(przebiegi_json_full, 0)

        for i, n in enumerate(przebiegi_json):
            lista_n = object_changing.all_sem(n)
            if przy in lista_n:
                for x in lista_n: object_changing.zero_sem(x)
                przebiegi_json_full.remove(przebiegi_json_full[i])

        program_utils.save_json('databases/przebiegi/przebiegi.json', przebiegi_json_full)
    
        self.load_and_display_buttons()


if __name__ == "__main__":
    root = tk.Tk()

    # Provide the background image path and a list of photos information as arguments
    bg_path = "databases/obrazy/static/background.png"
    bg_up_path = "databases/obrazy/static/panelGorny.png"
    bg_dw_path = "databases/obrazy/static/tlo.png"
    dynamicObjectsParameters_address = "databases/cechy/obiekty_zmienne.json"
    dynamicObjectsLocalisation_address = "databases/lokalizacje/obiekty_dynamiczne.json"


    app = ImageSwitchApp(root, bg_path, bg_up_path, bg_dw_path)

    root.mainloop()
