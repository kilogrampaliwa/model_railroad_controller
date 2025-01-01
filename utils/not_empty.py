import json

def is_not_empty():
    """
    Checks if the 'przebiegi.json' file contains any data.
    
    This function reads the JSON file located at 'databases/przebiegi/przebiegi.json' 
    and returns True if the file contains any data (i.e., its length is greater than 0). 
    Otherwise, it returns False.
    
    Returns:
        bool: True if the file is not empty, False otherwise.
    """
    with open('databases/przebiegi/przebiegi.json', 'r') as file:
        przebiegi = json.load(file)  # Loads the content of the JSON file
    
    if len(przebiegi) > 0:
        return True  # Returns True if the file has data
    else:
        return False  # Returns False if the file is empty
