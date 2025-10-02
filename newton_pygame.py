import pygame
pygame.init()


WIDTH, HEIGHT = 900, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador - Leyes de Newton")

# Colores
WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)

# pelota
x, y = WIDTH // 4, HEIGHT // 2
vx, vy = 0, 0
m = 1.0
fuerza = 1.0  # magnitud de la fuerza aplicada

# Estados de las leyes
ley1, ley2, ley3 = True, True, True  # activadas por defecto

# Reloj
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 28)

# Definir botones
button_accel = pygame.Rect(WIDTH - 120, 100, 100, 50)   # botón verde acelerar
button_brake = pygame.Rect(WIDTH - 120, 200, 100, 50)   # botón azul frenar

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Teclas para activar/desactivar leyes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                ley1 = not ley1
            if event.key == pygame.K_2:
                ley2 = not ley2
            if event.key == pygame.K_3:
                ley3 = not ley3
            if event.key == pygame.K_q:
                running = False

        # Clic en botones
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_accel.collidepoint(event.pos):
                vx += 2  # acelerar en x
            if button_brake.collidepoint(event.pos):
                vx *= 0.5  # frenar: reducir velocidad a la mitad

    keys = pygame.key.get_pressed()

    # 2da ley: F = m * a (aplicar fuerza con flechas) 
    if ley2:
        if keys[pygame.K_LEFT]:
            vx -= fuerza / m
        if keys[pygame.K_RIGHT]:
            vx += fuerza / m
        if keys[pygame.K_UP]:
            vy -= fuerza / m
        if keys[pygame.K_DOWN]:
            vy += fuerza / m

    # 1ra ley: Inercia
    if not ley1:
        # Si está desactivada, frena el objeto (como si hubiera friccion irreal)
        vx *= 0.9
        vy *= 0.9

    # Actualizar posición
    x += vx
    y += vy

    # 3ra ley Acción y reaccion 
    if ley3:
        if x - 20 < 0:
            x = 20
            vx *= -1
        if x + 20 > WIDTH - 150:  # limite antes de los botones
            x = WIDTH - 150 - 20
            vx *= -1
        if y - 20 < 0:
            y = 20
            vy *= -1
        if y + 20 > HEIGHT:
            y = HEIGHT - 20
            vy *= -1

    # Dibujar
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (int(x), int(y)), 20)

    # Dibujar botones
    pygame.draw.rect(screen, GREEN, button_accel)
    pygame.draw.rect(screen, BLUE, button_brake)
    accel_text = font.render("Acelerar", True, BLACK)
    brake_text = font.render("Frenar", True, BLACK)
    screen.blit(accel_text, (button_accel.x + 10, button_accel.y + 15))
    screen.blit(brake_text, (button_brake.x + 15, button_brake.y + 15))

    # Mostrar estado de las leyes
    text = f"Ley1(Inercia): {'ON' if ley1 else 'OFF'} | " \
           f"Ley2(F=ma): {'ON' if ley2 else 'OFF'} | " \
           f"Ley3(Accion-Reaccion): {'ON' if ley3 else 'OFF'} " \
           f"| Q: Salir"
    label = font.render(text, True, BLACK)
    screen.blit(label, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
