import bpy

# === CONFIGURABLE VARIABLES ===
total_height = 0.7874  # Total height in meters
cubes_tall = 5  # Number of cubes stacked vertically
total_mass = 33.75  # Combined mass of all cubes (kg)
sphere_mass = 10.0  # Mass of the falling icosphere (heavier than cubes)

# === CALCULATED DIMENSIONS ===
cube_size = total_height / cubes_tall
cubes_across = cubes_tall  # Square layout

# === 3D CURSOR POSITION ===
cursor_location = bpy.context.scene.cursor.location.copy()

# Calculate total width of the stack
total_width = cubes_across * cube_size
offset_x = total_width / 2
offset_y = total_width / 2

# Total number of cubes
total_cubes = cubes_across * cubes_across * cubes_tall
mass_per_cube = total_mass / total_cubes

# Build cubes, centered on cursor, bottom aligned at cursor Z
for x in range(cubes_across):
    for y in range(cubes_across):
        for z in range(cubes_tall):
            bpy.ops.mesh.primitive_cube_add(
                size=cube_size,
                location=(
                    cursor_location.x + (x * cube_size) - offset_x + (cube_size / 2),
                    cursor_location.y + (y * cube_size) - offset_y + (cube_size / 2),
                    cursor_location.z + (cube_size / 2) + (z * cube_size)
                )
            )
            cube = bpy.context.active_object

            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            # Set origin to geometry center
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

            # Add bevel modifier
            bevel = cube.modifiers.new(name="Bevel", type='BEVEL')
            bevel.width = 0.005
            bevel.segments = 2
            bevel.limit_method = 'NONE'

            # Add rigid body physics
            bpy.ops.rigidbody.object_add()
            cube.rigid_body.mass = mass_per_cube
            cube.rigid_body.collision_shape = 'BOX'
            cube.rigid_body.collision_margin = 0.0

# === ADD FALLING ICOSPHERE ===

# Calculate top of the stack Z height
stack_top_z = cursor_location.z + total_height

# Add icosphere above the stack
bpy.ops.mesh.primitive_ico_sphere_add(
    subdivisions=2,
    radius=cube_size * 1.5,  # Bigger than before
    location=(cursor_location.x, cursor_location.y, stack_top_z + (cube_size * 4))  # Placed higher above
)
sphere = bpy.context.active_object

# Apply scale
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Set origin
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

# Add rigid body
bpy.ops.rigidbody.object_add()
sphere.rigid_body.mass = sphere_mass
sphere.rigid_body.collision_shape = 'CONVEX_HULL'
sphere.rigid_body.collision_margin = 0.0
