def create_voxel_obj_file(file_path, voxel_positions, voxel_colors, voxel_size=1.0):
    vertices = []
    current_vertex_index = 1  # Index of the current vertex
    cube_vertices = [
        (0, 0, 0), (voxel_size, 0, 0), (voxel_size, voxel_size, 0), (0, voxel_size, 0),
        (0, 0, voxel_size), (voxel_size, 0, voxel_size), (voxel_size, voxel_size, voxel_size), (0, voxel_size, voxel_size)
    ]
    cube_faces = [
        [1, 2, 3, 4],  # Front face
        [8, 7, 6, 5],  # Back face
        [4, 3, 7, 8],  # Top face
        [5, 6, 2, 1],  # Bottom face
        [1, 4, 8, 5],  # Left face
        [2, 6, 7, 3]   # Right face
    ]

    with open(file_path, 'w') as obj_file:
        for voxel_pos, voxel_color in zip(voxel_positions, voxel_colors):
            for dx, dy, dz in cube_vertices:
                vertex = (voxel_pos[0] + dx, voxel_pos[1] + dy, voxel_pos[2] + dz)
                vertices.append(vertex)
                obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]} {voxel_color[0]/255.0} {voxel_color[1]/255.0} {voxel_color[2]/255.0}\n")

            for face in cube_faces:
                offset_face = [idx + current_vertex_index - 1 for idx in face]
                obj_file.write(f"f {offset_face[0]} {offset_face[1]} {offset_face[2]} {offset_face[3]}\n")
            current_vertex_index += 8
