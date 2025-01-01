import json

def overwrite():
    """
    This function orchestrates the overwriting process of various data files.
    
    It calls three helper functions to overwrite specific sets of files:
    - __overwrite_ardu(): Overwrites Arduino-related data files.
    - __overwrite_obiekt(): Overwrites object-related data files.
    - __overwrite_przebiegi(): Overwrites the 'przebiegi.json' file, setting it as an empty list.
    """
    __overwrite_ardu()  # Overwrite Arduino files
    __overwrite_obiekt()  # Overwrite object-related files
    __overwrite_przebiegi()  # Overwrite the 'przebiegi.json' file

def __overwrite_ardu():
    """
    Overwrites Arduino-related data files.

    This function copies a list of files from the 'databases/arduino_res/' folder to 
    the 'databases/arduino/' folder, effectively overwriting them with the corresponding files.
    """
    # List of Arduino-related JSON files
    file_list = [
        'C1.json', 'C2.json', 'C3.json', 'L1.json', 'L2.json', 'L3.json', 'P1.json', 'P2.json', 
        'P3.json', 'P4.json', 'W1.json', 'W2.json', 'W3.json', 'W4.json', 'W5.json'
    ]
    
    # Combine file paths for two folders: 'obiekty' and 'plytki'
    folder_list = []
    for x in file_list:
        folder_list.append('obiekty/' + x)
    for x in file_list:
        folder_list.append('plytki/' + x)

    # Overwrite each file from 'databases/arduino_res/' to 'databases/arduino/'
    for x in folder_list:
        with open('databases/arduino_res/' + x, 'r') as source:
            with open('databases/arduino/' + x, 'w') as target:
                json.dump(json.load(source), target, indent=6)

def __overwrite_obiekt():
    """
    Overwrites object-related data files.

    This function copies object-related files from the 'databases/cechy_res/' folder to 
    the 'databases/cechy/' folder, effectively overwriting them.
    """
    # List of object-related JSON files
    file_list = [
        'obiekty_zmienne_odcinki.json', 'obiekty_zmienne.json', 'okna.json', 'przyciski.json'
    ]

    # Overwrite each file from 'databases/cechy_res/' to 'databases/cechy/'
    for x in file_list:
        with open('databases/cechy_res/' + x, 'r') as source:
            with open('databases/cechy/' + x, 'w') as target:
                json.dump(json.load(source), target, indent=6)

def __overwrite_przebiegi():
    """
    Overwrites the 'przebiegi.json' file with an empty list.

    This function clears the content of the 'przebiegi.json' file by writing an empty list to it.
    """
    with open('databases/przebiegi/przebiegi.json', 'w') as target:
        json.dump([], target, indent=6)
