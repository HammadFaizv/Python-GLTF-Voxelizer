import numpy as np

from vanilla import get_block_color_data
from block_id import get_block_id

color_data = get_block_color_data()

block_colors = []

for block in color_data:
    block_colors.append([block['colour']['r'], block['colour']['g'], block['colour']['b']])

# # delete blocks that aren't in block_id.py
# for block in color_data:
#     try:
#         block_data = get_block_id(block['name'])
#     except KeyError:
#         print(block['name'])

def nearest_block_by_color(color, block_colors = block_colors):

    color = np.array(color) / 255
    block_colors = np.array(block_colors)
    distance = np.sqrt(np.sum((block_colors - color) ** 2, axis = 1))
    name = color_data[np.argmin(distance)]['name']

    return get_block_id(name)