from ursina import *
from math import sin, cos, radians
from random import *
from ursina import lerp
from panda3d.core import Fog
from tree import Tree

app = Ursina()

# === CONFIG ===
target_eye_height = 1.8
target_scale_y = 1.8
normal_speed = 8
crouch_speed = 3
camera.fov = 90  # Try values between 60 - 120
sprint_speed = 20
sensitivity = 100  # Mouse sensitivity; adjust if unintended drift occurs
jump_height = 6
gravity = 20
max_pitch = 89
pitch = -30  # Initial camera pitch to view ground on first frame
yaw = 0
eye_height = 1.8
player_points = 0
velocity_y = 0
is_grounded = False
game_over = False
fall_check_enabled = False  # Delay fall detection
# ==============

window.title = "Haunted City - FPS"
mouse.locked = True
window.color = color.black
window.fps_counter.enabled = True
window.exit_button.visible = False


is_first_person = True
pitch, yaw = 0, 0
max_pitch = 89

coord_text = Text(
    text='Coordinates: 0, 0, 0',
    position=(-0.85, 0.45),  # top-left corner
    origin=(0, 0),
    scale=0.9,
    color=color.white
)


crouch_height = 0.9
stand_height = 1.8
is_crouching = False

held_left = None
held_right = None
pickup_distance = 4.0  # max distance to grab object

bobbing_time = 0.1
base_eye_height = 1.8

# Add fog effect
fog = Fog("SceneFog")  
fog.setMode(Fog.MExponential) 
fog.setColor(0.3, 0.3, 0.3) 
fog.setExpDensity(0.05)
scene.setFog(fog)

crosshair = Entity(parent=camera.ui, model='circle', scale=(0.0125, 0.0125), color=color.white, position=(0, 0))

# === HAND ENTITIES (3D) ===
hand_right = Entity(
    parent=camera,
    model='cube',
    color=color.rgb(255, 224, 189),
    scale=(0.075, 0.2, 0.075),
    position=(0.35, -0.20, 0.4),  # adjusted position
    rotation=(10, 20, -10),
    enabled=True
)

hand_left = Entity(
    parent=camera,
    model='cube',
    color=color.rgb(255, 224, 189),
    scale=(0.075, 0.2, 0.075),
    position=(-0.35, -0.20, 0.4),  # adjusted position
    rotation=(10, -20, 10),
    enabled=True
)

Sky()

# === TERRAIN ===
ground = Entity(
    model='plane',
    scale=(9980, 1, 9981),
    texture_scale=(1690, 2160),
    collider='box',
    position=(0, 0, 0),
    texture="/assets/textures/grass.png"
)

DirectionalLight(y=3, z=3, shadows=True)

# === PLAYER ===
player = Entity(model='cube', scale_y=1.8, origin_y=-0.5, collider='box', position=(0, 10, 0))
player.collider = BoxCollider(player, center=Vec3(0,1,0), size=Vec3(1,2,1))
player.visible = False

points_text = Text(
    text=f'Points: {player_points}',
    position=(0.75, 0.45),
    origin=(0, 0),
    scale=1.5,
    color=color.red
)

# === POINT PICKUPS ===
point_pickups = []

class PointPickup(Entity):
    def __init__(self, position=(0, 1, 0), value=10):
        super().__init__(
            model='cube',
            color=color.green,
            scale=0.5,
            position=position,
            collider='box'
        )
        self.value = value
        point_pickups.append(self)

def spawn_points(num_points=5, area_size=40):
    for _ in range(num_points):
        x = uniform(-area_size, area_size)
        z = uniform(-area_size, area_size)
        y = 0.5  
        PointPickup(position=Vec3(x, y, z))

# spawn_points(num_points=100)

# road_segment = Entity(
#     model='plane',
#     scale=(52, 1, 13),
#     texture="/assets/textures/road.jpg",
#     texture_scale=(2, 2),
#     collider='box',
#     position=(70,0.1,-5),
#     rotation=(0, 0, 0)
# )

