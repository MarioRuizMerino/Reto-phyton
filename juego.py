from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Suelo amplio
ground = Entity(
    model='plane',
    scale=(200, 1, 200),
    texture='white_cube',
    texture_scale=(100, 100),
    collider='box',
    color=color.rgb(50,150,50)
)

# # Pequeñas montañas/colinas con cubos para dar relieve
# for x in range(-20, 21, 4):
#     for z in range(-20, 21, 4):
#         h = random.choice([0, 0, 1, 2])
#         if h > 0:
#             Entity(
#                 model='cube',
#                 color=color.lime.tint(-0.1 * h),
#                 scale=(3, h, 3),
#                 position=(x * 2, h / 2, z * 2),
#                 collider='box'
#             )

# Cielo y ambiente
Sky()

# Jugador: controlador en primera persona (WASD + ratón)
player = FirstPersonController()
player.speed = 5

# Menú de pausa (Escape): panel con botones para continuar o salir
menu = Entity(parent=camera.ui, model='quad', scale=(0.5, 0.45), color=color.rgba(0, 0, 0, 190), enabled=False)
Text('Pausa', parent=menu, y=0.2, scale=2, color=color.white)
resume_btn = Button(text='Continuar', parent=menu, scale=(0.6, 0.12), y=0.04)
quit_btn = Button(text='Salir', parent=menu, scale=(0.6, 0.12), y=-0.14)

def resume():
    menu.enabled = False
    player.enabled = True
    mouse.locked = True

def quit_game():
    application.quit()

resume_btn.on_click = resume
quit_btn.on_click = quit_game

def input(key):
    if key == 'escape':
        menu.enabled = not menu.enabled
        player.enabled = not menu.enabled
        mouse.locked = not menu.enabled

# Bloqueamos el ratón al iniciar para permitir mirar con el ratón
mouse.locked = True

app.run()
