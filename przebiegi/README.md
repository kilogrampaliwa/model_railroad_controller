# Przebiegi Project

This repository contains a set of Python scripts designed for managing and verifying train signaling systems, specifically focusing on semaphores, switches, and sections. The project consists of multiple modules that interact with CSV data to ensure the correct configuration and safe operation of tracks and signaling systems.

## Folder Structure

- **`pg_to_objects.py`**: Contains functions and logic for verifying and managing program points (PGs) in the signaling system. It checks if a given run is available, evaluates switch and section availability, and performs necessary adjustments to the state of the system based on the current configuration.
  
- **`wyklucz_zajete.py`**: Defines the `wyklucz` class that verifies whether semaphores or sections can be activated based on the current state of the system (occupied sections and switches). This class utilizes data from CSV files to manage the relationships between semaphores, sections, and switches and ensures that no conflicting configurations occur.

## Key Components

### 1. **Program Point (PG) Management** (`pg_to_objects.py`)
   - **`give_objects(pg, existing_pgs)`**: Checks whether the given program point (PG) can be used based on the availability of switches and sections.
   - **`_check_existing(pg, existing_pgs)`**: Verifies if a PG already exists or if a conflict is present.
   - **`_give_switches(pg, existing_pgs)`**: Checks if the switches required for a specific PG are available.
   - **`_give_sections(pg, existing_pgs)`**: Checks if the necessary sections for a given PG are available.

### 2. **Activation Verification** (`wyklucz_zajete.py`)
   - **`weryfikuj(przyciski, zajete, ostatni_sem)`**: Verifies if the requested semaphores or sections can be activated based on the current status of the signaling system.
   - **`__dict_odcinki`**, **`__dict_zwrotnice`**: These dictionaries store relationships between sections and switches, respectively, for later verification.
   - **`__dict_mozliwe`**: A predefined dictionary of possible semaphore connections, used to evaluate activation feasibility.

## Configuration Files
The system relies on the following CSV files to function:
- **`tablice_prawdy/odcinki_rel.csv`**: Contains the relationships and statuses of sections.
- **`tablice_prawdy/zwrotnice.csv`**: Contains data on switch configurations.

These files are critical for the operation of both `pg_to_objects.py` and `wyklucz_zajete.py`.


## Dependencies

Ensure you have Python 3.x and the necessary dependencies:
- `csv` (for reading CSV files)
- Other standard Python libraries

