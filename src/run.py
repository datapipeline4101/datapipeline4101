# run with blender -b --python ./src/run.py

import bpy
import numpy as np
import os
import tqdm
import math


def import_package_windows(package, os_type="windows"):
    import importlib
    import os
    import subprocess
    import ensurepip
    import sys
    if os_type == "windows":
       print("WINDOWS")
       python_exe = os.path.join(sys.prefix, 'bin', 'python.exe') 
    else:
        print("MAC OR LINUX")
        python_exe = os.path.join(sys.prefix, 'bin', 'python3.10')
    target = os.path.join(sys.prefix, 'lib', 'site-packages')
    
    subprocess.call([python_exe, '-m', 'ensurepip'])
    subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'])

    #example package to install (SciPy):
    subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', package, '-t', target,])
    #  i = importlib.import_module(package)



def back_ground_adder(filepath):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

    for node in tree.nodes:
        tree.nodes.remove(node)

    image_node = tree.nodes.new('CompositorNodeImage')
    scale_node = tree.nodes.new('CompositorNodeScale')
    alpha_over_node = tree.nodes.new('CompositorNodeAlphaOver')
    render_layer_node = tree.nodes.new('CompositorNodeRLayers')
    output_node = tree.nodes.new('CompositorNodeComposite')

    # Scales image to dimensions set in the Render panel, my case 1280x720
    scale_node.space = "RENDER_SIZE"


    # Scale background image
    links.new(image_node.outputs[0], scale_node.inputs[0])

    # Set background image as background image input to alpha node
    links.new(scale_node.outputs[0], alpha_over_node.inputs[1]) #1

    # Set rendered object as the foreground image to alpha node
    links.new(render_layer_node.outputs[0], alpha_over_node.inputs[2]) #2

   
    # Set rendered object as the foreground image to alpha node
    links.new(render_layer_node.outputs[0], alpha_over_node.inputs[2]) #2

    # Final image is the output image
    links.new(alpha_over_node.outputs[0], output_node.inputs[0])
    bpy.context.scene.render.film_transparent = True
    
    
    # Load background image and set output file
    image_node = bpy.context.scene.node_tree.nodes[0]
    image_node.image = bpy.data.images.load(filepath)
    #file_output_node.file_slots[0].path = 'blender-######.color.png' # blender placeholder #


def create_camera(location, rotation, lens):
    scene = bpy.context.scene
    cam1 = bpy.data.cameras.new("Camera 1")
    cam1.lens = lens

    cam_obj1 = bpy.data.objects.new("Camera 1", cam1)
    cam_obj1.location = location
    cam_obj1.rotation_euler = rotation
    scene.collection.objects.link(cam_obj1)
    bpy.context.scene.camera = bpy.data.objects["Camera 1"]

def create_light(type, energy, location, rotation=[1.5, 0.0, 0.0]):

    
    # Create light datablock
    light_data = bpy.data.lights.new(name="my-light-data", type=type)
    light_data.energy = energy

    # Create new object, pass the light data 
    light_object = bpy.data.objects.new(name="my-light", object_data=light_data)

    if (type=="SUN"):
        light_object.rotation_euler = rotation

    # Link object to collection in context
    bpy.context.collection.objects.link(light_object)

    # Change light position
    light_object.location = location

def delete_all_objects():
    
    bpy.ops.object.select_all()
    bpy.ops.object.delete()
    """
    Deletes all objects in the current scene
    """
    deleteListObjects = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'HAIR', 'POINTCLOUD', 'VOLUME', 'GPENCIL',
                     'ARMATURE', 'LATTICE', 'EMPTY', 'LIGHT', 'LIGHT_PROBE', 'CAMERA', 'SPEAKER']

    # Select all objects in the scene to be deleted:

    for o in bpy.context.scene.objects:
        for i in deleteListObjects:
            if o.type == i: 
                o.select_set(False)
            else:
                o.select_set(True)
    # Deletes all selected objects in the scene:
    bpy.ops.object.delete() 


def get_location(obj, frame):
    bpy.context.scene.frame_set(frame)
    global_location = obj.matrix_world.to_quaternion()

    return(global_location[0], global_location[1], global_location[2], global_location[3])

