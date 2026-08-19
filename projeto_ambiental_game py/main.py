import pygame
import sys

pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Quiz Verde")

# Fontes
fonte_pergunta = pygame.font.Font(None, 40)
fonte_resposta = pygame.font.Font(None, 30)
fonte_resultado = pygame.font.Font(None, 45)

# Cores
BRANCO = (255, 255, 255)
VERDE = (50, 150, 50)
CINZA = (220, 220, 220)
PRETO = (0, 0, 0)

pergunta = "O que é reciclagem?"

respostas = [
    "Transformar materiais usados em novos produtos",
    "Jogar todos os resíduos no mesmo lugar",
    "Queimar o lixo",
    "Jogar resíduos em rios"
]

resposta_correta = 0  # Índice da resposta correta

botoes = []

for i in range(4):
    botao = pygame.Rect(100, 200 + i * 80, 600, 60)
    botoes.append(botao)


resultado = ""

rodando = True

while rodando:

    # Fundo
    tela.fill(BRANCO)

    # Mostra a pergunta
    texto = fonte_pergunta.render(pergunta, True, PRETO)
    tela.blit(texto, (100, 100))

    # Mostra as respostas
    for i in range(4):

        # Desenha o botão
        pygame.draw.rect(tela, CINZA, botoes[i])

        # Texto da resposta
        texto_resposta = fonte_resposta.render(
            respostas[i],
            True,
            PRETO
        )

        tela.blit(
            texto_resposta,
            (botoes[i].x + 10, botoes[i].y + 18)
        )

    # Mostra resultado
    if resultado != "":
        texto_resultado = fonte_resultado.render(
            resultado,
            True,
            VERDE
        )

        tela.blit(texto_resultado, (100, 540))

    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        # Clique do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:

            posicao_mouse = evento.pos

            # Verifica qual botão foi clicado
            for i in range(4):

                if botoes[i].collidepoint(posicao_mouse):

                    if i == resposta_correta:
                        resultado = "Resposta correta!"
                    else:
                        resultado = "Resposta incorreta!"

    pygame.display.flip()

pygame.quit()
sys.exit()