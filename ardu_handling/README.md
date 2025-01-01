 # Arduino Pin Manager
 
 ## Overview
 
 The `Arduino Pin Manager` is a Python-based system designed to manage and control the pin configurations of Arduino boards. The system allows reading, writing, and updating pin states through JSON configuration files. It provides a way to interact with the boards, configure their pins, and communicate with them through serial communication.
 
 ## Classes Overview
 
 ### 1. **`sender` class**
 The `sender` class manages the process of preparing and sending commands to Arduino boards via serial communication. It includes methods for generating the code that will be sent, managing serial ports, and sending the data to the Arduino boards.
 
 - **Key Methods**:
   - `run()`: Main function to run the update process for the boards.
   - `_code_maker()`: Generates the full code string by combining data from all boards.
   - `_convert_all()`: Converts and aggregates data from all Arduino boards.
   - `_portCom()`: Loads available COM addresses from a text file.
   - `_activate_outs()`: Initializes serial communication by opening all COM ports.
   - `_send()`: Sends the generated code to the boards via serial communication.
   
 ### 2. **`arduino` class**
 The `arduino` class represents an individual Arduino board and allows interaction with its pin configurations. It loads, updates, and saves data to a JSON file for each board, allowing users to configure and manage pin states.
 
 - **Key Methods**:
   - `__init__(nazwa, strona, symb_pinow)`: Initializes an Arduino object with board name, side, and pin symbol configuration.
   - `przypisz_stan(pin, stan)`: Assigns a state (True/False or 1/0) to a specified pin and saves the new state.
   - `daj_stan_pinow()`: Returns the current states of all pins on the board.
   - `daj_strone()`: Returns the side of the board (P, L, or C).
   - `daj_symb_pinow()`: Returns the symbol configuration for the board's pins.
   - `daj_nazwe()`: Returns the name of the Arduino board.
 
 ## File Structure
 
 - `databases/arduino/plytki/`: Contains JSON files for each Arduino board, representing their pin configurations and states.
   - Each JSON file includes:
     - Pin names (e.g., "A0", "D2", "D5") and their associated states (True/False).
     - Symbol configurations for the pins (e.g., `symb_pin`).
     - Side information (e.g., `strona`) indicating the physical side of the board (P, L, or C).
 
 - `databases/adresy_COM/`: Contains the COM addresses used for serial communication with the Arduino boards.
 
 ## Usage Example
 
 ### 1. **Creating an `arduino` Object**
 
 To create and interact with an Arduino object, instantiate it with the board name, side, and symbol configuration:
 
 ```python
 from arduino import arduino
 
 # Initialize an Arduino board object
 board = arduino('C1', 'P', ['A0', 'A1', 'A2', 'A3'])
 ```
 
 ### 2. **Updating Pin States**
 
 You can update the state of a pin on the Arduino board using the `przypisz_stan()` method:
 
 ```python
 # Set pin D2 to HIGH (True or 1)
 board.przypisz_stan('D2', 1)
 ```
 
 ### 3. **Getting Pin States**
 
 To get the current state of all pins:
 
 ```python
 # Get all pin states
 pin_states = board.daj_stan_pinow()
 print(pin_states)
 ```
 
 ### 4. **Sending Commands to Arduino**
 
 Use the `sender` class to send the generated code to the Arduino boards:
 
 ```python
 from sender import sender
 
 # Initialize the sender object
 sender_obj = sender()
 
 # Run the process to send the commands to all Arduino boards
 sender_obj.run()
 ```
 
 ## Configuration Files
 
 The JSON files located in the `databases/arduino/plytki/` directory are essential for the configuration of the boards. Each file should have the following structure:
 
 ```json
 {
     "symb_pin": ["symbol1", "symbol2", "symbol3", "symbol4"],
     "strona": "P",
     "A0": true,
     "A1": false,
     "A2": true,
     "A3": false,
     "A4": true,
     "A5": false,
     "A6": true,
     "A7": false,
     "D2": true,
     "D3": false,
     "D4": true,
     "D5": false,
     "D6": true,
     "D7": false,
     "D8": true,
     "D9": false
 }
 ```
 
 Each Arduino board has its unique JSON file that contains the pin configuration, symbols, and side (strona). You can edit these files to configure the board's pins as needed.
 
 ## Requirements
 
 - Python 3.x
 - pySerial (`pip install pyserial`)
 