def create_stars(star_config):
    import random
    from tqdm import tqdm

    # Set the number of stars to create
    num_stars = star_config["num_stars"]

    # Set the size range for the stars
    min_size = star_config["min_size"]
    max_size = star_config["max_size"]

    # Set the location range for the stars
    min_loc = star_config["min_dist"]
    max_loc = star_config["max_dist"]
    random.seed(star_config["star_seed"])
    # Set the brightness range for the stars
    min_bright = star_config["min_bright"]
    max_bright = star_config["max_bright"]

    # Create a new material for the stars
    mat = bpy.data.materials.new(name="StarMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    emission_node = nodes.new(type="ShaderNodeEmission")
    emission_node.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Create the stars
    for i in tqdm(range(int(num_stars))):
        # Create a new sphere mesh for the star
        bpy.ops.mesh.primitive_uv_sphere_add(radius=random.uniform(min_size, max_size), location=(random.uniform(min_loc, max_loc), random.uniform(min_loc, max_loc), random.uniform(min_loc, max_loc)))

        # Add the material to the star
        bpy.context.object.active_material = mat

        # Set the brightness of the star
        brightness = random.uniform(min_bright, max_bright)
        emission_node.inputs[1].default_value = brightness

        # Set the random rotation of the star
        bpy.ops.transform.rotate(value=random.uniform(0, 2 * 3.14), orient_axis='X')
        bpy.ops.transform.rotate(value=random.uniform(0, 2 * 3.14), orient_axis='Y')
        bpy.ops.transform.rotate(value=random.uniform(0, 2 * 3.14), orient_axis='Z')

        # Set the random scale of the star
        bpy.ops.transform.resize(value=(random.uniform(0.5, 1.5), random.uniform(0.5, 1.5), random.uniform(0.5, 1.5)))

        # Set the random location of the star
        bpy.ops.transform.translate(value=(random.uniform(min_loc, max_loc), random.uniform(min_loc, max_loc), random.uniform(min_loc, max_loc)))

def import_obj(filepath, scale=1.0, location_arr=None):
    
    bpy.ops.import_scene.obj(filepath=filepath)

    obj = bpy.context.selected_objects

    for sub_part in obj:
        if location_arr:
            sub_part.location = location_arr
        new_scale = (scale, scale, scale)

        # Set the scale of the object
        sub_part.scale = new_scale
    return obj


def flightpath(flight_path_type, fps, len_of_ani, scene, obj_group, rotations, positions=None, x_eq=None, y_eq=None, z_eq=None,  ):
        if flight_path_type == "POINT":
            number_of_frame = 0
            frame_gap = (len_of_ani*fps) // (len(positions)-1)

            for idx in (range(len(positions))):
                for obj_i in obj_group:

                    # now we will describe frame with number $number_of_frame
                    scene.frame_set(number_of_frame)

                    obj_i.location = positions[idx]
                    obj_i.keyframe_insert(data_path="location", index=-1)

                    # move next camera_frame_gap frames forward - Blender will figure out what to do between this time
                    number_of_frame += frame_gap-1

        number_of_frame = 0
        frame_gap = (len_of_ani*fps) // (len(positions)-1)

        for idx in (range(len(rotations))):
            for obj_i in obj_group:

                # now we will describe frame with number $number_of_frame
                scene.frame_set(number_of_frame)

                obj_i.rotation_euler = rotations[idx]
                obj_i.keyframe_insert(data_path="rotation_euler", index=-1)

                # move next camera_frame_gap frames forward - Blender will figure out what to do between this time
                number_of_frame += frame_gap-1

        if flight_path_type == "FUNCTION":
            positions = []

            def flight_path(t):
                new_position_x = eval(x_eq)
                new_position_y = eval(y_eq)
                new_position_z = eval(z_eq)
                new_position = (new_position_x, new_position_y, new_position_z)
                return new_position

            position_amount = len_of_ani * fps

            for i in range(position_amount):
                # pass i instead of start_position
                start_position = flight_path(i)
                #print("new position", start_position)
                positions.append(start_position)


            frame_gap = (len_of_ani*fps) // (len(positions)-1)


            # start with frame 0
            number_of_frame = 0  
            for idx in range(len(positions)):  
                for obj_i in obj_group:

                    # now we will describe frame with number $number_of_frame
                    scene.frame_set(number_of_frame)

                    # set new location for sphere $kule and new rotation for cube $kostka
                    obj_i.location = positions[idx]
                    #print(positions[idx])
                    obj_i.keyframe_insert(data_path="location", index=-1)

                # move next 10 frames forward - Blender will figure out what to do between this time
                number_of_frame += 1


def get_depth():
    import numpy as np
    import cv2
    """Obtains depth map from Blender render.
    :return: The depth map of the rendered camera view as a numpy array of size (H,W).
    """
    z = bpy.data.images['Viewer Node']
    w, h = z.size
    dmap = np.array(z.pixels[:], dtype=np.float32) # convert to numpy array
    dmap = np.reshape(dmap, (h, w, 4))[:,:,0]
    dmap = np.rot90(dmap, k=2)
    dmap = np.fliplr(dmap)
    return dmap

def main():
    # bpy.ops.wm.read_homefile(use_empty=True)
    delete_all_objects()
    
    base_path = os.getcwd() 
    import_package_windows("toml")
    import toml
    import_package_windows("tqdm")
    import_package_windows("opencv-python")

    from tqdm import tqdm
    toml_path = base_path + r"/src/config.toml"
    print(base_path)

    with open(toml_path, "rb") as f:
        toml_dict = toml.load(toml_path)
        
    # Import the satellite
    sat_path = (base_path + toml_dict["satellite"]["satellite_file"]).encode('unicode_escape')
    sat = import_obj(sat_path, scale =toml_dict["satellite"]["scale"])

    # Import the earth
    if toml_dict["earth"]["use_earth"]:
        earth_path = (base_path + toml_dict["earth"]["earth_file"]).encode('unicode_escape')
        earth = import_obj(earth_path, location_arr=toml_dict["earth"]["earth_location"], scale=toml_dict["earth"]["scale"])
  
    

    create_stars(toml_dict["stars"])

    world = bpy.data.worlds["World"]
    world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)


    light_data = toml_dict["lighting"]
    create_light(type=light_data["light_type"], energy=light_data["energy"], location=tuple(light_data["location"]))

    # read the camera setting and create camera
    camera_settings = toml_dict["camera"]
    create_camera(location=camera_settings["location"], rotation=camera_settings["rotation"], lens=camera_settings["lens"])
    cam = bpy.data.objects['Camera 1']

    # This sets an invisible object that the camera will always point to if view_locked = True
    bpy.ops.object.empty_add(location=tuple(toml_dict["camera"]["lock_point"]))
    if toml_dict["camera"]["view_locked"]:
        constraint = cam.constraints.new(type='TRACK_TO')
        constraint.target = bpy.data.objects['Empty']
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'

    # Add static backgound
    if toml_dict["background"]["static_background"]:
        back_ground_adder((base_path+toml_dict["background"]["background_file"]))

    # set the scene
    scene = bpy.context.scene

    # Change the fps
    fps = toml_dict["animation"]["fps"]
    scene.render.fps = fps
    
    
    positions = toml_dict["flightpath"]["positions"]
    rotations = toml_dict["flightpath"]["rotations"]
    
    
    ani_setting = toml_dict["animation"]

    len_of_ani = ani_setting["animation_lenth"]

    frame_gap = (len_of_ani*fps) // (len(positions)-1)

    flightpath(toml_dict["flightpath"]["flight_path_type"], fps, len_of_ani, scene, sat, toml_dict["flightpath"]["rotations"], 
               positions=toml_dict["flightpath"]["positions"], x_eq=toml_dict["flightpath"]["x_eq"], 
               y_eq=toml_dict["flightpath"]["y_eq"], z_eq=toml_dict["flightpath"]["z_eq"])
    
    flightpath(toml_dict["camera_flightpath"]["flight_path_type"], fps, len_of_ani, scene, [cam], toml_dict["camera_flightpath"]["rotations"], 
               positions=toml_dict["camera_flightpath"]["positions"], x_eq=toml_dict["camera_flightpath"]["x_eq"], 
               y_eq=toml_dict["camera_flightpath"]["y_eq"], z_eq=toml_dict["camera_flightpath"]["z_eq"])


    bpy.context.scene.render.image_settings.file_format=ani_setting["file_format"]
    output_dir = ani_setting["output_dir"]

    import cv2
    for frame in tqdm(range(fps*len_of_ani)):
        bpy.context.scene.frame_set(frame)
        bpy.context.scene.render.filepath = output_dir + str(frame)
        bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)
        cv2.imwrite('depth' +str(frame) + ".png", get_depth() * 255)

        
    bpy.ops.wm.save_as_mainfile(filepath=base_path+r"/animation_test.blend")

    #render_depth_map(scene, cam, output_dir, 0, len_of_ani*fps)
    for frame in range(len_of_ani*fps):
       # print(frame)
        get_location(sat[0], frame)
    #bpy.ops.render.view_show()

    import json
    annotations = []

    for frame in range(len_of_ani*24):
        annotation = {
            'Frame': frame ,
            'Image': output_dir + str(frame),
            'Pose_info': get_location(sat[0], frame), 
        }
        print(annotation)
        annotations.append(annotation)
        print(frame, get_location(sat[0], frame))
        get_location(sat[0], frame)

    with open(output_dir+"coco.json" , "w") as outfile:
        outfile.write(json.dumps(annotations))


    

    #print("FRAMEGAP:", frame_gap)


main()
