import bpy
import numpy as np
import os
from sklearn import linear_model


def back_ground_adder(filepath):
  img = bpy.data.images.load(filepath)
  bpy.data.images.load(filepath, check_existing=False)
  
#bpy.ops.wm.addon_enable(module='Import-Export: Import Images as Planes')
back_ground_adder(r"C:\Users\stern\Documents\college\senior_proj\datapipeline4101\code\space.jpg")
full_path = r"C:/Users/stern\Documents\college\senior_proj\datapipeline4101\models\nasa-aqua-satellite-obj\nasa-aqua-satellite.obj"
bpy.ops.import_scene.obj(filepath=full_path)

sat = bpy.context.selected_objects
print(", ".join(o.name for o in sat))

scene = bpy.context.scene
cam1 = bpy.data.cameras.new("Camera 1")
cam1.lens = 20

# Create light datablock
light_data = bpy.data.lights.new(name="my-light-data", type='POINT')
light_data.energy = 10000

# Create new object, pass the light data 
light_object = bpy.data.objects.new(name="my-light", object_data=light_data)

# Link object to collection in context
bpy.context.collection.objects.link(light_object)

# Change light position
light_object.location = (0, 0, 3)


# create the first camera object
cam_obj1 = bpy.data.objects.new("Camera 1", cam1)
cam_obj1.location = (9.69, -10.85, 12.388)
cam_obj1.rotation_euler = (0.6799, 0, 0.8254)
scene.collection.objects.link(cam_obj1)
bpy.context.scene.camera = bpy.data.objects["Camera 1"]

zoo = np.array([1,2,3,4,5])

positions = (0,0,1),(0,1,1),(0,2,1),(1,4,1),(1,6,1)

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
    number_of_frame += 10
print("FFFF")

bpy.context.scene.render.image_settings.file_format='JPEG'
bpy.context.scene.render.filepath = "C:/tmp/"

bpy.ops.render.render('INVOKE_DEFAULT', animation=True, use_viewport = True, write_still=True)
print("FFFF")

#bpy.ops.render.view_show()
