import json
import ardu_handling.ardu_template

class actu:
    """
    The `actu` class is responsible for managing the states of Arduino-controlled objects,
    including initializing data structures, loading data from JSON files, updating states,
    and saving these states back to JSON files.
    """

    def __init__(self):
        """
        Initializes default lists and loads data into the main dictionary (`dict_ards`).

        Attributes:
        - ardu_pin_list: List of Arduino pins used in the system.
        - list_ards: List of Arduino identifiers.
        - dict_ards: Dictionary holding the state of each Arduino and its objects.
        """
        self.ardu_pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9"]
        self.list_ards = ["C1", "C2", "C3", "L1", "L2", "L3", "P1", "P2", "P3", "P4"]

        self.dict_ards = {
            "C1": [], "C2": [], "C3": [], "L1": [], "L2": [], "L3": [],
            "P1": [], "P2": [], "P3": [], "P4": []
        }

        self.get_info()

    def get_info(self):
        """
        Loads data for each Arduino from corresponding JSON files and populates the main dictionary (`dict_ards`).
        """
        for x in self.list_ards:
            # Load data from JSON file
            with open(f"databases/arduino/obiekty/{x}.json", 'r') as file:
                from_jsn = json.load(file)

            # Append an Arduino template object to the dictionary
            self.dict_ards[x].append(ardu_handling.ardu_template.arduino(x, from_jsn["strona"], from_jsn["symb_pin"]))

            # Create a dictionary for pin states and populate it
            objects = {pin: "0" for pin in self.ardu_pin_list}
            for y in self.ardu_pin_list:
                objects[y] = from_jsn[y]

            self.dict_ards[x].append(objects)

    def update_states(self):
        """
        Main function that updates the states of all objects and saves the updates to JSON files.

        Steps:
        1. Loads states from object JSONs (via `get_raw_states`).
        2. Encrypts states for Arduino output (via `restate_raw`).
        3. Saves the states into Arduino pin JSONs (via `update_jsons`).
        """
        self.get_raw_states()
        self.restate_raw()
        self.update_jsons()

    def get_raw_states(self):
        """
        Loads states of objects from a JSON file and interprets their states, filling the `raw_states` attribute.
        """
        self.raw_states = {
            # Default states for various objects
            'A': [False, False, False], 'B': [False, False, False],
            'C': [False, False, False], 'D': [False, False, False],
            'G': [False, False, False], 'H': [False, False, False],
            'I': [False, False, False], 'J': [False, False, False],
            'K': [False, False, False], 'L': [False, False, False],
            'R': [False, False, False], 'S': [False, False, False],
            'T': [False, False, False], 'U': [False, False, False],
            'V': [False, False, False], 'W': [False, False, False],
            'Y': [False, False, False], 'Z': [False, False, False],
            'z1': [], 'z2': [], 'z3': [], 'z5': [], 'z7': [],
            'z10': [], 'z11': [], 'z16': [], 'z17': [], 'z24': [],
            'z25': [], 'z26': [], 'z27': [], 'z12': [], 'z15': [],
            'z28': [], 'z4': [], 'z9': [], 'z18': [], 'z19': [],
            'Tm1': [], 'Tm11': [], 'Tm12': [], 'Tm10': [], 'Tm4': [],
            'Tm41': []
        }

        with open("databases/cechy/obiekty_zmienne.json", 'r') as file:
            from_file = json.load(file)

        self.__list_of_sem = ['A', 'B', 'C', 'D', 'G', 'H', 'I', 'J', 'K', 'L', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']
        self.__list_of_tm = ['Tm1', 'Tm11', 'Tm12', 'Tm10', 'Tm4', 'Tm41']
        self.__list_of_zwr = ['z1', 'z2', 'z3', 'z5', 'z7', 'z10', 'z11', 'z16', 'z17', 'z24', 'z25', 'z26', 'z27', 'z12', 'z15', 'z28']
        self.__list_of_krz = ['z4', 'z9', 'z18', 'z19']

        def which_state(n):
            """
            Determines the state index based on the type of the object and its possible states.
            """
            for i, possible_type in enumerate(from_file[n]['possible_types']):
                if from_file[n]['type'] == possible_type:
                    return i

        # Update states for semaphores
        for x in self.__list_of_sem:
            self.raw_states[x][0] = which_state(x) if not from_file[x]['blinking'][0] else 0
            self.raw_states[x][1] = which_state(x) if not from_file[x]['blinking'][1] else 0
            self.raw_states[x][2] = which_state(x) if not from_file[x]['blinking'][2] else 0

        # Update states for other objects
        for x in self.__list_of_tm:
            self.raw_states[x] = which_state(x)
        for x in self.__list_of_zwr:
            self.raw_states[x] = which_state(x)
        for x in self.__list_of_krz:
            self.raw_states[x] = which_state(x)

    def restate_raw(self):
        """
        Encrypts raw states into binary output for Arduino pinouts.
        """
        # Functions to encode states
        def sem_to_tab(tab):
            return [tab[0], tab[1] == 2, tab[1] == 1, tab[2] == 1, tab[2] == 2]

        def zwr_to_tab(state):
            return [state == 1, state == 0]

        def tmn_to_tab(state):
            return [state == 1, state == 2]

        for n in list(self.raw_states.keys()):
            if n in self.__list_of_sem:
                self.raw_states[n] = sem_to_tab(self.raw_states[n])
            elif n in self.__list_of_zwr:
                self.raw_states[n] = zwr_to_tab(self.raw_states[n])
            elif n in self.__list_of_tm:
                self.raw_states[n] = tmn_to_tab(self.raw_states[n])

    def update_jsons(self):
        """
        Saves encrypted states into JSON files for Arduino pins.
        """
        for x in self.list_ards:
            print(f"NAME START --------------------------------- >>>> {x}")
            temp_dict = self.load_json(x, True)
            temp_chck = self.load_json(x, False)

            pins_chck = {k:v for k,v in temp_chck.items() if k not in ['strona', 'symb_pin']}

            for n in temp_dict.keys():
                if n in self.ardu_pin_list and pins_chck[n][0] not in [0, '0']:
                    try:
                        for i,y in enumerate(self.raw_states[pins_chck[n][0]]):
                            if y==None: self.raw_states[pins_chck[n][0]][i]=False
                        temp_dict[n] = self.raw_states[pins_chck[n][0]]
                    except:
                        if   pins_chck[n][0] in ['z4ab','z4cd']:

                            temp_dict[n] = self.__krzZwr('z4', self.raw_states)['z4ab']
                            temp_dict[n] = self.__krzZwr('z4', self.raw_states)['z4cd']

                        elif pins_chck[n][0] in  ['z9ab','z9cd']:

                            temp_dict[n] = self.__krzZwr('z9', self.raw_states)['z9ab']
                            temp_dict[n] = self.__krzZwr('z9', self.raw_states)['z9cd']

                        elif pins_chck[n][0] in ['z18ab','z18cd']:

                            temp_dict[n] = self.__krzZwr('z18', self.raw_states)['z18ab']
                            temp_dict[n] = self.__krzZwr('z18', self.raw_states)['z18cd']

                        elif pins_chck[n][0] in ['z19ab','z19cd']:

                            temp_dict[n] = self.__krzZwr('z19', self.raw_states)['z19ab']
                            temp_dict[n] = self.__krzZwr('z19', self.raw_states)['z19cd']

            print(f"self.save_json(x, temp_dict) ... {temp_dict}")
            print(f"NAME STOP --------------------------------- >>>> {x}")
            self.save_json(x, self.__toBytes(temp_dict, pins_chck))

    def load_json(self, name, czy_plytki):
        with open(f"databases/arduino/{'plytki' if czy_plytki else 'obiekty'}/{name}.json", 'r') as file:
            return json.load(file)

    def save_json(self, name, data):
        with open(f"databases/arduino/plytki/{name}.json", 'w') as file:
            json.dump(data, file, indent=6)

    def __krzZwr(self, nazwa, states):
        zwr_dict = {}
        if   str(states[nazwa]) == '0':
            zwr_dict[f'{nazwa}ab'] = [True, False]
            zwr_dict[f'{nazwa}cd'] = [True, False]
        elif str(states[nazwa]) == '1':
            zwr_dict[f'{nazwa}ab'] = [True, False]
            zwr_dict[f'{nazwa}cd'] = [False, True]
        elif str(states[nazwa]) == '2':
            zwr_dict[f'{nazwa}ab'] = [False, True]
            zwr_dict[f'{nazwa}cd'] = [False, True]
        elif str(states[nazwa]) == '3':
            zwr_dict[f'{nazwa}ab'] = [False, True]
            zwr_dict[f'{nazwa}cd'] = [True, False]
        return zwr_dict
    
    def __toBytes(self, tempDict, tempCheck):
        outDict = {}
        print(f"tempCheck : {tempCheck}")
        for k, v in tempDict.items():
            if k not in ['strona', 'symb_pin']:
                try:
                    if   tempCheck[k][1]== "B" :
                        print(v)
                        outDict[k] = int(v[0])
                    elif tempCheck[k][1]== "Pd":
                        print(v)
                        outDict[k] = int(v[1])
                    elif tempCheck[k][1]== "C" :
                        print(v)
                        outDict[k] = int(v[2])
                    elif tempCheck[k][1]== "Pg":
                        print(v)
                        outDict[k] = int(v[3])
                    elif tempCheck[k][1]== "Z" :
                        print(v)
                        outDict[k] = int(v[4])

                    elif tempCheck[k][1]== "0" :
                        outDict[k] = 0

                    elif tempCheck[k][1]== "L" :
                        print(v)
                        outDict[k] = int(v[0])
                    elif tempCheck[k][1]== "P" :
                        print(v)
                        outDict[k] = int(v[0])

                    elif tempCheck[k][1]== "N" :
                        print(v)
                        outDict[k] = int(v[1])
                except:
                    if   v in [0, '0', False]:
                        outDict[k] = 0
                    elif v in [1, '1', True]:
                        outDict[k] = 1

        outDict['strona'] = tempDict['strona']
        outDict['symb_pin'] = tempDict['symb_pin']
        return outDict