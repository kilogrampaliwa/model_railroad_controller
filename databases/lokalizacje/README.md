# JSON Database README

This project uses a JSON-based database to store and organize various configuration data for objects, buttons, and windows. The data is categorized into different types of JSON files based on the nature of the objects or UI elements involved.

## Folder Structure

The folder structure is as follows:

```
lokalizacje
│
├── obiekty_dynamiczne.json
├── obiekty_statystyczne.json
├── okna.json
└── przyciski.json
```

### Files Overview

1. **obiekty_dynamiczne.json**  
   Contains data for **dynamic objects**. These objects represent items that may change position or state over time. Each entry in this file includes an object identifier and an array with its coordinates (x, y).

   Example entry:

   ```json
   "LC12": [203, 292]
   ```

2. **obiekty_statystyczne.json**  
   Stores data for **static objects**. These objects typically have fixed positions or states. This file also contains key-value pairs, where the key represents the object, and the value is an array of coordinates.

   Example entry:

   ```json
   "tlo": [0, 0]
   ```

3. **okna.json**  
   Defines window positions in the system. Each window has an identifier (e.g., `okna0`, `okna1`, etc.) and a coordinate pair for its position (x, y). The windows are typically fixed or anchored in the UI.

   Example entry:

   ```json
   "okna0": "0,0"
   ```

4. **przyciski.json**  
   Contains data for **buttons**. Each button has a unique identifier (e.g., `p_A`, `p_B`, etc.) and is defined by its position (x, y) on the UI screen.

   Example entry:

   ```json
   "p_A": [40, 210]
   ```

## Example JSON Structure

### Example of `obiekty_dynamiczne.json`

```json
{
    "LC12": [203, 292],
    "LC13": [271, 320],
    "LC21": [79, 292],
    "LC46": [393, 190]
}
```

### Example of `okna.json`

```json
{
    "okna0": "0,0",
    "okna1": "0,0",
    "okna2": "0,0",
    "okna3": "0,0"
}
```

### Example of `obiekty_statystyczne.json`

```json
{
    "tlo": [0, 0],
    "panelGorny": [0, 0],
    "background": [0, 0]
}
```

### Example of `przyciski.json`

```json
{
    "p_A": [40, 210],
    "p_B": [40, 243],
    "p_C": [40, 277],
    "p_D": [40, 311]
}
```
