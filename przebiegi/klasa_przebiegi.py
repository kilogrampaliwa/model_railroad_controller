import przebiegi.pg_to_objects as pto

class przebieg:
    """
    Represents a train journey (przebieg), managing its state, semaphore-panel pairings (PGs),
    and related elements.

    Class Attributes:
    - existing_pgs: Tracks all existing PGs across instances to prevent overlaps.

    Instance Attributes:
    - __pgs: List of PGs (semaphore-panel identifiers) associated with this journey.
    - __elements: List of objects/elements involved in the journey.
    - __state: Current state of the journey (0: proposed, 1: accepted, 2: occupied).
    - __edit: Boolean flag indicating if the journey is still being edited.
    - __sem_mid: Mapping of semaphore configurations for validation.
    """

    existing_pgs = []

    def __init__(self):
        """
        Initializes a `przebieg` instance with default values:
        - __pgs and __elements are empty lists.
        - __state is set to 0 (proposed).
        - __edit is set to True to allow editing.
        """
        self.__pgs: list[str] = []
        self.__elements: list[str] = []
        self.__state: int = 0
        self.__edit = True

        # Predefined semaphore mappings for validation purposes.
        self.__sem_mid = [
            [['H', 'V'], '1'], [['I', 'U'], '2'], [['G', 'W'], '3'],
            [['J', 'T'], '4'], [['K', 'S'], '6'], [['L', 'R'], '8']
        ]

    def show_state(self):
        """Returns the current state of the journey."""
        return self.__state

    def show_pgs(self):
        """Returns the list of PGs associated with this journey."""
        return self.__pgs

    def show_elements(self):
        """Returns the list of elements associated with this journey."""
        return self.__elements

    def change_state(self, state: int):
        """
        Changes the state of the journey.
        Args:
        - state (int): The new state to assign.
        """
        self.__state = state

    def end_edition(self):
        """Marks the journey as finalized, disabling further edits."""
        self.__edit = False

    def __delete_form_list(self):
        """
        Removes the journey's PGs from the global `existing_pgs` list upon deletion.
        This ensures other journeys can reuse the released PGs.
        """
        for x in self.__pgs:
            self.__class__.existing_pgs.remove(x)

    def __del__(self):
        """Destructor to clean up PGs from the global list."""
        self.__delete_form_list()

    def add_pg(self, sem: str, tor: str):
        """
        Adds a PG (semaphore-panel pairing) to the journey.

        Args:
        - sem (str): The semaphore identifier.
        - tor (str): The panel identifier.
        """
        if self.__edit:
            if not self.__pgs:
                # First PG in the journey.
                self.__add_single(sem, tor)
            else:
                # Subsequent PGs finalize the journey.
                self.__add_single(sem, tor)
                self.__edit = False

    def __add_single(self, sem: str, tor: str):
        """
        Adds a single PG to the journey if valid.

        Args:
        - sem (str): Semaphore identifier.
        - tor (str): Panel identifier.
        """
        # Determine the section and validate its availability.
        sect = pto.give_section(tor, sem)
        cont = False

        if not self.__pgs:
            cont = True
        elif self.__check_mids(sect[1]):
            cont = True
        else:
            print(f'else = {self.__check_mids(sect[1])}')

        if sect[0] and cont:
            # Retrieve objects associated with the PG and add them to the journey.
            obj = pto.give_objects(sect[1], self.__class__.existing_pgs)

            if obj[0]:
                self.__pgs.append(sect[1])
                self.__elements += obj[1] + obj[2]
                self.__class__.existing_pgs += sect[1]

    def __check_mids(self, new_pg):
        """
        Validates if the new PG belongs to a compatible semaphore configuration.

        Args:
        - new_pg (str): The new PG to validate.

        Returns:
        - bool: True if the PG is valid, False otherwise.
        """
        if new_pg[0] == self.__pgs[0][0]:
            return False

        for x in self.__sem_mid:
            if x[1] == self.__pgs[0][1]:
                if new_pg[0] in x[0]:
                    return True
        return False