# road_segment_2 = Entity(
#     model='plane',
#     scale=(52, 1, 13),
#     texture="/assets/textures/road.jpg",
#     texture_scale=(2, 2),
#     collider='box',
#     position=(102.5,0.1,-5),
#     rotation=(0, 90, 0)
# )

# road_segment_3 = Entity(
#     model='plane',
#     scale=(52, 1, 13),
#     texture="/assets/textures/road.jpg",
#     texture_scale=(2, 2),
#     collider='box',
#     position=(102.5,0.1,-57),
#     rotation=(0, 90, 0)
# )

# road_segment_4 = Entity(
#     model='plane',
#     scale=(70, 1, 13),
#     texture="/assets/textures/road.jpg",
#     texture_scale=(2, 2),
#     collider='box',
#     position=(70, 0.1, -57),  # bottom horizontal segment
#     rotation=(0, 90, 0)
# )

# # Top horizontal (closing top side of square)
# road_segment_5 = Entity(
#     model='plane',
#     scale=(70, 1, 13),
#     texture="/assets/textures/road.jpg",
#     texture_scale=(2, 2),
#     collider='box',
#     position=(70, 0.1, 20),  # Above road_segment
#     rotation=(0, 0, 0)
# )

# # Bottom horizontal (closing bottom side of square)
# road_segment_6 = Entity(
#     model='plane',
#     scale=(70, 1, 13),
#     texture="/assets/textures/road.jpg",
#     texture_scale=(2, 2),
#     collider='box',
#     position=(70, 0.1, -83),  # Below road_segment_4
#     rotation=(0, 0, 0)
# )


# crossroad = Entity(
#     model='plane',
#     scale=(52, 1, 13),
#     texture="/assets/textures/road.jpg",  # Optional: use a cross texture
#     texture_scale=(1, 1),
#     collider='box',
#     position=(85, 0.1, -31),  # center of the square
#     rotation=(0, 0, 0)
# )

# road_left = Entity(
#     model='plane',
#     scale=(52, 1, 13),
#     texture="/assets/textures/road.jpg",
#     texture_scale=(2, 2),
#     collider='box',
#     position=(37.5, 0.1, -5),
#     rotation=(0, 90, 0)
# )

# # Top vertical (mirroring bottom road_segment_3)
# road_top = Entity(
#     model='plane',
#     scale=(70, 1, 13),
#     texture="/assets/textures/road.jpg",
#     texture_scale=(2, 2),
#     collider='box',
#     position=(70, 0.1, 35),  # Top side
#     rotation=(0, 0, 0)
# )

# # Bottom vertical (extending bottom edge)
# road_bottom = Entity(
#     model='plane',
#     scale=(70, 1, 13),
#     texture="/assets/textures/road.jpg",
#     texture_scale=(2, 2),
#     collider='box',
#     position=(70, 0.1, -83),  # Bottom side
#     rotation=(0, 0, 0)
# )

# === ROADS LAYOUT ===

# Horizontal Roads (Top, Middle, Bottom)
road_top = Entity(
    model='plane',
    scale=(80, 1, 13),
    texture="/assets/textures/road.jpg",
    texture_scale=(4, 2),
    collider='box',
    position=(85, 0.1, 44),
    rotation=(0, 0, 0)
)

road_middle = Entity(
    model='plane',
    scale=(80, 1, 13),
    texture="/assets/textures/road.jpg",
    texture_scale=(4, 2),
    collider='box',
    position=(85, 0.1, -4),
    rotation=(0, 0, 0)
)

road_bottom = Entity(
    model='plane',
    scale=(80, 1, 13),
    texture="/assets/textures/road.jpg",
    texture_scale=(4, 2),
    collider='box',
    position=(85, 0.1, -80),
    rotation=(0, 0, 0)
)

