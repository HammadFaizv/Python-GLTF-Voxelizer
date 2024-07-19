from gltflib import GLTF
import numpy as np
import os
from Vertex import get_triangles
from preprocess import resize_model
from Voxel import triangle_voxalize
from export import create_voxel_obj_file, export_schematic

# loading the gltf file
glb = GLTF.load('meshes/mutant_skull.glb')
model = glb.model
resource = glb.resources[0]

triangles = [] # contain objects of Triangle
triangles_color = []
triangles, triangles_color = get_triangles(model, resource, triangles)
triangles = np.array(triangles)
triangles_color = np.array(triangles_color)
# print('Triangles : ')
# print(triangles[:5])
# print('Color : ')
# print(triangles_color[:5])

voxel_size = [60,60,60]
triangles = resize_model(triangles, voxel_size)

voxel = []
voxel_color = []

for i in range (len(triangles)): # go though each triangle and voxelize it
    new_voxel, color_voxel = triangle_voxalize(triangles[i], triangles_color[i])
    for j in range(len(new_voxel)):
        if new_voxel[j] not in voxel: #if the point is new add it to the voxel
            voxel.append(new_voxel[j])
            voxel_color.append(color_voxel[j])
    print("done for: ",((i/len(triangles)) * 100))
    # if((i/len(new_triangles)) * 100 >= 5): # testing
    #     break


print(len(voxel)) #number of points in the voxel
print("Voxels : ",voxel[:10])

x_points = []
y_points = []
z_points = []
for a in range (len(voxel)):
    x_points.append(voxel[a][0])
    y_points.append(voxel[a][1])
    z_points.append(voxel[a][2])

max_dimensions = [ max(x_points), max(y_points), max(z_points) ]
min_dimensions = [ min(x_points), min(y_points), min(z_points) ]
print("Dimensions : ", max_dimensions, '&', min_dimensions)

offset = [0, 0, 0]

# setup offset
for i in range(3):
    offset[i] = min(min_dimensions[i],0)

# fancy way to save files
items = os.listdir('output')
files = [item for item in items if os.path.isfile(os.path.join('output', item))]
cnt = len(files)

## save voxel
# file_path = f'output/glb_voxel_model{cnt+1}.obj'
# create_voxel_obj_file(file_path, voxel, voxel_color)
# print(f"Voxel model saved to {file_path}")

## save schematic
file_path = f'schem/glb_schematic{cnt+1}.schematic'
export_schematic(voxel, voxel_color, voxel_size[0], offset, file_path)
print(f"Schematic saved to {file_path}")