 # Button Manager for Stages
 
 ## Overview
 
 This script, `give_buttons.py`, provides functionality to determine and manage the appropriate buttons for various operational stages of a process. It dynamically loads button configurations from a JSON file and filters them based on predefined criteria for each stage.
 
 ## Key Functionality
 
 - **Dynamic Button Loading**: Buttons are loaded from a JSON file (`przyciski.json`) located in the `databases/lokalizacje` directory.
 - **Stage-Specific Button Selection**: Filters buttons based on the specified stage (`which_stage`) and optional parameters (`which_buttons`).
 - **Helper Functions**: Includes a series of internal functions to manage and filter button lists, such as:
   - Buttons for upper panels.
   - Buttons for starting, continuing, and destroying processes.
   - Customizable button lists for specific use cases.
 
 ## File Structure
 
 - **JSON File**: The `przyciski.json` file should contain button definitions as key-value pairs.
 - **Script Location**: This script is located in its dedicated folder, separate from other modules.
 
 ## Function Breakdown
 
 ### `give_buttons(which_stage, which_buttons=False)`
 Main function that provides a list of buttons for a specified stage.
 
 - **Parameters**:
   - `which_stage` (str): Specifies the current stage for which buttons are needed.
   - `which_buttons` (optional): Additional input to refine the button selection for specific stages.
 
 - **Returns**:
   - A list of button identifiers relevant to the current stage.
 
 ### Helper Functions
 
 #### `give_uppers()`
 Adds buttons from the upper panel (prefixed with `pg_`) to the output list.
 
 #### `give_sem(chosen=False)`
 Adds buttons to start a run (`przebieg`).
 - **Parameters**:
   - `chosen`: If provided, specifies specific buttons to add.
 
 #### `give_lin(chosen=False)`
 Adds buttons to continue a run.
 - **Parameters**:
   - `chosen`: If provided, specifies specific buttons to add.
 
 #### `give_usn()`
 Adds buttons to destroy a run (prefixed with `p_usn`).
 
 #### `give_exc_usn(chosen)`
 Adds specific buttons for destroying a run based on the provided list.
 - **Parameters**:
   - `chosen`: A list of identifiers to customize the buttons added.
 
 #### `give_given(butlist)`
 Adds a given list of buttons to the output list.
 - **Parameters**:
   - `butlist`: A list of button identifiers to be added.
 
 ## Stage Logic
 
 The script provides buttons based on the following stages:
 
 - **`Default(empty)`**: No actions have started. Includes upper panel buttons and defaults like `p_NDr` and `p_Stp`.
 - **`Default(full)`**: At least one process exists. Includes buttons for creating, stopping, and deleting processes.
 - **`newLine`**: Starting a new process. Includes semaphores and basic control buttons.
 - **`lineSem`**: After selecting a line. Includes semaphores and control buttons.
 - **`lineTor`**: After selecting a semaphore. Includes line options and control buttons.
 - **`continueLine`**: Continuing an existing process. Includes line continuation and control buttons.
 - **`noMore`**: No further options. Includes control buttons only.
 - **`delete`**: Deleting a process. Includes specific delete buttons and control buttons.
 
 ## Example JSON File
 
 ```json
 {
     "pg_1": "Upper Panel Button 1",
     "pg_2": "Upper Panel Button 2",
     "p_A": "Start Button A",
     "p_B": "Start Button B",
     "p_usn_1": "Destroy Button 1"
 }
 ```
 
 ## Requirements
 
 - Python 3.x
 - JSON file located in `databases/lokalizacje/przyciski.json`
 
