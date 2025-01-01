# Object Changing Module

## Overview

This module provides a comprehensive set of functions for managing and manipulating semaphore and object states in a transportation control system. The primary features include updating states, handling semaphore signals, and processing configurations.

---

## Functions

### 1. **`change_object(what, which, toChange)`**
   General-purpose function to update the state of an object.

   - **Parameters**:
     - `what`: The type of object to change (`sem`, `zwr`, `tmn`, `krz`).
     - `which`: The specific object identifier.
     - `toChange`: The new state or value to apply.

### 2. **`change_sem(which, toChange)`**
   Updates the semaphore state, including signal type and blinking configuration.

   - **Parameters**:
     - `which`: Identifier for the semaphore.
     - `toChange`: List defining new signal and blinking states.

### 3. **`change_zwr(which, toChange)`**
   Updates the state of a switch.

   - **Parameters**:
     - `which`: Identifier for the switch.
     - `toChange`: List defining new type and blinking state.

### 4. **`_change_krz_g(which, part, toChange)`**
   Internal function to update crossing states.

   - **Parameters**:
     - `which`: Identifier for the crossing.
     - `part`: Specifies which part (0 or 1) to update.
     - `toChange`: New state to apply.

### 5. **`change_krz(which, toChange)`**
   Updates crossing states based on site-specific conditions.

   - **Parameters**:
     - `which`: Identifier for the crossing.
     - `toChange`: New state to apply.

### 6. **`podwojne(tablica, ktory_element)`**
   Extracts elements from nested lists.

   - **Parameters**:
     - `tablica`: List of nested lists.
     - `ktory_element`: Index of the element to extract.

### 7. **`change_sems(sem_nastawy)`**
   Updates multiple semaphore states based on predefined configurations.

   - **Parameters**:
     - `sem_nastawy`: A callable that returns semaphore configurations.

### 8. **`sem_numsig(nums_3)`**
   Converts a numeric representation into semaphore signal configurations.

   - **Parameters**:
     - `nums_3`: List of numeric signal states.

### 9. **`zero_sem(segm)`**
   Resets semaphore signals to their default state.

   - **Parameters**:
     - `segm`: List of semaphore segments.

### 10. **`number_to_sem(number_char, strona)`**
   Maps numeric identifiers to semaphore codes based on location.

   - **Parameters**:
     - `number_char`: Numeric identifier as a string.
     - `strona`: Location (e.g., `LL`, `CL`, `CP`, `PP`).

### 11. **`all_sem(lista_p)`**
   Extracts all related semaphore identifiers from a list.

   - **Parameters**:
     - `lista_p`: List of semaphore properties.

### 12. **`sem_to_but(sem)`**
   Maps semaphore identifiers to button codes.

   - **Parameters**:
     - `sem`: Semaphore identifier.

---

## Requirements

- **Dependencies**:
  - `program_utils`: Provides JSON handling utilities for loading and saving configurations.
- **File Structure**:
  - `databases/cechy/obiekty_zmienne.json`: Stores object configurations.
  - `databases/przebiegi/przebiegi.json`: Stores trajectory configurations.

---
