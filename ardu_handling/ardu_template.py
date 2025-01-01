import json as jsn


class arduino:
    """
    The 'arduino' class represents an Arduino board and its associated properties.
    It allows interaction with the board's pins and configurations by loading
    and saving data to/from a JSON file.
    """

    def __init__(self, nazwa: str, strona: str, symb_pinow: str):
        """
        Initializes an Arduino object with the following attributes:
        - name:                self.__nazwa (name of the Arduino board)
        - pin-dictionary:      self.__slownik (dictionary of pin states)
        - side:                self.__strona (the side of the board, typically 'P', 'L', or 'C')
        
        The constructor also loads the board's pin configuration from a JSON file and saves the new data.
        """
        # saving name of the Arduino board
        self.__nazwa = nazwa

        # loading actual pin configuration data from the JSON file
        self.__wczytaj_json()

        # saving side and pin symbol configuration, overwriting in case of mistakes
        self.__strona = strona
        self.__symb_pinow = symb_pinow

        # saving updated data back to the JSON file
        self.__zapisz_json()

    def __wczytaj_json(self):
        """
        Loads the current pin configuration and side from the JSON file associated
        with the specific Arduino board.
        """
        # temporary dictionary to store the JSON data
        __dict_0 = {}
        # opening the JSON file containing board configuration
        with open("databases/arduino/plytki/"+self.__nazwa+".json", 'r') as __file:
            __dict_0 = jsn.load(__file)

        # updating the pin dictionary of the board (e.g., A0, A1, D2, etc.)
        self.__slownik = {
            "A0" : __dict_0["A0"],
            "A1" : __dict_0["A1"],
            "A2" : __dict_0["A2"],
            "A3" : __dict_0["A3"],
            "A4" : __dict_0["A4"],
            "A5" : __dict_0["A5"],
            "A6" : __dict_0["A6"],
            "A7" : __dict_0["A7"],
            "D2" : __dict_0["D2"],
            "D3" : __dict_0["D3"],
            "D4" : __dict_0["D4"],
            "D5" : __dict_0["D5"],
            "D6" : __dict_0["D6"],
            "D7" : __dict_0["D7"],
            "D8" : __dict_0["D8"],
            "D9" : __dict_0["D9"]
        }

        # updating the symbol and side information
        self.__symb_pinow = __dict_0["symb_pin"]
        self.__strona = __dict_0["strona"]

    def __zapisz_json(self):
        """
        Saves the current state of the Arduino board (pin configurations, side, symbols)
        to its respective JSON file.
        """
        # temporary dictionary to store current configuration data
        __dict = {}
        with open("databases/arduino/plytki/"+self.__nazwa+".json", 'r') as __file:
            __dict = jsn.load(__file)

        # updating the symbol and side information in the JSON
        __dict["symb_pin"] = self.__symb_pinow
        __dict["strona"] = self.__strona

        # overwriting pin states in the JSON (e.g., A0, A1, D2, etc.)
        __dict["A0"] = self.__slownik["A0"]
        __dict["A1"] = self.__slownik["A1"]
        __dict["A2"] = self.__slownik["A2"]
        __dict["A3"] = self.__slownik["A3"]
        __dict["A4"] = self.__slownik["A4"]
        __dict["A5"] = self.__slownik["A5"]
        __dict["A6"] = self.__slownik["A6"]
        __dict["A7"] = self.__slownik["A7"]
        __dict["D2"] = self.__slownik["D2"]
        __dict["D3"] = self.__slownik["D3"]
        __dict["D4"] = self.__slownik["D4"]
        __dict["D5"] = self.__slownik["D5"]
        __dict["D6"] = self.__slownik["D6"]
        __dict["D7"] = self.__slownik["D7"]
        __dict["D8"] = self.__slownik["D8"]
        __dict["D9"] = self.__slownik["D9"]

        # saving updated configuration back to the JSON file
        with open("databases/arduino/plytki/"+self.__nazwa+".json", "w") as jsonFile:
            jsn.dump(__dict, jsonFile, sort_keys=True, indent=4)

    def przypisz_stan(self, pin, stan):
        """
        Assigns a state (True/False or 1/0) to a specified pin on the Arduino board.
        Updates the pin's state in the internal dictionary and saves the updated state to the JSON file.
        
        Parameters:
        - pin: The pin name (e.g., 'A0', 'D3')
        - stan: The state of the pin (True or False, or 1 or 0)
        """
        # converting boolean state to integer (True -> 1, False or None -> 0)
        if stan == True:
            stan = 1
        if stan == False or stan == None:
            stan = 0

        # updating the pin state in the internal dictionary and saving the new state to the JSON
        self.__slownik[pin] = stan
        self.__zapisz_json()

    def daj_stan_pinow(self):
        """
        Returns the current states of all pins on the Arduino board.
        
        It reloads the pin configurations from the JSON file before returning the pin states.
        """
        self.__wczytaj_json()
        return self.__slownik

    def daj_strone(self):
        """
        Returns the side of the Arduino board (P, L, or C).
        """
        return self.__strona

    def daj_symb_pinow(self):
        """
        Returns the symbol configuration for the pins on the Arduino board.
        """
        return self.__symb_pinow

    def daj_nazwe(self):
        """
        Returns the name of the Arduino board.
        """
        return self.__nazwa
