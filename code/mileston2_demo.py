import bpy
import numpy as np
import os



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

    print(global_location)

def main():
    bpy.ops.wm.read_homefile(use_empty=True)
    delete_all_objects()
    
    base_path = r"C:\Users\stern\Documents\college\senior_proj\datapipeline4101"
    sat_path = base_path + r"\models\nasa-aqua-satellite-obj\nasa-aqua-satellite.obj"
    bpy.ops.import_scene.obj(filepath=sat_path)

    sat = bpy.context.selected_objects
    
    create_light(type="POINT", energy=1000, location=(10,-10,10))

    create_camera(location=(9.69, -5.85, 12.388), rotation=(0.6799, 0, 0.8254), lens=20)
    back_ground_adder(base_path+r"/code/space.jpg")
    scene = bpy.context.scene
    
    positions = (0,0,1),(0,1,1),(0,2,1),(1,4,1),(1,6,1)

    print("POS", len(positions))
    len_of_ani = 1

    frame_gap = (len_of_ani*24) // len(positions)

   

    # start with frame 0
    number_of_frame = 0  
    for pozice in positions:
        
        for satt in sat:

            # now we will describe frame with number $number_of_frame
            scene.frame_set(number_of_frame)

            # set new location for sphere $kule and new rotation for cube $kostka
            satt.location = pozice
            satt.keyframe_insert(data_path="location", index=-1)

            satt.rotation_euler = pozice
            satt.keyframe_insert(data_path="rotation_euler", index=-1)

        # move next 10 frames forward - Blender will figure out what to do between this time
        number_of_frame += frame_gap
    #print("FFFF")

    bpy.context.scene.render.image_settings.file_format='JPEG'
    bpy.context.scene.render.filepath = "C:/tmp/"

    for frame in range(len_of_ani*24):
        bpy.context.scene.frame_set(frame)
        bpy.ops.render.render(write_still=True)


    #bpy.ops.render.render('INVOKE_DEFAULT', animation=True, use_viewport = True, write_still=True)
    #print("FFFF")
    for frame in range(10*len(positions)):
        get_location(sat[0], frame)
    #bpy.ops.render.view_show()
main()
