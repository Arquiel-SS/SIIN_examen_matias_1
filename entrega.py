import pygame

# Configuración inicial
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (50, 50, 50)  # Color predeterminado por si no hay imagen
ERIZO_SPEED = 5

# Cargar el fondo y el splash art del erizo
background_image = pygame.image.load("img/fondo.jpg")  # Asegúrate de que la ruta sea correcta
erizo_image = pygame.image.load("img/erizo.png")  # Asegúrate de que la ruta sea correcta

# Redimensionar la imagen del erizo si es necesario
erizo_image = pygame.transform.scale(erizo_image, (300, 300))  # Ajustar tamaño del erizo

def initialize_pygame():
    """Inicializa pygame y crea la ventana."""
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT))

def main_loop(screen, background_image, erizo_image):
    """Bucle principal de la aplicación."""
    clock = pygame.time.Clock()
    running = True

    # Posición inicial del erizo
    erizo_x = WIDTH // 2
    erizo_y = HEIGHT // 2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obtener teclas presionadas para mover el erizo
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # Mover a la izquierda
            erizo_x -= ERIZO_SPEED
        if keys[pygame.K_RIGHT]:  # Mover a la derecha
            erizo_x += ERIZO_SPEED

        # Limitar el movimiento del erizo para que no se salga de la pantalla
        erizo_x = max(0, min(erizo_x, WIDTH - erizo_image.get_width()))

        # Dibujar el fondo y el erizo
        screen.blit(background_image, (0, 0))  # Fondo
        screen.blit(erizo_image, (erizo_x, erizo_y))  # Erizo

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def run():
    """Función principal para iniciar el programa."""
    screen = initialize_pygame()
    main_loop(screen, background_image, erizo_image)

# Ejecutar el programa
if __name__ == "__main__":
    run()