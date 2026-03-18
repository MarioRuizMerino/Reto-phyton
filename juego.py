from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Suelo amplio
laberinto = Entity(
    model='assets/laberinto.obj',
    scale=0.5,
    texture='assets/textura-pared.jpeg',
    position=(-17.5, 0, -16.5),
    collider='mesh',
)

barriles = Entity(
    model='assets/barril.obj',
    scale=0.5,
    position=(-17.5, 0, -16.5),
    collider='mesh'
)

cristal = Entity(
    model='assets/cristal.obj',
    scale=0.5,
    position=(-17.5, 0, -16.5),
    collider='mesh',
    color=color.rgba(180, 220, 255, 120)
)
cristal.alpha = 0.2

#Esto es para las paredes anti caída y evitar que te caigas al vacío
paredes = Entity(
    model='assets/paredes.obj',
    scale=0.5,
    position=(-17.5, 0, -16.5),
    collider='mesh'
)
paredes.alpha = 0.00001

palanca = Entity(
    model='palanca1.obj',
    position=(-3.66, -3.5, -1.71),
    scale=0.5,
    collider='mesh'
)

Sky()


# ──────────────────────────────────────────────
# BOLAS: coordenadas predefinidas (ajústalas tú)
# ──────────────────────────────────────────────
BALL_POSITIONS = [
    (-27.5,   1,  -25),
    (-34,  1, -4.22),
    (-13,   1, -4.5),
    (-38, 1,  -35),
    (-5,   1, 4),
    (-5,  1, -4),
    (-5,  1,  -35),
    (-34,  1, -34),
    (-34,   1, 4),
    (-1, 1, -1),
]

balls = []
for pos in BALL_POSITIONS:
    ball = Entity(
        model='assets/bola.obj',
        scale=0.5,
        position=pos,
        collider='sphere',
        #color=color.rgba(180, 220, 255, 120)
    )
    ball.alpha = 0.8
    balls.append(ball)



# ──────────────────────────────────────────────
# CONTADOR EN PANTALLA
# ──────────────────────────────────────────────
collected = 0
total = len(balls)

counter_text = Text(
    text=f'Bolas: {collected} / {total}',
    position=(-0.85, 0.45),
    scale=2,
    color=color.white,
    background=True,
)
pos_text = Text(
    text='X: 0.00  Y: 0.00  Z: 0.00',
    position=(-0.85, 0.38),
    scale=1.5,
    color=color.cyan,
    background=True,
)
activada = False

def update():
    global collected, activada
    for ball in balls[:]:          # copia para poder modificar la lista
        if ball.enabled and distance(player, ball) < 1.2:
            ball.enabled = False
            balls.remove(ball)
            collected += 1
            counter_text.text = f'Bolas: {collected} / {total}'
            if collected == total:
                counter_text.text = '¡Has recogido todas las bolas!'
    pos_text.text = f'X: {player.x:.2f}  Y: {player.y:.2f}  Z: {player.z:.2f}'
    if distance(player, palanca) < 1.2 and not activada:
        palanca.model = 'palanca.obj'
        activada = True
        destroy(cristal)

# ──────────────────────────────────────────────
# MENÚ DE PAUSA
# ──────────────────────────────────────────────
menu = Entity(
    parent=camera.ui,
    model='quad',
    scale=(0.5, 0.45),
    color=color.rgba(0, 0, 0, 190),
    enabled=False,
)
Text('Pausa', parent=menu, y=0.2, scale=2, color=color.white)
resume_btn = Button(text='Continuar', parent=menu, scale=(0.6, 0.12), y=0.04)
quit_btn   = Button(text='Salir',     parent=menu, scale=(0.6, 0.12), y=-0.14)

def resume():
    menu.enabled = False
    player.enabled = True
    mouse.locked = True

def quit_game():
    application.quit()

resume_btn.on_click = resume
quit_btn.on_click   = quit_game

def input(key):
    if key == 'escape':
        menu.enabled = not menu.enabled
        player.enabled = not menu.enabled
        mouse.locked = not menu.enabled


# Jugador
player = FirstPersonController()
player.speed = 8
player.collider = ('capsule')
player.continuous_collision = True

mouse.locked = True
app.run()