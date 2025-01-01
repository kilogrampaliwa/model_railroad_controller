import program_utils

__all__ = ["change_object","change_sem","change_zwr","change_krz","podwojne","change_sems","sem_numsig","zero_sem","number_to_sem","all_sem","sem_to_but"]

def change_object( what, which, toChange):
    if what == 'sem':
        change_sem(which, toChange)
    elif what == 'zwr':
        change_zwr(which, [toChange, False])
    elif what == 'tmn':
        _change_tmn(which, [toChange, False])
    elif what == 'krz':
        if which[-2:] == 'ab':  _change_krz_g(which[:-2], 0, [toChange, False])
        else:                   _change_krz_g(which[:-2], 1, [toChange, False])

def change_sem( which, toChange):
    table = program_utils.load_json('databases/cechy/obiekty_zmienne.json')
    table = program_utils.load_json('databases/cechy/obiekty_zmienne.json')
    table[which]['type'][0] = table[which]['possible_types'][0][toChange[0][0]]
    table[which]['type'][1] = table[which]['possible_types'][1][toChange[1][0]]
    table[which]['type'][2] = table[which]['possible_types'][2][toChange[2][0]]
    table[which]['blinking'][0] = toChange[0][1]
    table[which]['blinking'][1] = toChange[1][1]
    table[which]['blinking'][2] = toChange[2][1]
    if 'blinking_one' not in table[which]:  table[which]['blinking_one'] = ['','','']
    if table[which]['blinking'][0]:
        if    table[which]['type'][0]==table[which]['possible_types'][0][0]: table[which]['blinking_one'][0] = table[which]['type'][0]
        else: table[which]['blinking_one'][0] = table[which]['type'][0]
    if table[which]['blinking'][1]:
        if    table[which]['type'][1]==table[which]['possible_types'][1][0]: table[which]['blinking_one'][1] = table[which]['type'][1]
        else: table[which]['blinking_one'][1] = table[which]['type'][1]
    if table[which]['blinking'][2]:
        if    table[which]['type'][2]==table[which]['possible_types'][2][0]: table[which]['blinking_one'][2] = table[which]['type'][0]
        else: table[which]['blinking_one'][2] = table[which]['type'][2]
    program_utils.save_json('databases/cechy/obiekty_zmienne.json', table)

def change_zwr( which, toChange):
    table = program_utils.load_json('databases/cechy/obiekty_zmienne.json')
    table[which]['type'] = table[which]['possible_types'][toChange[0]]
    table[which]['blinking'] = toChange[1]
    program_utils.save_json('databases/cechy/obiekty_zmienne.json', table)

def _change_krz_g( which, part, toChange):
    table = program_utils.load_json('databases/cechy/obiekty_zmienne.json')
    if part == 0:
        actual = table[which]['type']
        actual = actual[:-6] + str(toChange[0]) + actual[-5:]
        table[which]['type'] = actual
    else:
        actual = table[which]['type']
        actual = actual[:-5] + str(toChange[0]) + actual[-4:]
        table[which]['type'] = actual
    table[which]['blinking'] = toChange[1]
    program_utils.save_json('databases/cechy/obiekty_zmienne.json', table)

def _change_tmn( which, toChange):
    table = program_utils.load_json('databases/cechy/obiekty_zmienne.json')
    table[which]['type'] = table[which]['possible_types'][toChange[0]]
    table[which]['blinking'] = toChange[1]
    program_utils.save_json('databases/cechy/obiekty_zmienne.json', table)

