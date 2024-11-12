import pygame
import random
import math

# Inicializa Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Recoger Pelotas")

# Configuración del jugador
player_size = 50
player_color = (0, 0, 255)
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 0.4  # Velocidad de movimiento ajustada

# Configuración de las pelotas
max_balls = 80  # Número máximo de pelotas
ball_radius = 9  # Radio de las pelotas normales
ball_color = (255, 0, 0)  # Color de las pelotas normales
balls = []  # Lista de pelotas normales

# Configuración de las pelotas especiales
special_ball_radius = 30  # Radio de las pelotas especiales
special_ball_color = (0, 255, 0)  # Color de las pelotas especiales
special_balls = []  # Lista de pelotas especiales
special_ball_time = 0  # Tiempo para generar pelotas especiales
special_ball_frequency = 3000  # Generación cada 3000ms (3 segundos)

# Variables de tiempo
last_ball_time = 0  # Tiempo del último evento de pelotas generadas

# Puntuación
score = 0  # Puntuación inicial

# Función para comprobar la colisión
def check_collision(player_pos, ball_pos, ball_radius):
    player_center = (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2)
    ball_center = (ball_pos[0], ball_pos[1])
    distance = math.sqrt((player_center[0] - ball_center[0]) ** 2 + (player_center[1] - ball_center[1]) ** 2)
    return distance < (player_size // 2 + ball_radius)

# Función para mover pelotas especiales hacia el jugador
def move_towards_player(ball_pos, player_pos, speed=0.1):
    direction_x = player_pos[0] - ball_pos[0]
    direction_y = player_pos[1] - ball_pos[1]
    distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
    
    if distance > 0:
        direction_x /= distance
        direction_y /= distance
        ball_pos[0] += direction_x * speed
        ball_pos[1] += direction_y * speed

# Bucle principal del programa
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()
    
    # Movimiento del jugador
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += player_speed
    
    # Comprobar si han pasado 500ms (medio segundo) para generar pelotas normales
    current_time = pygame.time.get_ticks()
    if current_time - last_ball_time > 500 and len(balls) < max_balls:
        # Generar una pelota en una posición aleatoria
        ball_pos = [random.randint(ball_radius, WIDTH - ball_radius), random.randint(ball_radius, HEIGHT - ball_radius)]
        balls.append(ball_pos)
        last_ball_time = current_time  # Actualizar el tiempo del último evento
    
    # Comprobar si han pasado el tiempo de frecuencia para pelotas especiales
    if current_time - special_ball_time > special_ball_frequency:
        # Generar una pelota especial en una posición aleatoria
        special_ball_pos = [random.randint(special_ball_radius, WIDTH - special_ball_radius), random.randint(special_ball_radius, HEIGHT - special_ball_radius)]
        special_balls.append(special_ball_pos)
        special_ball_time = current_time  # Actualizar el tiempo de última pelota especial
    
    # Mover pelotas especiales hacia el jugador
    for special_ball in special_balls:
        move_towards_player(special_ball, player_pos, speed=0.05)
    
    # Comprobar las colisiones con las pelotas normales
    for ball in balls[:]:
        if check_collision(player_pos, ball, ball_radius):
            balls.remove(ball)  # Eliminar la pelota de la lista
            score += 1  # Aumentar el score
    
    # Comprobar las colisiones con las pelotas especiales
    for special_ball in special_balls[:]:
        if check_collision(player_pos, special_ball, special_ball_radius):
            running = False  # Fin del juego si el jugador toca una pelota especial
    
    # Relleno de la pantalla en blanco
    screen.fill((255, 255, 255))
    
    # Dibujar el jugador
    pygame.draw.rect(screen, (0, 0, 255), (*player_pos, player_size, player_size))
    
    # Dibujar las pelotas normales
    for ball in balls:
        pygame.draw.circle(screen, ball_color, ball, ball_radius)
    
    # Dibujar las pelotas especiales
    for special_ball in special_balls:
        pygame.draw.circle(screen, special_ball_color, special_ball, special_ball_radius)
    
    # Mostrar el contador de puntuación
    font = pygame.font.SysFont("Marven Pro", 30)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))  # Dibujar el score en la esquina superior izquierda
    
    # Actualización de pantalla
    pygame.display.flip()

# Cierre de Pygame
pygame.quit()