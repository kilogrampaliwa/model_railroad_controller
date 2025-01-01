# Cechy Folder


The cechy folder contains several JSON files responsible for defining various graphical and logical aspects of the model layout. These files include representations of objects, tracks, windows, and buttons used in the layout's graphical interface and functionality. The following JSON files are present in this folder:

- obiekty_zmienne.json
- obiekty_zmienne_odcinki.json
- okna.json
- przyciski.json

## obiekty_zmienne.json

This file is responsible for the graphical representation of objects on the model layout. Each object in the layout is represented by a symbol in this file. The file defines the current state of the object, the possible states, and additional settings such as visibility and blinking options.

### Example:

```json
"Tm41": {
    "type": "obrazy/nst/sem/LM0.png",
    "possible_types": [
        "obrazy/nst/sem/PL.png",
        "obrazy/nst/sem/LM0.png",
        "obrazy/nst/sem/LM1.png"
    ],
    "blinking": false,
    "visibility": true
}
```

- key: The name of the object. 
- type: The address to the graphical representation of the current state of the object. 
- possible_types: A list of all possible graphical representations for the object, corresponding to different states. 
- blinking: A boolean indicating whether the object can blink. 
- visibility: A boolean indicating whether the object is currently visible. 
 
## obiekty_zmienne_odcinki.json 
 
This file defines the logical order for track sections, similarly to how obiekty_zmienne.json works for individual objects. It specifies the possible states and the visual representation of track segments used in determining the layout's routing. 
 
### Example: 
```
"PC2": {
    "type": "obrazy/nst/odc/grey_light/PC2.png",
    "possible_types": [
        "obrazy/nst/odc/grey_light/PC2.png",
        "obrazy/nst/odc/green/PC2.png",
        "obrazy/nst/odc/amber_dark/PC2.png",
        "obrazy/nst/odc/red/PC2.png",
        "obrazy/nst/odc/grey_dark/PC2.png",
        "obrazy/nst/odc/blue/PC2.png",
        "obrazy/nst/odc/amber_light/PC2.png"
    ],
    "blinking": false,
    "visibility": true
}
```
 
- The structure and functionality are similar to obiekty_zmienne.json, but this file specifically handles logical elements used for track routing and status visualization. 
 
## okna.json 
 
This file contains basic information about whether the window is visible and whether it contains buttons. It controls the visibility and interaction with the layout's windows. 
 
## przyciski.json 
 
This file describes the buttons within the layout. Each button has an address (graphic), visibility status, and an associated action. 
 
### Example: 
"p_LL1": {
    "address": "obrazy/nst/prz/blue.png",
    "visibility": true,
    "action": "przycisk tor p_LL1"
}

 
- address: The address to the graphical representation of the button. 
- visibility: A boolean indicating whether the button is visible. 
- action: The action that occurs when the button is pressed (identified by name). 
 
