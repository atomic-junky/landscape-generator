import os
import random
import io

import noise
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

font = ImageFont.truetype(font=f"{ROOT_DIR}/assets/Rockstar-ExtraBold.otf", size=35)
shape = (512,512)

def generate(seed=random.randint(0, 100000), scale=300, octaves=8, persistence=0.5, lacunarity=2.0):

    seed = seed
    scale = scale
    octaves = int(octaves)
    persistence = float(persistence)
    lacunarity = float(lacunarity)

    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = noise.snoise2(i/scale, 
                                        j/scale, 
                                        octaves=octaves, 
                                        persistence=persistence, 
                                        lacunarity=lacunarity,
                                        repeatx=512, 
                                        repeaty=512, 
                                        base=seed)

    ocean = [0,66,137]
    water = [0, 87, 180]
    plain = [172, 166, 90]
    valley = [105, 140, 37]
    mountain = [244, 252, 252]
    beach = [238, 214, 175]

    def add_color(world):
        color_world = np.zeros(shape+(3,), dtype=np.uint8)
        for i in range(shape[0]):
            for j in range(shape[1]):
                if world[i, j] < -0.02:
                    color_world[i][j] = ocean
                elif world[i, j] < 0.05:
                    color_world[i][j] = water
                elif world[i, j] < 0.1:
                    color_world[i][j] = beach
                elif world[i, j] < 0.15:
                    color_world[i][j] = plain
                elif world[i, j] < 0.35:
                    color_world[i][j] = valley
                elif world[i, j] < 1.0:
                    color_world[i][j] = mountain

        return color_world

    color_world = add_color(world)

    result = Image.fromarray(color_world)

    draw = ImageDraw.Draw(result)
    draw.text((10, shape[0]-35), f"#{seed}", font=font, stroke_fill=(0, 0, 0), stroke_width=1)
    stream = io.BytesIO()
    
    result.save(stream, format='PNG')
    
    return stream