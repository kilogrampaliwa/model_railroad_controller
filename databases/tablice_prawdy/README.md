# README for "tablice_prawdy"

This repository contains three truth tables related to the analysis of segments and switches in various configurations. These truth tables are provided as CSV files and show the relationships between different elements, such as segment blocks and switches. The elements specified within these tables represent components that may block or interact with each other.

## Folder Structure
```
tablice_prawdy/
│
├── calosc.csv            # Full relationship truth table
├── odcinki_rel.csv       # Segment relations truth table
└── zwrotnice.csv         # Switches truth table
```

### Files:

#### 1. `calosc.csv`
This file represents a comprehensive truth table that shows the interaction between various segments, which are labeled as A8, A6, A4, B8, B6, B4, C8, C6, and C4. The table uses `1` to indicate that two segments can interact or are compatible, and `-` indicates incompatibility. The columns represent the possible interactions for each segment.

**Format:**
| id   | A8 | A6 | A4 | B8 | B6 | B4 | C8 | C6 | C4 |
|------|----|----|----|----|----|----|----|----|----|
| A8   | -  | 1  | 1  | 1  | 1  | 1  | 1  | 1  | 0  |
| A6   | 1  | -  | 1  | 1  | 1  | 1  | 1  | 1  | 0  |
| A4   | 1  | 1  | -  | 1  | 1  | 1  | 1  | 1  | 0  |
| B8   | 1  | 1  | 1  | -  | 1  | 1  | 1  | 1  | 0  |
| ...  | ...| ...| ...| ...| ...| ...| ...| ...| ...|

**Explanation:**
- Rows represent the segment in focus (e.g., A8, A6, etc.).
- Columns represent other segments that are being tested for compatibility.
- A `1` indicates that the pair of segments is compatible.
- A `-` indicates that the segments are incompatible.

#### 2. `odcinki_rel.csv`
This file displays relationships between segments and their respective switches. The table includes a variety of rows for different segments (such as CC1, CC2, etc.), and the columns correspond to specific switches and their states.

**Format:**
| id   | A8 | A6 | A4 | B8 | B6 | B4 | C8 | C6 | C4 | C |
|------|----|----|----|----|----|----|----|----|----|---|
| CC1  | -  | -  | -  | -  | -  | -  | -  | -  | -  | 1 |
| CC2  | -  | -  | -  | -  | -  | -  | -  | -  | 1  | - |
| ...  | ...| ...| ...| ...| ...| ...| ...| ...| ...| ...|

**Explanation:**
- Each row represents a segment (e.g., CC1, CC2, CC3).
- The columns represent the corresponding states of switches like A8, A6, B8, etc.
- A `1` indicates that the switch is active, while a `-` indicates that it is inactive.

#### 3. `zwrotnice.csv`
This file contains information about switches (labeled z1, z2, etc.) in relation to segments. It includes specific switches like `z1`, `z2`, `z3`, etc., and their status relative to each segment (like A8, A6, etc.). These columns show whether the switches are engaged or not.

**Format:**
| id   | z1 | z2 | z3 | z4ab | z4cd | z5 | z7 | z9ab | z9cd |
|------|----|----|----|------|------|----|----|------|------|
| A8   | -  | -  | -  | -    | -    | -  | -  | 0    | 1    |
| A6   | -  | -  | -  | -    | -    | -  | -  | 0    | 1    |
| A4   | -  | -  | -  | -    | -    | -  | -  | 0    | 0    |
| B8   | -  | -  | -  | -    | -    | 1  | 1  | 1    | 0    |
| ...  | ...| ...| ...| ...  | ...  | ...| ...| ...  | ...  |

**Explanation:**
- The `id` column represents different segments (like A8, A6, etc.).
- Columns like `z1`, `z2`, `z3`, etc. represent the state of various switches associated with each segment.
- The `1` or `0` indicates whether the switch is active or not, respectively.

---

## Purpose of these Truth Tables
These truth tables are used to model the interactions and compatibility of various elements in a system. They ensure that segments and switches operate as expected without interfering with each other. These tables should not be altered, as they represent fixed relationships and logic.

### Important Notes:
- The segments and switches listed (e.g., A8, A6, B8, z1, z2) represent specific components within the system and their interactions.
- The `1` and `-` values indicate whether components can interact, block, or are incompatible with each other.
- The tables are intended to be used as references for validating system configurations.

---

## How to Use

1. **Examine the `calosc.csv`** to understand which segments are compatible or blocked with each other.
2. **Check the `odcinki_rel.csv`** for relationships between segments and switches. This will help identify the active switches and their corresponding segments.
3. **Review the `zwrotnice.csv`** for detailed information about the switches and how they are assigned to different segments.

These files are provided as-is and should not be modified. They serve as a reliable foundation for understanding the system's components and their interactions.

---

## License
This repository does not include any licensing information. Please ensure that you have permission to use and distribute the data if needed.