def change_krz( which, toChange):
    site = which[-2:]
    ####if which[1:3] in ['18', '19']: toChange[0] = abs(toChange[0] - 1)
    if which[1:3] in ['18', '19']:
        if   site=="ab": site = "cd"
        elif site=="cd": site = "ab"
    if   site=="ab":
        table = program_utils.load_json('databases/cechy/obiekty_zmienne.json')
        temp_choice = []
        if table[which[:-2]]['type'][-5] == '0':    temp_choice = [table[which[:-2]]['possible_types'][0], table[which[:-2]]['possible_types'][3]]#table[which[:-2]]['type'] = table[which[:-2]]['possible_types'][toChange[0]]
        else:                                       temp_choice = [table[which[:-2]]['possible_types'][1], table[which[:-2]]['possible_types'][2]]
        table[which[:-2]]['type'] = temp_choice[toChange[0]]
        table[which[:-2]]['blinking'] = toChange[1]
        program_utils.save_json('databases/cechy/obiekty_zmienne.json', table)
    elif site=="cd":
        table = program_utils.load_json('databases/cechy/obiekty_zmienne.json')
        temp_choice = []
        if table[which[:-2]]['type'][-6] == '0':    temp_choice = [table[which[:-2]]['possible_types'][0], table[which[:-2]]['possible_types'][1]]#table[which[:-2]]['type'] = table[which[:-2]]['possible_types'][toChange[0]]
        else:                                       temp_choice = [table[which[:-2]]['possible_types'][3], table[which[:-2]]['possible_types'][2]]
        table[which[:-2]]['type'] = temp_choice[toChange[0]]
        table[which[:-2]]['blinking'] = toChange[1]
        program_utils.save_json('databases/cechy/obiekty_zmienne.json', table)

def podwojne(tablica, ktory_element):
    
    outlist = []
    for x in tablica:
        try:
            outlist.append(x[ktory_element])
        except:
            print("Zly ktory_element")
            return False
    return outlist

def change_sems(sem_nastawy):
    # Load the JSON data from a file
    with open('databases/przebiegi/przebiegi.json', 'r') as file:
        przebiegi = program_utils.load_json(file)#json.load(file)
        przebiegi = podwojne(przebiegi, 0)
    # Define the initial structure of the dictionary
    result = {}
    # Iterate through each sublist in the data
    for przbieg in przebiegi:
        for odcinek in przbieg:
            # Extract the first letter of the item
            first_letter = odcinek[0]
            wprost      = False
            zwrotnica   = False
            krzyz       = False
            # Na wprost
            # D1 H1 V1 Z1
            # C2 I2 U2 Y2
            # A4 J4
            if odcinek in ["D1", "H1", "V1", "Z1", "C2", "I2", "U2", "Y2", "A4", "J4"]: wprost = True
            # Na krzyz
            # A4 A6 A8 B4 B6 B8 C4 C6 C8 D2 D4 D6 D8 J3 J2 J1 K4 K3 K2 K1 L4 L3 L2 L1 I1
            # R2 R1 S2 S1 T2 T1 U1
            elif odcinek in ["A4","A6","A8","B4","B6","B8","C4","C6","C8","D2","D4","D6","D8","J3","J2","J1","K4","K3","K2","K1","L4","L3","L2","L1","I1","R2","R1","S2","S1","T2","T1","U1"]: krzyz = True
            # Na zwrotnica
            else: zwrotnica = True
            # Determine the value based on the first letter and the length of the sublist
            key_nastawa = first_letter
            if krzyz:       key_nastawa+="2"
            elif zwrotnica: key_nastawa+="1"
            elif wprost:    key_nastawa+="0"
            else:           key_nastawa+="2"
            value_dict = sem_nastawy()[key_nastawa]
            value = [[value_dict['B']['sygnal'],value_dict['B']['mruganie']], [value_dict['D']['sygnal'],value_dict['D']['mruganie']], [value_dict['G']['sygnal'],value_dict['G']['mruganie']],]
            value[0][0] = int(value[0][0])
            value[1][0] = int(value[1][0])
            value[2][0] = int(value[2][0])
            value[0][1] = bool(int(value[0][1]))
            value[1][1] = bool(int(value[1][1]))
            value[2][1] = bool(int(value[2][1]))
            # Add the value to the dictionary under the corresponding first letter
            if first_letter not in result:
                result[first_letter] = value
    keys_result = result.keys()
    keys_result = sorted(keys_result)
    if len(keys_result)>1:
        if keys_result[0] in ["A","B","C","D","Y","Z"]:
            if   result[keys_result[1]][1][0] == 1:
                result[keys_result[0]][2][0] = 1
                result[keys_result[0]][2][1] = False
            elif result[keys_result[1]][1][0] == 2:
                result[keys_result[0]][2][0] = 1
                result[keys_result[0]][2][1] = True
            elif result[keys_result[1]][1][0] == 0:
                result[keys_result[0]][2][0] = 2
                result[keys_result[0]][2][1] = False
            else:
                result[keys_result[0]][2][0] = 1
                result[keys_result[0]][2][1] = False
    else:
        if keys_result[0] in ["A","B","C","D","Y","Z"]:
                result[keys_result[0]][2][0] = 1
                result[keys_result[0]][2][1] = False
    for x in result.keys():
        program_utils.change_sem(x, result[x])


