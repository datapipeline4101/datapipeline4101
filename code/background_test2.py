import bpy


bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

for node in tree.nodes:
    tree.nodes.remove(node)

image_node = tree.nodes.new('CompositorNodeImage')
scale_node = tree.nodes.new('CompositorNodeScale')
alpha_over_node = tree.nodes.new('CompositorNodeAlphaOver')
render_layer_node = tree.nodes.new('CompositorNodeRLayers')
file_output_node = tree.nodes.new('CompositorNodeOutputFile')

# Scales image to dimensions set in the Render panel, my case 1280x720
scale_node.space = "RELATIVE"

# Select output folder, i.e. where to store rendered images
file_output_node.base_path = "C:/tmp/"

# Scale background image
links.new(image_node.outputs[0], scale_node.inputs[0])

# Set background image as background image input to alpha node
links.new(scale_node.outputs[0], alpha_over_node.inputs[1]) #1

# Set rendered object as the foreground image to alpha node
links.new(render_layer_node.outputs[0], alpha_over_node.inputs[2]) #2

# Final image is the output image
links.new(alpha_over_node.outputs[0], file_output_node.inputs[0])
bpy.context.scene.render.film_transparent = True

# Load background image and set output file
image_node = bpy.context.scene.node_tree.nodes[0]
image_node.image = bpy.data.images.load(r"C:\Users\stern\Documents\college\senior_proj\datapipeline4101\code\space.jpg")
file_output_node = bpy.context.scene.node_tree.nodes[4]
file_output_node.file_slots[0].path = 'blender-######.color.png' # blender placeholder #

cam_obj = bpy.data.objects['Camera']

#bpy.data.objects['Lamp'].data.energy = 50
#bpy.ops.object.lamp_add(type='SUN')
#xavier:
bpy.types.SpotLight.energy = 50
bpy.ops.render.render(write_still=True)