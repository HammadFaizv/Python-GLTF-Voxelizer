import numpy as np
from io import BytesIO
import imageio

def get_triangles(model, resource, triangles):
    triangle_colors = []
    for mesh in model.meshes:
        for primitive in mesh.primitives:
            # vertices value
            v_accesors = model.accessors[primitive.attributes.POSITION]
            v_buffer_view = model.bufferViews[v_accesors.bufferView]
            # v_buffer = model.buffers[v_buffer_view.buffer]
            # print(v_buffer)
            start = v_buffer_view.byteOffset or 0
            size = v_buffer_view.byteLength
            vertex_data = np.frombuffer(resource.data[start: start+size], dtype="float32").reshape([-1,3])
            
            i_accesor = model.accessors[primitive.indices]
            i_bufferView = model.bufferViews[i_accesor.bufferView]

            start = i_bufferView.byteOffset or 0
            size = i_bufferView.byteLength
            index_data = np.frombuffer(resource.data[start: start+size], dtype="uint32").reshape([-1,3])

            # get vertex color
            material = model.materials[primitive.material]
            pbr = material.pbrMetallicRoughness

            # either texture exists or color does...get one
            if(pbr.baseColorTexture != None):
                texture_index = pbr.baseColorTexture.index
                texture = model.textures[texture_index]
                image_index = texture.source
                image = model.images[image_index]
                idx = model.bufferViews[image.bufferView]
                img = resource.data[idx.byteOffset : idx.byteOffset+idx.byteLength]
                # convert image bytes to actual image
                bytes_stream = BytesIO(img)
                image_data = imageio.v3.imread(bytes_stream) # gives warning when using v2
                height, width, _ = image_data.shape

                # get vertex uv
                uv_accesors = model.accessors[primitive.attributes.TEXCOORD_0]
                uv_buffer_view = model.bufferViews[uv_accesors.bufferView]
                # uv_buffer = model.buffers[uv_buffer_view.buffer]
                start = uv_buffer_view.byteOffset
                size = uv_buffer_view.byteLength
                uv_data = np.frombuffer(resource.data[start: start+size], dtype="float32").reshape([-1,2])

                # get color from image and create vertex
                for v_idx in index_data: # [[], [], []] -> []
                    coords = []
                    color_coords = []
                    for i in v_idx: # [] -> a,b,c
                        uv_coords = uv_data[i]
                        pt = vertex_data[i]
                        px = int(uv_coords[0] * width)
                        py = int(uv_coords[1] * height)
                        color = image_data[py][px]
                        coords.append([pt[0], pt[1], pt[2]])
                        color_coords.append(color)
                    triangles.append(coords)
                    triangle_colors.append(color_coords)
            else:
                bsf = [int(pbr.baseColorFactor[0]*255), int(pbr.baseColorFactor[1]*255), int(pbr.baseColorFactor[2]*255)]

                for v_idx in index_data:
                    coords = []
                    for i in v_idx:
                        pt = vertex_data[i]
                        coords.append([pt[0], pt[1], pt[2]])
                    triangles.append(coords)
                    triangle_colors.append([bsf]*3)

    return triangles, triangle_colors