# Vertical Roads (Left, Center, Right)
road_left = Entity(
    model='plane',
    scale=(80, 1, 13),
    texture="/assets/textures/road.jpg",
    texture_scale=(4, 2),
    collider='box',
    position=(40, 0.1, 0),
    rotation=(0, 90, 0)
)

road_center = Entity(
    model='plane',
    scale=(80, 1, 13),
    texture="/assets/textures/road.jpg",
    texture_scale=(4, 2),
    collider='box',
    position=(85, 0.1, 0),
    rotation=(0, 90, 0)
)

road_right = Entity(
    model='plane',
    scale=(142, 1, 13),
    texture="/assets/textures/road.jpg",
    texture_scale=(4, 2),
    collider='box',
    position=(131.5, 0.1, -20),
    rotation=(0, 90, 0)
)

# Central Crossroad (optional distinct visual)
crossroad = Entity(
    model='plane',
    scale=(13, 1, 13),
    texture="/assets/textures/road.jpg",
    texture_scale=(1, 1),
    collider='box',
    position=(85, 0.1, 0),
    rotation=(0, 0, 0)
)


house1 = Entity(
    model='assets/models/house.glb',
    collider='box',
    scale=0.15,
    position=(50, 0.1, 6)
)

house2 = Entity(
    model='assets/models/lp_japnes_house.glb',
    collider='box',
    scale=3.8,
    position=(56, -1.8, -27)
)

school = Entity(
    model='assets/models/school.glb',
    collider='box',
    scale=1.5,
    position=(85, 0, 20),
    rotation=(0,-90,0)
)

factory1 = Entity(
    model='assets/models/factory.glb',
    collider='box',
    scale=1,
    position=(85, 0, -20),
    rotation=(0,-90,0)
)

garden = Entity(
    model='assets/models/garden.glb',
    collider='box',
    scale=0.85,
    position=(85, -0.5, -50),
    rotation=(0,-90,0)
)

clinic = Entity(
    model='assets/models/clinic.glb',
    collider='box',
    scale=0.0175,
    position=(105, -0.5, 100),
    rotation=(0,0,0)
)

def bins(n):
    for i in range(n):
        bin1 = Entity(
            model='assets/models/trash_can.glb',
            collider='box',
            scale=2.5,
            position=(55+i*15, 0.1, 3)
        )
        bin1.is_trash_can = True  # ✅ Mark for detection

        bin2 = Entity(
            model='assets/models/trash_can.glb',
            collider='box',
            scale=2.5,
            position=(55+i*15, 0.1, -12)
        )
        bin2.is_trash_can = True

bins(3)

def lights(n):



    # === Horizontal Roads ===

    for x in range(46, 131, 15):  # X positions along the road

        # Top road (Z=40)

        Entity(model='assets/models/lights.glb', collider='box', scale=0.4,

               color=color.black, position=(x, 0.1, 51), rotation=(0, 90, 0))

        Entity(model='assets/models/lights.glb', collider='box', scale=0.4,

               color=color.black, position=(x, 0.1, 37), rotation=(0, -90, 0))



        # Middle road (Z=0)

        Entity(model='assets/models/lights.glb', collider='box', scale=0.4,

               color=color.black, position=(x, 0.1, -11), rotation=(0, -90, 0))

        Entity(model='assets/models/lights.glb', collider='box', scale=0.4,

               color=color.black, position=(x, 0.1, 2.5), rotation=(0, 90, 0))



        # Bottom road (Z=-40)

        Entity(model='assets/models/lights.glb', collider='box', scale=0.4,

               color=color.black, position=(x, 0.1, -70), rotation=(0, 90, 0))

        Entity(model='assets/models/lights.glb', collider='box', scale=0.4,

               color=color.black, position=(x, 0.1, -90), rotation=(0, -90, 0))

lights(4)

# def lights(n):
#     for i in range(n):
#         bin = Entity(
#             model='assets/models/lights.glb',
#             collider='box',
#             color=color.black,
#             scale=0.4,
#             position=(47.5+i*15, 0.1, 3),
#             rotation=(0,90,0)
#         )

