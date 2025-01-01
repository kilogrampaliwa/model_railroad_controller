class wyklucz:
    """
    Class responsible for verifying if certain semaphores or sections can be activated
    based on the current status of the signaling system (occupied sections and switches).
    """

    def __init__(self):
        """
        Initializes dictionaries to store data about sections, switches, and possible semaphore connections.
        Reads the data from CSV files that define relationships between sections and switches.
        """
        self.__dict_odcinki = {}  # Dictionary for section relationships
        self.__dict_zwrotnice = {}  # Dictionary for switch relationships
        self.__zbiorczo = {}  # Combined dictionary of sections and switches
        self.__dict_mozliwe = {
            'A':['4','6','8'],
            'B':['4','6','8'],
            'C':['1','3','2','4','6','8'],
            'D':['1','3','2','4','6','8'],
            'G':['1','2'],
            'H':['1','2'],
            'I':['1','2'],
            'J':['1','2','3','4'],
            'K':['1','2','3','4'],
            'L':['1','2','3','4'],
            'R':['1','2'],
            'S':['1','2'],
            'T':['1','2'],
            'U':['1','2'],
            'V':['1','2'],
            'W':['1','2'],
            'Y':['1','3','2','4','6','8'],
            'Z':['1','3','2','4','6','8'],
        }

        # Read sections data from 'odcinki_rel.csv'
        with open("databases/tablice_prawdy/odcinki_rel.csv", 'r') as odcinki:
            temp_dict = {}
            raw_odcinki = odcinki.readlines()
            id = raw_odcinki[0][:-1].split(',')
            for x in raw_odcinki[1:]:
                for i, n in enumerate(x.split(',')):
                    if i != 0:
                        if len(n) > 1:
                            if '\n' in n: n = n[:-1]
                        if id[i] not in temp_dict.keys():
                            temp_dict[id[i]] = []
                        if n != '-':
                            temp_dict[id[i]].append(x.split(',')[0])
            self.__dict_odcinki = temp_dict  # Store section data

        # Read switches data from 'zwrotnice.csv'
        with open("databases/tablice_prawdy/zwrotnice.csv", 'r') as zwrotnice:
            temp_dict = {}
            raw_zwrotnice = zwrotnice.readlines()
            zwr = raw_zwrotnice[0][:-1].split(',')
            for x in raw_zwrotnice[1:]:
                for i, n in enumerate(x.split(',')):
                    if i != 0:
                        if len(n) > 1:
                            if '\n' in n: n = n[:-1]
                        if x.split(',')[0] not in temp_dict.keys():
                            temp_dict[x.split(',')[0]] = []
                        if n != '-':
                            temp_dict[x.split(',')[0]].append(zwr[i])
            self.__dict_zwrotnice = temp_dict  # Store switch data

        # Combine both section and switch data into a single dictionary
        for x in self.__dict_odcinki.keys():
            self.__zbiorczo[x] = self.__dict_odcinki[x] + self.__dict_zwrotnice[x]


    def weryfikuj(self, przyciski, zajete, ostatni_sem):
        """
        Verifies if the given buttons (semaphores or sections) can be activated based on the current status
        of the system (occupied sections and switches).
        
        Arguments:
            - przyciski (list): List of buttons/semaphores to check.
            - zajete (list): List of already occupied sections or switches.
            - ostatni_sem (str): The last semaphore activated.
        
        Returns:
            - zwrotne (list): List of buttons/semaphores that can be activated.
        """
        zwrotne = []  # List to store valid buttons that can be activated

        loopFlagSemafory = False
        loopFlagOdcinki = False

        # Separate the buttons into two categories: semaphores/sections and others
        przyciski_odc_sem = []
        przyciski_reszta = []

        # Categorize the buttons
        for x in przyciski:
            if x in ['p_A', 'p_B', 'p_C', 'p_D', 'p_G', 'p_H', 'p_I', 'p_J', 'p_K', 'p_L', 'p_R', 'p_S', 'p_T', 'p_U', 'p_V', 'p_W', 'p_Y', 'p_Z']:
                loopFlagSemafory = True
                przyciski_odc_sem.append(x)
            elif x in ['p_LL1','p_LL2','p_LL3','p_LL4','p_PP1','p_PP2','p_LC1','p_LC2','p_LC3','p_LC4','p_LC6','p_LC8','p_PC1','p_PC2','p_PC3','p_PC4','p_PC6','p_PC8']:
                loopFlagOdcinki = True
                przyciski_odc_sem.append(x)
            else:
                przyciski_reszta.append(x)

        # Check semaphores and sections if they can be activated
        if loopFlagSemafory:
            for n in przyciski_odc_sem:
                mozliwe = 0
                for m in self.__dict_mozliwe[n[-1]]:
                    potrzeba = self.__zbiorczo[n[-1] + m]  # Required sections for activation
                    mozliwy = True
                    potrzeba_bis = []

                    # If the semaphore is in specific categories, modify the required sections
                    for o in potrzeba:
                        if n in ['p_G', 'p_H', 'p_I', 'p_J', 'p_K', 'p_L', 'p_R', 'p_S', 'p_T', 'p_U', 'p_V', 'p_W'] and ostatni_sem:
                            if 'C' not in o: potrzeba_bis.append(o)
                        else:
                            potrzeba_bis.append(o)

                    # Check if any of the required sections are already occupied
                    for o in potrzeba_bis:
                        if o in zajete:
                            mozliwy = False
                    if mozliwy:
                        mozliwe += 1
                if mozliwe > 0:
                    zwrotne.append(n)  # Add semaphore to list if it can be activated
        
        # If we are checking sections
        elif loopFlagOdcinki:
            for n in przyciski_odc_sem:
                odcinek = ostatni_sem + n[-1]
                potrzeba = self.__zbiorczo[odcinek]  # Required sections for the given segment
                mozliwy = True
                potrzeba_bis = []

                # Modify required sections for certain types of segments
                for o in potrzeba:
                    if n in ["p_LL1","p_LL2","p_LL3","p_LL4","p_PP1","p_PP2"]:
                        if 'C' not in o: potrzeba_bis.append(o)
                    else:
                        potrzeba_bis.append(o)

                # Check if any of the required sections are already occupied
                for o in potrzeba_bis:
                    if o in zajete:
                        mozliwy = False
                if mozliwy:
                    zwrotne.append(n)  # Add section to list if it can be activated

        # Add any remaining buttons that are not semaphores or sections
        for x in przyciski_reszta:
            zwrotne.append(x)

        return zwrotne  # Return the list of valid buttons/semaphores that can be activated
