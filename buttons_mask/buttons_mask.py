import json

def give_buttons(which_stage: str, which_buttons=False):
    """
    Provides a list of buttons appropriate to the specified stage of an operation.

    Parameters:
    - which_stage (str): Specifies the current stage for which buttons are needed.
    - which_buttons (optional): Additional input to refine the button selection for specific stages.

    Returns:
    - list: A list of button identifiers relevant to the current stage.
    """
    
    # Load button definitions from the JSON file
    buttons = []
    with open('databases/lokalizacje/przyciski.json', 'r') as file:
        buttons = json.load(file).keys()

    # Output list to store relevant buttons
    output = []

    # Define helper functions for filtering buttons

    def give_uppers():
        """
        Adds buttons from the upper panel to the output list.
        These buttons are typically prefixed with 'pg_'.
        """
        for x in buttons:
            if 'pg_' in x:
                output.append(x)

    def give_sem(chosen=False):
        """
        Adds buttons that start a run (przebieg).
        
        Parameters:
        - chosen (optional): If provided, adds specific buttons to the output list.
        """
        if chosen:
            return give_given(chosen)
        for x in buttons:
            if 'p_' in x:
                if x not in ['p_Akc', 'p_Usn']:
                    # Only add buttons with specific valid characters at position 2
                    if len(x) == 3 and x[2] in ['A', 'B', 'C', 'D', 'G', 'H', 'I', 'J', 
                                                'K', 'L', 'R', 'S', 'T', 'U', 'V', 'W', 
                                                'Y', 'Z']:
                        output.append(x)
        if chosen == 'end':
            return True

    def give_lin(chosen=False):
        """
        Adds buttons that continue the run (przebieg).

        Parameters:
        - chosen (optional): If provided, adds specific buttons to the output list.
        """
        if chosen:
            return give_given(chosen)
        for x in buttons:
            if 'p_' in x:
                if x[-1] not in ['A', 'B', 'C', 'D', 'G', 'H', 'I', 'J', 'K', 'L', 
                                 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']:
                    if x[2] != 'u':
                        output.append(x)
        if chosen == 'end':
            return True

    def give_usn():
        """
        Adds buttons that destroy the run (przebieg) to the output list.
        These buttons are prefixed with 'p_usn'.
        """
        for x in buttons:
            if 'p_usn' in x:
                output.append(x)

    def give_exc_usn(chosen):
        """
        Adds specific buttons to destroy the run based on the provided list.

        Parameters:
        - chosen: A list of identifiers to customize the buttons added.
        """
        for x in chosen:
            output.append(f'p_usn_{x}')

    def give_given(butlist):
        """
        Adds a given list of buttons to the output list.

        Parameters:
        - butlist: A list of button identifiers to be added.
        """
        for x in butlist:
            output.append(f'p_{x}')

    # Logic to determine buttons based on the current stage
    if which_stage == 'Default(empty)':  # Stage when no actions have started
        give_uppers()
        output.extend(['p_NDr', 'p_Stp'])
        return output
    elif which_stage == 'Default(full)':  # Stage when at least one run exists
        give_uppers()
        output.extend(['p_NDr', 'p_Usn', 'p_Stp'])
        return output
    elif which_stage == 'newLine':  # Stage for starting a new run
        give_sem(which_buttons)
        output.extend(['p_Anl', 'p_Zak', 'p_Stp'])
        return output
    elif which_stage == 'lineSem':  # Stage after choosing the line
        give_sem(which_buttons)
        output.extend(['p_Anl', 'p_Zak', 'p_Stp'])
        return output
    elif which_stage == 'lineTor':  # Stage after choosing the semaphore
        give_lin(which_buttons)
        output.extend(['p_Anl', 'p_Zak', 'p_Stp'])
        return output
    elif which_stage == 'continueLine':  # Stage when continuing a line
        give_lin()
        output.extend(['p_Anl', 'p_Zak', 'p_Stp'])
        return output
    elif which_stage == 'noMore':  # Stage when no more options are available
        output.extend(['p_Anl', 'p_Zak', 'p_Stp'])
        return output
    elif which_stage == 'delete':  # Stage for deleting a run
        give_exc_usn(which_buttons)
        output.extend(['p_Anl', 'p_Stp'])
        return output