#         bin = Entity(
#             model='assets/models/lights.glb',
#             collider='box',
#             color=color.black,
#             scale=0.4,
#             position=(47.5+i*15, 0.1, -12),
#             rotation=(0,-90,0)
#         )

# lights(4)

# def more_lights(n):
#     for i in range(n):
#         # Left side of bottom road
#         Entity(
#             model='assets/models/lights.glb',
#             collider='box',
#             color=color.black,
#             scale=0.4,
#             position=(47.5+i*15, 0.1, -64),
#             rotation=(0,90,0)
#         )

#         # Right side of bottom road
#         Entity(
#             model='assets/models/lights.glb',
#             collider='box',
#             color=color.black,
#             scale=0.4,
#             position=(47.5+i*15, 0.1, -50),
#             rotation=(0,-90,0)
#         )

# more_lights(4)

def input(key):
    global held_left, held_right

    # Pick up object
    if key == 'e':
        ray = raycast(camera.world_position, camera.forward, distance=pickup_distance, ignore=(player,))
        if ray.hit and hasattr(ray.entity, 'is_holdable') and ray.entity.is_holdable:
            item = ray.entity
            if not held_right:
                held_right = item
                item.parent = camera
                item.position = Vec3(0.675, -0.2, 1)  # local to camera
                item.rotation = Vec3(0, 0, 0)  # Reset rotation
                item.is_thrown = False

    
    # Offhand grabbing
    if key == 'f':
        ray = raycast(camera.world_position, camera.forward, distance=pickup_distance, ignore=(player,))
        if ray.hit and hasattr(ray.entity, 'is_holdable') and ray.entity.is_holdable:
            item = ray.entity
            if not held_left:
                held_left = item
                item.parent = camera
                item.position = Vec3(-0.675, -0.2, 1)
                item.rotation = Vec3(0, 0, 0)
                item.is_thrown = False

    # Drop / Throw object
    if key == 'q':
        thrown = None

        if held_right:
            thrown = held_right
            held_right = None
        elif held_left:
            thrown = held_left
            held_left = None

        if thrown:
            thrown.parent = scene
            thrown.scale = 0.5

            forward = camera.forward.normalized()
            start_pos = camera.world_position + forward * 1.5 + Vec3(0, 0, 0)
            target_point = start_pos + forward * 5 + Vec3(uniform(-0.1, 0.1), 0.1, uniform(-0.1, 0.1))

            thrown.world_position = start_pos
            thrown.collider = None

            def on_landed():
                thrown.collider = 'box'

                # Check distance to hospital
                if hasattr(thrown, 'is_holdable'):
                    dist = distance(thrown.position, clinic.position)
                    if dist < 30:  # within range
                        global player_points
                        player_points += 10
                        points_text.text = f'Points: {player_points}'

            thrown.animate_position(target_point, duration=0.35, curve=curve.out_circ)
            invoke(on_landed, delay=0.35)


class HoldableItem(Entity):
    def __init__(self, position=(0, 1, 0), model='cube', color=color.azure, scale=0.5):
        super().__init__(
            model=model,
            color=color,
            scale=scale,
            position=position,
            collider='box'
        )
        self.is_holdable = True

holdable_items = []
trash_items=[]



def spawn_trash(n=5):

    for _ in range(n):

        # Define city area limits (customize as needed)

        min_x, max_x = 40, 130

        min_z, max_z = -70, 25





        # Avoid spawning in restricted zones (e.g., inside walls or buildings)

        pos_x = uniform(min_x, max_x)

        pos_z = uniform(min_z, max_z)



        # Place trash slightly above the ground

        trash = Entity(

            model='assets/models/trash.glb',

            collider='box',

            position=(pos_x, 0.1, pos_z),

            scale=0.5

        )

        trash.is_trash = True

        trash.is_holdable = True

        trash.is_thrown = False

        trash.velocity = Vec3(0, 0, 0)

        trash.angular_velocity = Vec3(0, 0, 0)


