import numpy as np

def resize_model(triangles, voxel_size):
    print(triangles.shape)
    x = triangles[:,:,0]
    y = triangles[:,:,1]
    z = triangles[:,:,2]
    min_x, min_y, min_z = np.min(x), np.min(y), np.min(z)
    max_x, max_y, max_z = np.max(x), np.max(y), np.max(z)

    curr_x = max_x - min_x
    curr_y = max_y - min_y
    curr_z = max_z - min_z

    scale_factor_x = voxel_size[0] / curr_x
    scale_factor_y = voxel_size[1] / curr_y
    scale_factor_z = voxel_size[2] / curr_z

    scale = min(scale_factor_x, scale_factor_y, scale_factor_z)

    for i in range(len(triangles)):
        for j in range(len(triangles[i])):
            for k in range(len(triangles[i][j])):
                triangles[i][j][k] *= scale
    
    return triangles
