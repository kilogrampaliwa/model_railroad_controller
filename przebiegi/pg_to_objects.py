def give_objects(pg, existing_pgs):
    """
    Checks if the run already exists or if a cross of existing ones is possible.
    
    Args:
    - pg: The current point (run).
    - existing_pgs: List of existing runs.
    
    Returns:
    - A list: [Boolean indicating availability, list of switches, list of sections].
    """
    if _check_existing(pg, existing_pgs):  # Check if the run exists or is possible
        # Check if switches are available
        _gsw = _give_switches(pg, existing_pgs)
        if _gsw[0]:  # If switches are available, check if sections are available
            _gse = _give_sections(pg, existing_pgs)
            if _gse[0]:  # If sections are available, return switches and sections
                return [True, _gsw[1], _gse[1]]
            else:
                return [False, False, 0]  # Sections not available
        else:
            return [False, False, 1]  # Switches not available
    else:
        return [False, False, 2]  # Run doesn't exist


def _check_existing(pg, existing):
    """
    Checks if the run is already existing or is blocked.
    
    Args:
    - pg: The point to check.
    - existing: List of existing runs.
    
    Returns:
    - Boolean indicating whether the run can proceed or is blocked.
    """
    excluded = []
    table = _give_table('databases/tablice_prawdy/calosc.csv')
    
    if table:
        for x in existing:
            position_nos = []
            for i, value in enumerate(table[0]):
                if x == value:
                    position_nos.append([x, i])
            for n in table:
                for m in position_nos:
                    if n[m[1]] in [1, '1']:
                        if m[0] not in excluded:
                            excluded.append(m[0])
    else:
        return False

    return pg not in excluded


def _give_switches(pg, existing):
    """
    Retrieves the switches reserved for a specific run.
    
    Args:
    - pg: The point (run).
    - existing: List of existing runs.
    
    Returns:
    - A list: [Boolean indicating switch availability, list of switch names].
    """
    pg_reserved = []
    ex_reserved = []
    output = []
    
    table = _give_table('databases/tablice_prawdy/zwrotnice.csv')
    
    if table:
        for n in table:
            if n[0] == pg:
                for i in range(1, len(n)):
                    if n[i] in [0, '0', 1, '1']: pg_reserved.append(i)
            elif n[0] in existing:
                for i in range(1, len(n)):
                    if n[i] in [0, '0', 1, '1']:
                        if i not in ex_reserved: ex_reserved.append(i)
    else:
        return [False, False]
    
    for x in pg_reserved:
        if x in ex_reserved:
            return [False, False]  # Conflict detected
    
    for x in pg_reserved:
        output.append(table[0][x])  # Add available switches
    
    return [True, output]


def _give_sections(pg, existing):
    """
    Retrieves the sections reserved for a specific run.
    
    Args:
    - pg: The point (run).
    - existing: List of existing runs.
    
    Returns:
    - A list: [Boolean indicating section availability, list of section names].
    """
    pg_reserved = []
    ex_reserved = []
    
    table = _give_table('databases/tablice_prawdy/odcinki_rel.csv')
    
    if table:
        to_check_pg = []
        to_check_ex = []
        for i, value in enumerate(table[0]):
            if value == pg:
                to_check_pg = i
            elif value in existing:
                to_check_ex.append(i)

        if to_check_pg:
            for x in table:
                if x[to_check_pg] in [1, '1']:
                    pg_reserved.append(x[0])
                for n in to_check_ex:
                    if x[n] in [1, '1']:
                        if x[0] not in ex_reserved:
                            ex_reserved.append(x[0])
        else:
            return [False, 0]  # No matching section found
    else:
        return [False, 1]  # No table found
    
    for x in pg_reserved:
        if x in ex_reserved:
            return [False, 2]  # Conflict between reserved sections
    
    return [True, pg_reserved]


def give_section(sec, sem):
    """
    Checks if a section is available.
    
    Args:
    - sec: The section to check.
    - sem: The semaphore to check.
    
    Returns:
    - A list: [Boolean indicating availability, section details].
    """
    table = _give_table('databases/tablice_prawdy/odcinki_rel.csv')
    
    if table:
        possible_nos = []
        possible = []
        for x in table:
            if '_' in sec:
                sec = sec.split('_')[1]
            if sec[1] == 'C':
                sec = 'CC' + sec[2:]
            if x[0] == sec:
                for i in range(1, len(x)):
                    if x[i] in [1, '1', '1\n']:
                        possible_nos.append(i)
        
        for x in possible_nos:
            possible.append(table[0][x])
        
        if not possible:
            return [False, "No possible connections."]
        
        for x in possible:
            if x[0] == sem:
                return [True, x]
        
        return [False, "Semaphore not possible in this section."]
    else:
        return [False, "Table not found."]


def _give_table(address):
    """
    Reads the truth table from a CSV file.
    
    Args:
    - address: The path to the CSV file.
    
    Returns:
    - A list representing the table data or False if an error occurred.
    """
    try:
        table = []
        with open(address) as file:
            table_raw = file.readlines()

        # Remove newline characters and split by commas
        table = [line.strip().split(',') for line in table_raw]
        return table
    except:
        return False


def give_possible(sem_or_tor):
    """
    Gives possible connections for a semaphore or track.
    
    Args:
    - sem_or_tor: The semaphore or track to check.
    
    Returns:
    - A list of possible connections.
    """
    connections = {
        'A': ['LC4', 'LC6', 'LC8'],
        'B': ['LC4', 'LC6', 'LC8'],
        'C': ['LC1', 'LC2', 'LC3', 'LC4', 'LC6', 'LC8'],
        'D': ['LC1', 'LC2', 'LC3', 'LC4', 'LC6', 'LC8'],
        'G': ['LL1', 'LL2'],
        'H': ['LL1', 'LL2'],
        'I': ['LL1', 'LL2'],
        'J': ['LL1', 'LL2', 'LL3', 'LL4'],
        'K': ['LL1', 'LL2', 'LL3', 'LL4'],
        'L': ['LL1', 'LL2', 'LL3', 'LL4'],
        'W': ['PP1', 'PP2'],
        'V': ['PP1', 'PP2'],
        'U': ['PP1', 'PP2'],
        'R': ['PP1', 'PP2'],
        'S': ['PP1', 'PP2'],
        'T': ['PP1', 'PP2'],
        'Y': ['PC1', 'PC2', 'PC3', 'PC4', 'PC6', 'PC8'],
        'Z': ['PC1', 'PC2', 'PC3', 'PC4', 'PC6', 'PC8']
    }

    if sem_or_tor in connections:
        return connections[sem_or_tor]
    
    # Handle specific track cases
    if sem_or_tor[1] == 'C':
        if sem_or_tor[0] == 'P':
            sem_or_tor = 'L' + sem_or_tor[1:]
        elif sem_or_tor[0] == 'L':
            sem_or_tor = 'P' + sem_or_tor[1:]
    
    return [x for x in connections if sem_or_tor in connections[x]]


def switch_to_pg(pg):
    """
    Converts a switch to a program point.
    
    Args:
    - pg: The program point to convert.
    
    Returns:
    - A list of switch names and statuses.
    """
    table = _give_table('databases/tablice_prawdy/zwrotnice.csv')
    
    if table:
        zwrot = []
        for x_c in pg:
            for x in table[1:]:
                if x[0] == x_c:
                    zwrot_usn = []
                    for i, y in enumerate(x[1:]):
                        if y in ['0', '1']:
                            zwrot.append([table[0][i+1], int(y)])
                        zwrot_usn.append(y)
        return zwrot
    return False
