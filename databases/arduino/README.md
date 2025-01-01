# arduino folder README

## Overview

This repository contains JSON files for objects and Arduino boards. The project is structured into two main folders: **obiekty** (objects) and **plytki** (boards). Both folders contain JSON files with information about the objects in a model layout (such as signals, switches, etc.) and the raw signals for Arduino pins (represented as binary values).

### Folder Structure

- **obiekty**: Contains information about various objects on the layout (semaphores, signals, switches, etc.). 
- **plytki**: Contains raw signals (0 and 1) for Arduino pin states.

Both folders have files with the same names, but the contents are different. In **obiekty**, the files provide object-level details, while in **plytki**, they represent the pin states.

### File Naming Convention

The JSON filenames follow a specific pattern:

- **A0, A1, D3, D5**: These refer to the pin numbers on the Arduino boards.
- **C1, C2, P1**: These represent board identifiers. The first symbol indicates the side (left, right, center, input), while the second part indicates the serial number.

### File Structure

#### Example file in **obiekty** folder:

```json
{
    "A0": [
        "L",
        "Z"
    ],
    "A1": [
        "L",
        "Pg"
    ],
    "A2": [
        "L",
        "C"
    ],
    "A3": [
        "L",
        "Pd"
    ],
    "A4": [
        "L",
        "B"
    ],
    "A5": [
        "0",
        "0"
    ],
    "A6": [
        "0",
        "0"
    ],
    "A7": [
        "0",
        "0"
    ],
    "D2": [
        "0",
        "0"
    ],
    "D3": [
        "z12",
        "L"
    ],
    "D4": [
        "z12",
        "P"
    ],
    "D5": [
        "H",
        "B"
    ],
    "D6": [
        "H",
        "Pd"
    ],
    "D7": [
        "H",
        "C"
    ],
    "D8": [
        "H",
        "Pg"
    ],
    "D9": [
        "H",
        "Z"
    ],
    "strona": "C",
    "symb_pin": "abcd"
}
```

- Pin assignments (e.g., A0, A1, D3, D5) are mapped to various object symbols. *- The object symbols can represent different states or positions, such as L (left), Z (signal), Pg (green), etc. *- The "strona" field indicates the side of the layout (e.g., "C" for center). *- The "symb_pin" field holds an identifier for the pin configuration (e.g., "abcd"). *

Example file in plytki folder:

{
    "A0": 0,
    "A1": 0,
    "A2": 1,
    "A3": 0,
    "A4": 0,
    "A5": 1,
    "A6": 0,
    "A7": 0,
    "D2": 0,
    "D3": 0,
    "D4": 1,
    "D5": 0,
    "D6": 0,
    "D7": 0,
    "D8": 1,
    "D9": 0,
    "strona": "C",
    "symb_pin": "efgh"
}


- In the plytki files, each pin (e.g., A0, A1, D3, D5) has a binary state (either 0 or 1). *- The "strona" field again represents the side of the layout (e.g., "C" for center). *- The "symb_pin" field represents the pin configuration (e.g., "efgh"). 
### Key Terms and Symbols 
- A0, A1, D3, D5: Arduino pin numbers. *- L, Z, Pg, Pd, H, B, C: Object symbols, representing different components like signals, semaphores, and switches. *- strona: The side of the layout (left, right, center, etc.). *- symb_pin: A symbolic identifier for the pin configuration. ## Usage 
To work with these files: 
1. Object Files (obiekty folder) contain detailed information about the objects on the layout, including their symbolic representations (such as lights, switches). *2. Board Files (plytki folder) contain raw signals representing the current states of the Arduino pins (0 or 1), which can be used for controlling the layout. 
This structure allows for flexible control of the layout while maintaining a clear separation between object definitions and the underlying pin states. 
