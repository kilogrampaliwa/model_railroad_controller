import przebiegi
import utils
import program_utils
import object_changing
import threading
import json

def check_seq_button(symbol, button_to_seq, list_of_sem, potential_seq):
    """
    Processes the sequence of buttons pressed and determines the section.
    
    Args:
    - symbol (str): Button symbol pressed.
    - button_to_seq (list): Current sequence of button presses.
    - list_of_sem (list): List of semaphore buttons.
    - potential_seq (list): List to store potential sequences.
    
    Returns:
    - Updated button_to_seq, list_of_sem, and potential_seq.
    """
    section = False
    button_to_seq.append(symbol)

    if len(button_to_seq) == 2:
        if button_to_seq[0] in list_of_sem:
            section = przebiegi.give_section(button_to_seq[1], button_to_seq[0])
            section = button_to_seq[0]
        else:
            section = przebiegi.give_section(button_to_seq[0], button_to_seq[1])
            section = button_to_seq[1]
        button_to_seq = []
        if potential_seq[0][0]:
            potential_seq[0][1] = section
        else:
            potential_seq[0][0] = section

    return button_to_seq, list_of_sem, potential_seq

def accept_seq(potential_seq):
    """
    Finalizes the sequence if valid and saves it.

    Args:
    - potential_seq (list): Current potential sequence.

    Returns:
    - Reset potential_seq after processing.
    """
    out = False

    if potential_seq[0][1]:
        out = potential_seq
    else:
        out = [[potential_seq[0][0]], potential_seq[1]]

    potential_seq = [[False, False], []]
    table = []

    if out and out[0][0]:
        table = program_utils.load_json('databases/przebiegi/przebiegi.json') if utils.is_not_empty else []
        table.append(out)
        program_utils.save_json('databases/przebiegi/przebiegi.json', table)

        zwrotnice = []
        for x in object_changing.podwojne(table, 0):
            zwr_temp = przebiegi.switch_to_pg(x)
            for y in zwr_temp:
                zwrotnice.append(y)

        for x in zwrotnice:
            try:
                object_changing.change_zwr(x[0], [x[1], False])
            except:
                try:
                    object_changing.change_krz(x[0], [x[1], False])
                except:
                    print(f"Non-existent switch: {x}")

        color_seqs(potential_seq)

    # Run background tasks in a separate thread
    threading.Thread(target=background_tasks, daemon=True).start()
    return potential_seq

def background_tasks(sem_nastawy):
    """
    Executes background tasks for signal changes and countdown.

    Args:
    - sem_nastawy: Semaphore settings.
    """
    utils.count_three_half()
    object_changing.change_sems(sem_nastawy)

def reject_seq(potential_seq):
    """
    Resets the potential sequence on rejection.

    Args:
    - potential_seq (list): Current potential sequence.

    Returns:
    - Reset potential_seq.
    """
    potential_seq = [[False, False], []]
    color_seqs(potential_seq)
    return potential_seq

def color_seqs(potential_seq, list_of_seg):
    """
    Updates the colors of the segments based on their status.

    Args:
    - potential_seq (list): Current potential sequence.
    - list_of_seg (list): List of segments.

    Returns:
    - Updated potential_seq, list_of_seg, and an empty list (placeholder).
    """
    reserved = []
    potential = []
    descr_dict = program_utils.load_json('databases/cechy/obiekty_zmienne.json')

    def color_segm(seq, color_no=0):
        """Assigns a color to a segment."""
        descr_dict[seq]['type'] = descr_dict[seq]['possible_types'][color_no]

    def give_segm(sq_tab):
        """Extracts segments from the given table."""
        seg = []
        for x in sq_tab:
            segm = przebiegi.give_objects(x, [])[2]
            if segm:
                seg.extend(segm)
        return seg

    if potential_seq[0][1]:
        potential = potential_seq
    else:
        potential = [[potential_seq[0]], potential_seq[1]]

    with open('databases/przebiegi/przebiegi.json', 'r') as file:
        table_rw = json.load(file)
        table_rw = object_changing.podwojne(table_rw, 0)

        try:
            if table_rw[0]:
                for x in table_rw:
                    reserved.extend(x)
        except:
            print('No sequences found.')

    reserved_seg = give_segm(reserved)
    potential_seg = give_segm(potential)

    for x in list_of_seg:
        if x in reserved_seg:
            color_segm(x, 2)
        elif x in potential_seg:
            color_segm(x, 1)
        else:
            color_segm(x)

    program_utils.save_json('databases/cechy/obiekty_zmienne.json', descr_dict)
    return potential_seq, list_of_seg, []
