import json
import serial as sr
import time
PRINT = False

class sender:
    """
    Class responsible for sending data to Arduino boards. It generates the communication code
    and sends it over the available COM ports.
    """

    def __init__(self):
        """
        Initializes default lists and variables.
        - arduino_pin_list: list of Arduino pin names.
        - list_ards: list of specific Arduino board names.
        - ready_code: a variable that will hold the final communication code.
        """
        self.ardu_pin_list = ["A0","A1","A2","A3","A4","A5","A6","A7","D2","D3","D4","D5","D6","D7","D8","D9"]
        self.list_ards = ["C1","C2","C3","L1","L2","L3","P1","P2","P3","P4"]
        self.ready_code = ''

    def run(self):
        """
        Main function that runs the Arduino update algorithm.
        1. Creates the communication code.
        2. Loads the COM addresses.
        3. Sends the generated code.
        """
        self._code_maker()              # 1. Creating a code
        self._portCom()                 # 2. Loading COM addresses
        #self._activate_outs()           # 3. Initialisation of OUT ports in Python
        self._send()                    # 4. Sending code
        #self._deactivate_outs()         # 5. Deactivation

    def _convert_all(self):
        """
        Converts all Arduino board data into a common format for communication.
        It combines the data from each Arduino board into a list of code elements.
        """
        tab = []  # List to store the output

        # Loop through all Arduino board names and convert the data
        for x in self.list_ards:    
            tab.append(self._aggregate_plytka(self._get_jsn(x)))

        return tab  # Return the combined list

    def _get_jsn(self, name):
        """
        Loads a JSON file with board data and returns it as a dictionary.
        """
        retDict = {}  # Dictionary to hold the loaded data
        adr = "databases/arduino/plytki/"+name+".json"  # Path to the JSON file

        # Load the dictionary from the JSON file
        with open(adr, 'r') as file: 
            retDict = json.load(file)

        return retDict  # Return the loaded dictionary

    def _aggregate_plytka(self, dict):
        """
        Aggregates data from the Arduino pin configurations into a specific format.
        It organizes data in a list of pin configurations for each Arduino board.
        """
        tab_ret = [[False,[]],[False,[]],[False,[]],[False,[]]]  # Temporary list for pin data

        # Assign pin states for each part of the board
        tab_ret[0][0] = dict["symb_pin"][0]
        for x in ["D5","D4","D3","D2"]:     
            tab_ret[0][1].append(dict[x])
        tab_ret[1][0] = dict["symb_pin"][1]
        for x in ["D9","D8","D7","D6"]:     
            tab_ret[1][1].append(dict[x])
        tab_ret[2][0] = dict["symb_pin"][2]
        for x in ["A3","A2","A1","A0"]:     
            tab_ret[2][1].append(dict[x])
        tab_ret[3][0] = dict["symb_pin"][3]
        for x in ["A7","A6","A5","A4"]:     
            tab_ret[3][1].append(dict[x])

        # Convert pin values and reverse polarization
        for i in range(len(tab_ret)):   
            tab_ret[i][1] = self.__konwerter_na_16(self._reverse_polarisation(tab_ret[i][1]))
        
        return dict["strona"], tab_ret  # Return the formatted data

    def _code_maker(self):
        """
        Creates the final communication code by combining all board codes.
        The code consists of a header, board data, and a footer.
        """
        tab = self._convert_all()  # Get all the board data
        code = '$$$$'  # Start of the code
        for x in tab:
            code = code + x[0] + x[0]  # Append the board identifier
            for i in range(4):
                code += '##' + x[1][i][0] + x[1][i][1] + '&&'  # Append pin data
        code += 'ZZZZ'  # End of the code
        self.ready_code = code  # Store the final code

    def __konwerter_na_16(self, tab_2):
        """
        Converts binary pin states into hexadecimal characters.
        """
        # Conversion from binary to hexadecimal
        if (type(tab_2[0])==chr):
            for i in range(4):
                tab_2[i] = int(tab_2[i])
        if tab_2 == [0,0,0,0]: return '0'
        if tab_2 == [0,0,0,1]: return '1'
        if tab_2 == [0,0,1,0]: return '2'
        if tab_2 == [0,0,1,1]: return '3'
        if tab_2 == [0,1,0,0]: return '4'
        if tab_2 == [0,1,0,1]: return '5'
        if tab_2 == [0,1,1,0]: return '6'
        if tab_2 == [0,1,1,1]: return '7'
        if tab_2 == [1,0,0,0]: return '8'
        if tab_2 == [1,0,0,1]: return '9'
        if tab_2 == [1,0,1,0]: return 'A'
        if tab_2 == [1,0,1,1]: return 'B'
        if tab_2 == [1,1,0,0]: return 'C'
        if tab_2 == [1,1,0,1]: return 'D'
        if tab_2 == [1,1,1,0]: return 'E'
        if tab_2 == [1,1,1,1]: return 'F'

    def _portCom(self):
        """
        Loads the available COM addresses from a text file.
        The COM addresses will be used to communicate with the Arduino boards.
        """
        self.adresy_COM = []  # List to store COM addresses

        # Helper function to clean empty spaces from the COM address
        def clean(line):
            outLine = ''
            for x in line:
                if x not in [' ', '\n']: outLine += x
            return outLine

        # Load COM addresses from a text file
        with open('databases/adresy_COM/adresy_COM.txt', 'r') as file:
            self.adresy_COM = file.readlines()

        # Clean each COM address and store it in the list
        for i in range(len(self.adresy_COM)):   
            self.adresy_COM[i] = clean(self.adresy_COM[i])

    def _reverse_polarisation(self, list):
        """
        Reverses the binary symbols: 0 -> 1, 1 -> 0.
        """
        outList = []  # List to store the reversed binary values
        for x in list:
            if x == 0: outList.append(1)
            else: outList.append(0)

        return outList  # Return the reversed list

    def _activate_outs(self):
        """
        Opens the serial ports for communication.
        """
        for i in range(len(self.adresy_COM)):   
            self.adresy_COM[i] = sr.Serial(self.adresy_COM[i], 115200, timeout=2)

    def _deactivate_outs(self):
        """
        Closes the serial ports after communication.
        """
        for i in range(len(self.adresy_COM)):    
            self.adresy_COM[i].close()

    def _send(self):
        """
        Sends the generated communication code to the Arduino boards over the COM ports.
        """
        self.ready_code = self.ready_code + '\n'  # Append newline to the code
        self._sendLine(self.ready_code)  # Send the code

    def _sendLine(self, x):
        """
        Sends the code line by line to each COM port.
        """
        ready_code = x
        k = 5
        r = len(ready_code) % k
        # Add padding if needed
        for n in range(r): ready_code += 'Z'
        
        # Send the code in chunks of 'k' characters
        for n in range(0, len(ready_code), k):
            try:
                toWrite = ''
                for m in range(k):
                    toWrite += ready_code[n+m]
                if PRINT: print(toWrite)  # Optionally print the code being sent
                time.sleep(0.001)  # Small delay between sends
            except: pass
