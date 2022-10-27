import bpy

bpy.ops.preferences.addon_enable(module='io_import_images_as_planes')
full_path = r"C:\Users\stern\Documents\college\senior_proj\datapipeline4101\code\space.jpg"
bpy.ops.import_image.to_plane(files=[{'name':full_path}], align_track=True, size_mode="CAMERA")