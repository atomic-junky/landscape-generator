import random
import PySimpleGUI as sg
from PIL import Image

import perlin

sg.theme('DarkBrown1')

seed = random.randint(0, 100000)
image = perlin.generate(seed=seed)

file_list_column = [
    [sg.Text("Image Settings", font=("Helvetica", 20))],
    [sg.VPush()],
    [sg.Text("Seed: #"), sg.InputText(seed, key="-SEED-", size=(15, 10)), sg.Button("Randomize", key="-RANDOMIZE-SEED-")],
    [sg.Text("Scale: "), sg.Push(), sg.Slider(range=(1, 2000), orientation='h', size=(34, 20), default_value=300, key='-SCALE-')],
    [sg.Text("Octaves: "), sg.Push(), sg.Slider(range=(1.0, 10.0), orientation='h', size=(34, 20), default_value=8, resolution=1, key='-OCTAVES-')],
    [sg.Text("Persistence: "), sg.Push(), sg.Slider(range=(0.0, 1.0), orientation='h', size=(34, 20), default_value=0.5, resolution=.1, key='-PERSISTENCE-')],
    [sg.Text("Lacunarity: "), sg.Push(), sg.Slider(range=(0.0, 10.0), orientation='h', size=(34, 20), default_value=2.0, resolution=.5, key='-LACUNARITY-')],
    [sg.Button("Generate")],
]

image_viewer_column = [
    [sg.Text("Result", font=("Helvetica", 20))],
    [sg.Image(key="-IMAGE-", size=(512, 512), data=image.getvalue())],
    [sg.FileSaveAs("Save", key='-FILE-SAVE-', enable_events=True, font=("Helvetica", 10), file_types=(('PNG', '.png'), ('JPG', '.jpg')))]
]

layout = [
    [sg.Text('Landscape Generator', font=("Helvetica", 25), size=(50, 1), justification="center")],
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Lanscape generator", layout)

while True:

    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:

        break

    if event == "Generate":
        seed = values['-SEED-']
        scale = values['-SCALE-']
        octaves = values['-OCTAVES-']
        persistence = values['-PERSISTENCE-']
        lacunarity = values['-LACUNARITY-']
        
        try: 
            seed = int(seed)
        except:
            window['-SEED-'].update("")
            continue
            
        image = perlin.generate(seed=seed, scale=scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
        window['-IMAGE-'].update(data=image.getvalue())
        
    elif event == "-RANDOMIZE-SEED-":
        window['-SEED-'].update(str(random.randint(0, 100000)))
        
    elif event == "-FILE-SAVE-":
        file_save_path = values['-FILE-SAVE-']
        image_to_save = Image.open(image)
        image_to_save.save(file_save_path)
    
window.close()