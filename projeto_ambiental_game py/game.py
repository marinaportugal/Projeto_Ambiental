import pygame
import random


def carregar(nome, tamanho, alpha=True):
    imagem = pygame.image.load(f"imagens/{nome}")
    imagem = imagem.convert_alpha() if alpha else imagem.convert()
    return pygame.transform.scale(imagem, tamanho)


def game():
    ALTURA, LARGURA = 600, 1000
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Reciclando")
    clock = pygame.time.Clock()

    background = carregar("rua.jpg", (LARGURA, ALTURA), False)
    background_x = 0
    player = carregar("personagem.png", (300, 200))
    obstaculo = carregar("obstaculo.png", (150, 100))
    obstaculo_x = 400
    obstaculo_y = 480

    objetos = {
        nome: carregar(arquivo, tamanho)
        for nome, arquivo, tamanho in [
            ("garrafa", "bottle.png", (100, 100)),
            ("saco", "saco.png", (80, 80)),
            ("embalagem", "embalagem.png", (100, 100)),
            ("lata", "lata.png", (60, 80)),
            ("parafuso", "parafuso.png", (70, 70)),
            ("copo", "garrafa_vidro.png", (50, 70)),
            ("vidro", "vidro.png", (80, 80)),
            ("jornal", "jornal.png", (80, 100)),
            ("caixa", "box.png", (80, 100)),
        ]
    }

    player_largura, player_altura = 300, 200
    player_x = 0
    player_y = 400
    velocidade_y = 0
    jumping = False

    pontos = 0
    vida = 3
    fase = 1
    fonte = pygame.font.Font(None, 36)
    fonte_titulo = pygame.font.Font(None, 60)
    fonte_subtitulo = pygame.font.Font(None, 28)

    fases = {
        1: ("Plástico", ["garrafa", "saco", "embalagem"], (220, 40, 40)),
        2: ("Metal", ["lata", "parafuso"], (255, 220, 0)),
        3: ("Vidro", ["copo", "vidro"], (0, 170, 80)),
        4: ("Papel", ["jornal", "caixa"], (40, 100, 220)),
    }

    def gerar_x_coleta():
        while True:
            x = LARGURA + random.randint(200, 1200)
            if abs(x - obstaculo_x) > 220:
                return x

    def criar_coletas():
        return [[random.choice(fases[fase][1]), gerar_x_coleta(), 480] for _ in range(3)]

    def desenhar_fundo():
        for deslocamento in (0, LARGURA, -LARGURA):
            tela.blit(background, (background_x + deslocamento, 0))

    coletas = criar_coletas()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_ESCAPE]:
            pygame.quit()
            return

        player_x += 5 * (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT])

        if teclas[pygame.K_UP] and not jumping:
            jumping = True
            velocidade_y = -12

        background_x = (background_x - 3) % LARGURA

        obstaculo_x -= 5

        if obstaculo_x < -150:
            obstaculo_x = LARGURA + random.randint(200, 600)

        for item in coletas:
            item[1] -= 5
            if item[1] < -100:
                item[:2] = random.choice(fases[fase][1]), gerar_x_coleta()

        velocidade_y += 0.5
        player_y += velocidade_y

        if player_y >= ALTURA - player_altura:
            player_y, velocidade_y, jumping = ALTURA - player_altura, 0, False

        player_x = max(0, min(player_x, LARGURA - player_largura))

        player_rect = pygame.Rect(player_x + 150, player_y - 80, 20, 200)

        obstaculo_rect = pygame.Rect(obstaculo_x, obstaculo_y, 150, 100)

        if player_rect.colliderect(obstaculo_rect):

            player_x, player_y, velocidade_y, jumping = 0, 400, 0, False
            vida -= 1
            obstaculo_x = LARGURA + random.randint(200, 600)
            print(f"Colisão detectada!\nVida: {vida}")

            if vida <= 0:
                print("Game Over!")
                pygame.quit()
                return

        for item in coletas:

            if player_rect.colliderect(pygame.Rect(item[1], item[2], 100, 100)):
                pontos += 1
                print(f"Pontos: {pontos}")
                item[:2] = (random.choice(fases[fase][1]),
                            LARGURA + random.randint(300, 700))

        nova_fase = min(4, pontos // 10 + 1)

        if nova_fase != fase:

            fase = nova_fase
            coletas = criar_coletas()

            print(f"FASE {fase} - {fases[fase][0]}")

        if pontos >= 40:
            desenhar_fundo()
            for texto, fonte_atual, y in (("Parabéns!", fonte_titulo, 220),
                                           ("Você completou o jogo!", fonte, 290)):
                mensagem = fonte_atual.render(texto, True, (0, 0, 0))
                tela.blit(mensagem, (LARGURA // 2 - mensagem.get_width() // 2, y))
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            return

        desenhar_fundo()
        tela.blit(player, (player_x, player_y))
        tela.blit(obstaculo, (obstaculo_x, obstaculo_y))
        for nome, x, y in coletas:
            tela.blit(objetos[nome], (x, y))

        nome_fase, cor_fase = fases[fase][0], fases[fase][2]
        textos = ((f"Pontos: {pontos}", fonte, (10, 10), (255, 255, 255)),
                  (f"Vida: {vida}", fonte, (10, 50), (255, 255, 255)),
                  (f"Lixeira {['Vermelha', 'Amarela', 'Verde', 'Azul'][fase - 1]} - {nome_fase}",
                   fonte_titulo, (250, 10), cor_fase),
                  (f"Fase {fase}/4 - Colete os objetos de {nome_fase.lower()}!",
                   fonte_subtitulo, (300, 75), (0, 0, 0)))
        for texto, fonte_atual, posicao, cor in textos:
            tela.blit(fonte_atual.render(texto, True, cor), posicao)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    game()