def sem_numsig(nums_3):
        if   nums_3[0]==1:
            nums_3[0] = [1, False]
        else:
            nums_3[0] = [0, False]
        if   nums_3[2]==4:
            nums_3[2] = [2, False]
        elif nums_3[2]==3:
            nums_3[2] = [2, True ]
        elif nums_3[2]==2:
            nums_3[2] = [1, True ]
        elif nums_3[2]==1:
            nums_3[2] = [1, False]
        elif nums_3[2]==0:
            nums_3[2] = [0, False]
        if   nums_3[1]==4:
            nums_3[1] = [0, False]
        elif nums_3[1]==3:
            nums_3[1] = [2, False]
        elif nums_3[1]==2:
            nums_3[1] = [2, False]
        elif nums_3[1]==1:
            nums_3[1] = [2, False]
        elif nums_3[1]==0:
            nums_3[1] = [1, False]
        return nums_3




def zero_sem(segm):

    for x in segm:
        change_sem(x[0], [[0, False], [1, False], [0, False]])


def number_to_sem(number_char, strona):

    slownik_LL = {
                'A':'4',
                'B':'3',
                'C':'2',
                'D':'1'}
    slownik_CL = {
                'G':'3',
                'H':'1',
                'I':'2',
                'J':'4',
                'K':'6',
                'L':'8'}
    slownik_CP = {
                'R':'8',
                'S':'6',
                'T':'4',
                'U':'2',
                'V':'1',
                'W':'3'}
    slownik_PP = {
                'Y':'2',
                'Z':'1'}
    if strona=='LL':
        for x in slownik_LL.keys():
            if slownik_LL[x]==number_char: return x
    if strona=='CL':
        for x in slownik_CL.keys():
            if slownik_CL[x]==number_char: return x
    if strona=='CP':
        for x in slownik_CP.keys():
            if slownik_CP[x]==number_char: return x
    if strona=='PP':
        for x in slownik_PP.keys():
            if slownik_PP[x]==number_char: return x

def all_sem(lista_p):

    out =[]
    for x in lista_p:
        out.append(x[0])
        if x[0] in ['A','B','C','D']:
            out.append(number_to_sem(x[1], 'CP'))
        elif x[0] in ['G','H','I','J','K','L']:
            out.append(number_to_sem(x[1], 'LL'))
        elif x[0] in ['R','S','T','U','V','W']:
            out.append(number_to_sem(x[1], 'PP'))
        elif x[0] in ['Y','Z']:
            out.append(number_to_sem(x[1], 'CL'))
    return out

def sem_to_but(sem):

    slownik = {
            'D': "LL1",
            'C': "LL2",
            'B': "LL3",
            'A': "LL4",
            'Z': "PP1",
            'Y': "PP2",
            'H': "LC1",
            'I': "LC2",
            'G': "LC3",
            'J': "LC4",
            'K': "LC6",
            'L': "LC8",
            'W': "PC1",
            'V': "PC2",
            'U': "PC3",
            'T': "PC4",
            'S': "PC6",
            'R': "PC8",
    }
    return slownik[sem]
