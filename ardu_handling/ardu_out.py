import json
import serial as sr
import time

class sender:
    """
    This class handles the process of sending generated commands to Arduino boards.
    It prepares the communication data, manages serial communication ports,
    and sends the data to the boards.
    """

    def __init__(self):
        """
        Initializes the default lists and the 'ready_code' string.
        It also defines the list of Arduino pin names and board identifiers.
        """
        self.ardu_pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9"]
        self.list_ards = ["C1", "C2", "C3", "L1", "L2", "L3", "P1", "P2", "P3", "P4"]
        self.ready_code = ''

    def run(self):
        """
        Main function to run the Arduino update process:
        1. Create code using _code_maker()
        2. Load COM addresses using _portCom()
        3. Initialize serial ports using _activate_outs()
        4. Send the generated code using _send()
        5. Deactivate ports using _deactivate_outs()
        """
        self._code_maker()            # Step 1: Create the code
        self._portCom()               # Step 2: Load COM addresses
        self._activate_outs()         # Step 3: Initialize serial communication
        self._send()                  # Step 4: Send the code
        self._deactivate_outs()       # Step 5: Deactivate the serial ports

    def _convert_all(self):
        """
        Converts the codes for all Arduino boards and returns them in a common table.
        
        Each board's configuration is processed by _aggregate_plytka and combined into one table.
        """
        tab = []  # Initialize the output list
        for x in self.list_ards:
            tab.append(self._aggregate_plytka(self._get_jsn(x)))  # Aggregate board data
        return tab

    def _get_jsn(self, name):
        """
        Loads a JSON file for a given Arduino board and returns the dictionary.
        
        The file contains pin configurations and other settings for the board.
        """
        retDict = {}
        adr = "databases/arduino/plytki/" + name + ".json"  # Path to the board's JSON file
        with open(adr, 'r') as file:
            retDict = json.load(file)  # Load the JSON file into a dictionary
        return retDict

    def _aggregate_plytka(self, dict):
        """
        Aggregates data from the board configuration (pins and symbols) into a new format.
        
        Each board has 4-pin sections, and this function processes each pin group.
        After processing, the data is converted into a different format (from binary to octal).
        """
        tab_ret = [[False, []], [False, []], [False, []], [False, []]]  # Temporary list to hold 4-pin data
        
        # Processing the pins for each section
        tab_ret[0][0] = dict["symb_pin"][0]
        for x in ["D5", "D4", "D3", "D2"]:
            tab_ret[0][1].append(dict[x])
        
        tab_ret[1][0] = dict["symb_pin"][1]
        for x in ["D9", "D8", "D7", "D6"]:
            tab_ret[1][1].append(dict[x])
        
        tab_ret[2][0] = dict["symb_pin"][2]
        for x in ["A3", "A2", "A1", "A0"]:
            tab_ret[2][1].append(dict[x])
        
        tab_ret[3][0] = dict["symb_pin"][3]
        for x in ["A7", "A6", "A5", "A4"]:
            tab_ret[3][1].append(dict[x])
        
        # Convert and reverse the polarity of the pins' binary representation
        for i in range(len(tab_ret)):
            tab_ret[i][1] = self.__konwerter_na_16(self._reverse_polarisation(tab_ret[i][1]))
        
        return dict["strona"], tab_ret  # Return the board's page and the processed pin data

    def _code_maker(self):
        """
        Generates the full code string by combining the data from all boards.
        
        The generated code includes the board names, pin symbols, and their states.
        """
        tab = self._convert_all()  # Get all the processed board data
        code = '$$$$'  # Start of the code
        for x in tab:
            code = code + x[0] + x[0]  # Add the board identifier (repeated twice)
            for i in range(4):
                # Append pin state data for each 4-pin section
                code += '##' + x[1][i][0] + x[1][i][1] + '&&'
        code += 'ZZZZ'  # End of the code
        self.ready_code = code  # Store the final generated code

    def __konwerter_na_16(self, tab_2):
        """
        Converts a binary list (4 elements) into a hexadecimal string.
        
        The binary list represents values from 0000 to 1111 and is converted to corresponding hexadecimal.
        """
        if (type(tab_2[0]) == chr):
            for i in range(4):
                tab_2[i] = int(tab_2[i])  # Convert characters to integers if necessary
        
        # Convert from binary to hexadecimal
        hex_dict = {
            (0, 0, 0, 0): '0', (0, 0, 0, 1): '1', (0, 0, 1, 0): '2', (0, 0, 1, 1): '3',
            (0, 1, 0, 0): '4', (0, 1, 0, 1): '5', (0, 1, 1, 0): '6', (0, 1, 1, 1): '7',
            (1, 0, 0, 0): '8', (1, 0, 0, 1): '9', (1, 0, 1, 0): 'A', (1, 0, 1, 1): 'B',
            (1, 1, 0, 0): 'C', (1, 1, 0, 1): 'D', (1, 1, 1, 0): 'E', (1, 1, 1, 1): 'F'
        }
        return hex_dict[tuple(tab_2)]  # Convert the list to a hexadecimal string

    def _portCom(self):
        """
        Loads the available COM port addresses from a text file.
        
        The text file contains a list of serial port addresses used for communication with Arduino boards.
        """
        self.adresy_COM = []  # Initialize the list of COM addresses

        def clean(line):
            """
            Cleans up the line from unnecessary spaces or newlines.
            """
            outLine = ''
            for x in line:
                if x not in [' ', '\n']:
                    outLine += x
            return outLine  # Return cleaned line

        # Read COM addresses from the text file and clean each line
        with open('databases/adresy_COM/adresy_COM.txt', 'r') as file:
            self.adresy_COM = file.readlines()
        for i in range(len(self.adresy_COM)):
            self.adresy_COM[i] = clean(self.adresy_COM[i])  # Clean each COM address

    def _reverse_polarisation(self, list):
        """
        Reverses the binary symbols (0->1 and 1->0).
        
        This is used to invert the logic state of the pins.
        """
        outList = []
        for x in list:
            if x == 0:
                outList.append(1)  # Invert 0 to 1
            else:
                outList.append(0)  # Invert 1 to 0
        return outList

    def _activate_outs(self):
        """
        Initializes serial communication by opening all the COM ports.
        
        This allows communication with Arduino boards connected to the serial ports.
        """
        for i in range(len(self.adresy_COM)):
            self.adresy_COM[i] = sr.Serial(self.adresy_COM[i], 115200, timeout=2)

    def _deactivate_outs(self):
        """
        Closes the serial communication ports after usage.
        
        This ensures that all resources are freed up properly.
        """
        for i in range(len(self.adresy_COM)):
            self.adresy_COM[i].close()

    def _send(self):
        """
        Sends the generated `ready_code` to the Arduino boards via serial communication.
        
        It first adds a newline character and then calls `_sendLine()` to send the data in chunks.
        """
        self.ready_code = self.ready_code + '\n'  # Add newline character
        self._sendLine(self.ready_code)  # Send the code line by line

    def _sendLine(self, x):
        """
        Sends the code line by line in chunks of 5 characters.
        
        This approach helps avoid communication errors by managing the data in smaller portions.
        """
        ready_code = x
        ready_code = ready_code.encode()  # Convert the code to bytes
        for x in self.adresy_COM:
            x = sr.Serial(x, 115200)  # Initialize the serial port
            k = 5  # Chunk size
            r = len(ready_code) % k
            for n in range(r):
                ready_code += 'Z'  # Padding with 'Z' to complete the chunk
            for n in range(0, len(ready_code), k):
                try:
                    toWrite = ''
                    for m in range(k):
                        toWrite += ready_code[n + m]
                    x.write(toWrite.encode())  # Send the chunk
                    time.sleep(0.001)  # Small delay between chunks
                except:
                    pass  # Ignore any errors during sending
            x.close()  # Close the serial port after sending
