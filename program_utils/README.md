# program_utils

The `program_utils` folder contains utility modules for handling JSON files and communicating with an Arduino device. Below is a detailed description of the functionality of each module.

---

## Files

### 1. `jsons_handling.py`

The `jsons_handling.py` module provides functions for working with JSON files.

#### Functions:
- **`load_json(file_path)`**  
  Loads data from a JSON file and returns it as a Python object.  
  **Parameters:**  
  - `file_path` *(str)*: Path to the JSON file.  
  **Returns:**  
  - A Python object (e.g., dict, list) containing the data from the JSON file.

- **`save_json(path, json_dat)`**  
  Saves data in JSON format to a file.  
  **Parameters:**  
  - `path` *(str)*: Path where the JSON file will be saved.  
  - `json_dat` *(object)*: Data to be saved (e.g., dict, list).

---

### 2. `send_ardu.py`

The `send_ardu.py` module is responsible for communicating with an Arduino device by utilizing functions from the `ardu_handling` module.

#### Functions:
- **`send_ardu(output_ON)`**  
  Sends commands to the Arduino based on the value of the `output_ON` parameter.  
  **Parameters:**  
  - `output_ON` *(bool)*: A flag that determines the mode of command sending.  
    - If `True`, the `sender` function from the `ardu_handling` module is used.  
    - If `False`, the `sender_txt` function is used.  
  **Description:**  
  - The function first calls `actu.update_states()` from the `ardu_handling` module, then executes the appropriate `sender` or `sender_txt` object based on the value of `output_ON`.

---

## Requirements

- Python 3.6 or later
- The `ardu_handling` module (an external module required for `send_ardu.py` to work)

---

## Usage Instructions

1. **Working with JSON files:**
   - Use the `load_json` function to load data from a JSON file.
   - Use the `save_json` function to save data to a JSON file.

2. **Communicating with Arduino:**
   - Import the `send_ardu` function from the `send_ardu.py` module.
   - Call the function with the appropriate `output_ON` parameter depending on the desired mode.


