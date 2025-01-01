# Utils Folder

This folder contains utility scripts that serve various purposes in the project. These utilities are designed to simplify and optimize specific tasks, such as file operations, timing, and validation. Below is an overview of the scripts contained in this folder:

## Contents

### 1. `licznik.py`
This script includes a function to handle time delays.

#### Functions:
- `count_three_half()`: Pauses the execution of the program for 3.5 seconds and then returns `True`. This function is useful when a delay of 3.5 seconds is required in the program and ensures that the delay has passed.

### 2. `not_empty.py`
This script checks whether a specific JSON file contains any data.

#### Functions:
- `is_not_empty()`: Reads the `przebiegi.json` file from the `databases/przebiegi/` directory and returns `True` if the file contains any data. If the file is empty, it returns `False`.

### 3. `reset.py`
This script is responsible for overwriting various data files in the project. It orchestrates the process of resetting data by replacing existing files with their predefined templates.

#### Functions:
- `overwrite()`: Calls three internal functions to overwrite specific sets of files:
  - `__overwrite_ardu()`: Overwrites Arduino-related data files.
  - `__overwrite_obiekt()`: Overwrites object-related data files.
  - `__overwrite_przebiegi()`: Clears and overwrites the `przebiegi.json` file.

- `__overwrite_ardu()`: Overwrites Arduino-related JSON files in the `databases/arduino/` directory using source files from `databases/arduino_res/`.

- `__overwrite_obiekt()`: Overwrites object-related JSON files in the `databases/cechy/` directory using source files from `databases/cechy_res/`.

- `__overwrite_przebiegi()`: Clears the `przebiegi.json` file by overwriting it with an empty list.

