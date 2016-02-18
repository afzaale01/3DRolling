import bpy
import mathutils
import bmesh
import os

def makeMaterial(name, diffuse):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_intensity = 1
    return mat

if __name__ == "__main__":
    file_id = -1
    # import bunny
    bpy.ops.import_mesh.stl(filepath="/Users/apple/ws/3DRolling/blenderPython/StanfordBunnyTight.stl")
    resize_scale = 25
    bpy.ops.transform.resize(value=(resize_scale, resize_scale, resize_scale))

    # Create two materials
    keep = makeMaterial('keep', (0.8,0.07, 0.67))
    remove = makeMaterial('remove', (0.06, 0.035, 0.8))

    while True:
        try:
            file_id += 1
            bpy.ops.import_scene.obj(filepath="/Users/apple/ws/3DRolling/blenderPython/objGen/gen/test_"+ str(file_id)+".obj")
        except RuntimeError:
            print("last file imported" + str(file_id - 1))
            break
        imported_spiral_name = "test_" + str(file_id)
        imported_obj_name = "StanfordBunnyTight"
        spiral = bpy.data.objects[imported_spiral_name]
        bunny = bpy.data.objects[imported_obj_name]
        mat_offset = len(spiral.data.materials)
        spiral.data.materials.append(keep)
        spiral.data.materials.append(remove)
        keep_idx = mat_offset
        remove_idx = mat_offset + 1

        scene = bpy.context.scene
        scene.objects.active = spiral
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(spiral.data)

        # select and mark spiral on two ends
        bm.faces.ensure_lookup_table()
        bm.faces[0].material_index = remove_idx
        bm.faces[1].material_index = remove_idx
        for f in spiral.data.polygons:
            if (f.normal == mathutils.Vector((-1.0, 0.0, 0.0)) or
            f.normal == mathutils.Vector((1.0, 0.0, 0.0))):
                bm.faces[f.index].select = True
                bm.faces[f.index].material_index = remove_idx
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        spiral.active_material_index = remove_idx
        bpy.ops.object.material_slot_select()
        bpy.ops.mesh.hide(unselected = False)

        # select and mark the inner side of the wall
        bm.faces[spiral.data.polygons[3].index].select = True
        bpy.ops.mesh.select_linked()
        bpy.ops.object.material_slot_assign()
        bpy.ops.mesh.hide(unselected = False)

        bpy.ops.mesh.select_all(action='SELECT')

        #===================================================
        #====Finished construction of the spiral============
        #===================================================
        # Spiral - Bunny
        spiral.select = True
        bpy.context.scene.objects.active = spiral
        bpy.ops.object.modifier_add(type='BOOLEAN')
        mod = spiral.modifiers
        mod[0].name = "SminusB"
        mod[0].object = bunny
        mod[0].operation = 'DIFFERENCE'

        # Apply modifier
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod[0].name)
        bpy.ops.object.mode_set(mode='EDIT')
        spiral.select = False
        bpy.ops.uv.export_layout(filepath="/Users/apple/ws/3DRolling/blenderPython/blender_uv_out/blender_uv_output_"+str(file_id)+".svg", mode='SVG', size=(32768,32768))