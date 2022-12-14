import bpy
import numpy as np
import os
#import tomllib

def import_package_windows(package):
    # import subprocess
    # import sys
    # import os
    
    # # path to python.exe
    # python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
    
    # # upgrade pip
    # subprocess.call([python_exe, "-m", "ensurepip"])
    # subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
    
    # # install required packages
    # subprocess.call([python_exe, "-m", "pip", "install", package])

    import importlib

    #i = importlib.import_module(package)

    import subprocess
    import ensurepip
    import sys
    # ensurepip.bootstrap()
    # pybin = sys.executable
    # subprocess.check_call([pybin, '-m', 'pip', 'install', package])
    #import importlib

    # 

    
    python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
    target = os.path.join(sys.prefix, 'lib', 'site-packages')
    
    subprocess.call([python_exe, '-m', 'ensurepip'])
    subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'])

    #example package to install (SciPy):
    subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', package, '-t', target])
    i = importlib.import_module(package)
    print(i)
    print('DONE')


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

    # Select output folder, i.e. where to store rendered images
    #file_output_node.base_path = "C:/tmp/"

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

def create_light(type, energy, location):
    # Create light datablock
    light_data = bpy.data.lights.new(name="my-light-data", type=type)
    light_data.energy = energy

    # Create new object, pass the light data 
    light_object = bpy.data.objects.new(name="my-light", object_data=light_data)

    # Link object to collection in context
    bpy.context.collection.objects.link(light_object)

    # Change light position
    light_object.location = location

def delete_all_objects():
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

def get_location(obj, frame):
    bpy.context.scene.frame_set(frame)
    global_location = obj.matrix_world.to_quaternion()

    print(global_location[0], global_location[1], global_location[2], global_location[3])

def main():
    bpy.ops.wm.read_homefile(use_empty=True)
    delete_all_objects()
    
    base_path = os.getcwd() 
    import_package_windows("toml")
    import toml
    toml_path = base_path + r"\tomconfig.toml"


    with open(toml_path, "rb") as f:
        toml_dict = toml.load(toml_path)
    

    sat_path = (base_path + toml_dict["satellite"]["satellite_file"]).encode('unicode_escape')
    bpy.ops.import_scene.obj(filepath=sat_path)

    sat = bpy.context.selected_objects

    print(sat)
    
    light_data = toml_dict["lighting"]
    create_light(type=light_data["light_type"], energy=light_data["energy"], location=tuple(light_data["location"]))

    camera_settings = toml_dict["camera"]
    create_camera(location=camera_settings["location"], rotation=camera_settings["rotation"], lens=camera_settings["lens"])
    back_ground_adder((base_path+toml_dict["background"]["background_file"]))
    scene = bpy.context.scene
    
    positions = toml_dict["flightpath"]["positions"]
    rotations = toml_dict["flightpath"]["rotations"]

    
    ani_setting = toml_dict["animation"]

    len_of_ani = ani_setting["animation_lenth"]

    frame_gap = (len_of_ani*24) // (len(positions)-1)

    print("FRAMEGAP:", frame_gap)

    # start with frame 0
    number_of_frame = 0  
    for idx in range(len(positions)):
        
        for satt in sat:

            # now we will describe frame with number $number_of_frame
            scene.frame_set(number_of_frame)

            # set new location for sphere $kule and new rotation for cube $kostka
            satt.location = positions[idx]
            satt.keyframe_insert(data_path="location", index=-1)

            satt.rotation_euler = rotations[idx]
            satt.keyframe_insert(data_path="rotation_euler", index=-1)

        # move next 10 frames forward - Blender will figure out what to do between this time
        number_of_frame += frame_gap-1
    #print("FFFF")

    bpy.context.scene.render.image_settings.file_format=ani_setting["file_format"]
    output_dir = ani_setting["output_dir"]

    for frame in range(len_of_ani*24):
        bpy.context.scene.frame_set(frame)
        bpy.context.scene.render.filepath = output_dir + str(frame)
        bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)


    #bpy.ops.render.render('INVOKE_DEFAULT', animation=True, use_viewport = True, write_still=True)
    #print("FFFF")
    for frame in range(len_of_ani*24):
        print(frame)
        get_location(sat[0], frame)
    #bpy.ops.render.view_show()

    print("POS", len(positions))
    print("FRAMEGAP:", frame_gap)
main()