sapling_items = []

def spawn_tree_saplings(n=6):
    for _ in range(n):
        x = uniform(40, 130)
        z = uniform(-70, 25)
        sapling = Tree(position=(x, 0.1, z))
        sapling_items.append(sapling)
        holdable_items.append(sapling)

spawn_tree_saplings()

class Pill(Entity):
    def __init__(self, position):
        super().__init__(
            model='assets/models/pills.glb',
            position=position,
            scale=6,
            collider='box'
        )
        self.is_holdable = True 

# def spawn_pills_around_hospital(count=10, center=Vec3(105, 0.1, 100), radius=10):
#     for _ in range(count):
#         x_offset = uniform(-radius, radius)
#         z_offset = uniform(-radius, radius)
#         pos = center + Vec3(x_offset, 0.5, z_offset)
#         Pill(position=pos)

# spawn_pills_around_hospital()

def spawn_random_pills(count=50, area_size=300):
    for _ in range(count):
        x = uniform(-area_size, area_size)
        z = uniform(-area_size, area_size)
        y = 0.1  # slightly above ground
        Pill(position=Vec3(x, y, z))

spawn_random_pills()

trash = Entity(
    model='assets/models/trash.glb',
    scale=0.3,
    position=(2, 0, 2),
    collider='box',
    is_trash=True
)
trash.is_holdable = True
trash.is_thrown = False
holdable_items.append(trash)


holdable_items.append(HoldableItem(position=(2, 0.5, 2), color=color.orange))
holdable_items.append(HoldableItem(position=(-2, 0.5, -2), color=color.yellow))
holdable_items.append(HoldableItem(position=(0, 0.5, 4), color=color.cyan))

# === UPDATE ===
def update():
    global pitch, yaw, velocity_y, is_grounded, player_points, game_over
    global eye_height, target_eye_height, target_scale_y, bobbing_time, x_bob, y_bob

    if game_over:
        return

    # === Mouse Look ===
    if mouse.locked:
        dx = mouse.velocity[0] * sensitivity
        dy = mouse.velocity[1] * sensitivity
        yaw += dx
        pitch -= dy
        pitch = clamp(pitch, -max_pitch, max_pitch)
        camera.rotation_x = pitch
        player.rotation_y = yaw
        camera.rotation_y = yaw
        camera.rotation_z = 0

    # === Camera Position ===
    camera.position = player.position + Vec3(0, eye_height, 0)

    # === Movement Input ===
    forward = Vec3(sin(radians(yaw)), 0, cos(radians(yaw))).normalized()
    right = Vec3(forward.z, 0, -forward.x).normalized()

    move = Vec3(right * (held_keys['d'] - held_keys['a']) + forward * (held_keys['w'] - held_keys['s']))
    if move != Vec3(0, 0, 0):
        move = move.normalized()

    move_speed = sprint_speed if held_keys['shift'] and held_keys['w'] else normal_speed
    player.position += move * time.dt * move_speed

    # === Gravity and Jump ===
    surface_y = ground.position.y + ground.scale_y / 2
    if is_grounded and held_keys['space']:
        velocity_y += jump_height
    else:
        velocity_y -= gravity * time.dt

    player.y += velocity_y * time.dt

    if player.y < surface_y:
        player.y = surface_y
        velocity_y = 0
        is_grounded = True
    else:
        is_grounded = False

    # === Point Pickup Collection ===
    for pickup in point_pickups:
        if distance(player.position, pickup.position) < 1:
            player_points += pickup.value
            points_text.text = f'Points: {player_points}'
            pickup.disable()
            point_pickups.remove(pickup)

    # === Smooth Crouch ===
    if held_keys['left control']:
        target_scale_y = crouch_height
        target_eye_height = 0.9
    else:
        target_scale_y = stand_height
        target_eye_height = 1.8

    player.scale_y = lerp(player.scale_y, target_scale_y, 6 * time.dt)
    eye_height = lerp(eye_height, target_eye_height, 6 * time.dt)

    # === Highlight Holdables ===
    hovered_holdable = None
    ray = raycast(camera.world_position, camera.forward, distance=pickup_distance, ignore=(player,))
    if ray.hit and hasattr(ray.entity, 'is_holdable') and ray.entity.is_holdable:
        hovered_holdable = ray.entity

    for e in scene.entities:
        if hasattr(e, 'is_holdable'):
            e.highlight_color = color.lime if e == hovered_holdable else color.clear

    # === Hand Positioning ===
    hand_right.position = Vec3(0.35, -0.20, 0.4)
    hand_left.position = Vec3(-0.35, -0.20, 0.4)

    # === COORDS ===
    coord_text.text = f'Coordinates: {round(player.x,1)}, {round(player.y,1)}, {round(player.z,1)}'

    # === Thrown Trash Logic ===
    for item in holdable_items[:]:
        if hasattr(item, 'is_thrown') and item.is_thrown:
            if hasattr(item.model, 'name') and item.model.name.endswith('trash.glb'):
                for bin in scene.entities:
                    if hasattr(bin, 'is_trash_can') and distance(item.world_position, bin.world_position) < 2.5:
                        print("Trash scored!")
                        player_points += 10
                        points_text.text = f'SDG Points: {player_points}'
                        item.disable()
                        holdable_items.remove(item)
                        break

            # Thrown item physics
            if not hasattr(item, 'velocity'):
                item.velocity = Vec3(0, 0, 0)
            if not hasattr(item, 'angular_velocity'):
                item.angular_velocity = Vec3(0, 0, 0)

            item.velocity.y -= gravity * time.dt
            item.position += item.velocity * time.dt

            item.rotation_x += item.angular_velocity.x * time.dt
            item.rotation_y += item.angular_velocity.y * time.dt
            item.rotation_z += item.angular_velocity.z * time.dt

            # Collision with ground
            ground_y = ground.y + 0.5
            if item.y <= ground_y:
                item.y = ground_y
                item.velocity = Vec3(0, 0, 0)
                item.angular_velocity *= 0.8

                if item.angular_velocity.length() < 1:
                    if not hasattr(item, 'upright_timer'):
                        item.upright_timer = 0
                    item.upright_timer += time.dt

                    target_rot = Vec3(0, item.rotation.y, 0)
                    item.rotation = lerp(item.rotation, target_rot, 6 * time.dt)

                    if item.upright_timer > 0.5:
                        item.rotation = target_rot
                        item.angular_velocity = Vec3(0, 0, 0)
                        item.is_thrown = False
                        del item.upright_timer
    
        for sapling in sapling_items:

            if mouse.right and held_right == sapling and not sapling.is_planted:

                # Cast a ray downward from the player's view to detect ground

                target_pos = camera.world_position + camera.forward * 2 + Vec3(0, -1.5, 0)



                ground_hit = raycast(

                    origin=target_pos + Vec3(0, 2, 0),

                    direction=Vec3(0, -1, 0),

                    distance=5,

                    ignore=[player, camera],

                )



                if not ground_hit.hit:

                    print("No ground detected.")

                    continue



                # 🌿 Ensure the hit object is actually the grass ground

                if ground_hit.entity != ground:
                
                    print("Can only plant on grass.")
    
                    continue



                # Prevent planting too close to other objects

                overlap = [e for e in scene.entities if e.collider and e != sapling and distance(e.position, ground_hit.world_point) < 1.5]



                if overlap:

                    print("Can't plant here! Something is in the way.")

                    continue



                sapling.is_planted = True

                sapling.rotation = (0, 0, 0)

                sapling.animate_scale(2, duration=0.4)

                held_right = None

                sapling.parent = scene

                sapling.position = ground_hit.world_point + Vec3(0, 0.1, 0)



                player_points += 10

                points_text.text = f"Points: {player_points}"

app.run()
