import pygame
import sys

pygame.init()

# ==================================================
# CONFIGURAÇÕES DA TELA
# ==================================================

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Quiz Verde")

relogio = pygame.time.Clock()

# ==================================================
# FONTES
# ==================================================

fonte_titulo = pygame.font.Font(None, 70)
fonte_pergunta = pygame.font.Font(None, 40)
fonte_resposta = pygame.font.Font(None, 30)
fonte_pequena = pygame.font.Font(None, 28)
fonte_resultado = pygame.font.Font(None, 45)
fonte_botao = pygame.font.Font(None, 35)

# ==================================================
# CORES
# ==================================================

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

VERDE = (144, 238, 144)
VERDE_ESCURO = (46, 139, 87)
VERDE_MUITO_ESCURO = (30, 90, 55)

VERMELHO = (200, 50, 50)
AMARELO = (255, 215, 0)

# ==================================================
# FUNÇÃO DO FUNDO DEGRADÊ
# ==================================================

def desenhar_degrade():

    cor_cima = (15, 70, 40)
    cor_baixo = (120, 200, 140)

    for y in range(ALTURA):

        proporcao = y / ALTURA

        r = int(
            cor_cima[0]
            + (cor_baixo[0] - cor_cima[0]) * proporcao
        )

        g = int(
            cor_cima[1]
            + (cor_baixo[1] - cor_cima[1]) * proporcao
        )

        b = int(
            cor_cima[2]
            + (cor_baixo[2] - cor_cima[2]) * proporcao
        )

        pygame.draw.line(
            tela,
            (r, g, b),
            (0, y),
            (LARGURA, y)
        )

# ==================================================
# FUNÇÃO PARA QUEBRAR TEXTOS AUTOMATICAMENTE
# ==================================================

def quebrar_texto(texto, fonte, largura_maxima):

    palavras = texto.split()

    linhas = []

    linha_atual = ""

    for palavra in palavras:

        teste = linha_atual + " " + palavra

        if fonte.size(teste)[0] <= largura_maxima:

            linha_atual = teste.strip()

        else:

            if linha_atual:
                linhas.append(linha_atual)

            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    return linhas

# ==================================================
# PERGUNTAS
# ==================================================

perguntas = [
    "Qual é um dos principais objetivos da reciclagem?",
    "Por que a reciclagem ajuda a preservar recursos naturais?",
    "Qual destes materiais possui maior potencial de reciclagem?",
    "Qual atitude contribui mais para a reciclagem?",
    "Quais são os principais benefícios da reciclagem?",
    "Quais problemas podem ocorrer com o descarte inadequado?"
]

# ==================================================
# RESPOSTAS
# ==================================================

respostas = [

    [
        "Aumentar a quantidade de lixo produzido",
        "Transformar resíduos em novos produtos",
        "Eliminar completamente todos os resíduos",
        "Evitar o uso de qualquer tipo de material"
    ],

    [
        "Porque reduz a necessidade de retirar novas matérias-primas da natureza",
        "Porque impede qualquer tipo de poluição",
        "Porque transforma resíduos em alimentos",
        "Porque elimina a necessidade de energia"
    ],

    [
        "Papel",
        "Plástico",
        "Vidro",
        "Todos os materiais possuem o mesmo potencial"
    ],

    [
        "Misturar todos os resíduos no lixo comum",
        "Separar corretamente os materiais recicláveis",
        "Queimar materiais recicláveis",
        "Descartar resíduos em terrenos vazios"
    ],

    [
        "Redução da poluição e economia de recursos naturais",
        "Aumento da quantidade de resíduos nos aterros",
        "Maior consumo de matérias-primas",
        "Aumento da poluição dos rios"
    ],

    [
        "Poluição do solo, da água e do ar",
        "Apenas mudanças na aparência das cidades",
        "Somente aumento da quantidade de lixo",
        "Nenhum impacto significativo"
    ]
]

# ==================================================
# RESPOSTAS CORRETAS
# ==================================================

respostas_corretas = [1, 0, 3, 1, 0, 0]

# ==================================================
# VARIÁVEIS DO JOGO
# ==================================================

estado = "menu"

pergunta_atual = 0

pontos = 0

vidas = 3

resultado = ""

tempo_por_pergunta = 15

tempo_restante = tempo_por_pergunta

tempo_inicio = pygame.time.get_ticks()

# ==================================================
# FUNÇÃO PARA DESENHAR BOTÕES
# ==================================================

def desenhar_botao(texto, retangulo, cor):

    pygame.draw.rect(
        tela,
        cor,
        retangulo,
        border_radius=10
    )

    texto_renderizado = fonte_botao.render(
        texto,
        True,
        BRANCO
    )

    x = (
        retangulo.centerx
        - texto_renderizado.get_width() // 2
    )

    y = (
        retangulo.centery
        - texto_renderizado.get_height() // 2
    )

    tela.blit(
        texto_renderizado,
        (x, y)
    )

# ==================================================
# BOTÕES DO MENU
# ==================================================

botao_jogar = pygame.Rect(
    250,
    300,
    300,
    70
)

botao_sair = pygame.Rect(
    250,
    400,
    300,
    70
)

# ==================================================
# BOTÕES DA TELA FINAL
# ==================================================

botao_jogar_novamente = pygame.Rect(
    200,
    400,
    400,
    70
)

botao_sair_final = pygame.Rect(
    250,
    490,
    300,
    60
)

# ==================================================
# BOTÕES DAS RESPOSTAS
# ==================================================

botoes = []

for i in range(4):

    botao = pygame.Rect(
        100,
        190 + i * 80,
        600,
        60
    )

    botoes.append(botao)

# ==================================================
# INICIAR / REINICIAR O QUIZ
# ==================================================

def iniciar_quiz():

    global estado
    global pergunta_atual
    global pontos
    global vidas
    global resultado
    global tempo_restante
    global tempo_inicio

    estado = "quiz"

    pergunta_atual = 0

    pontos = 0

    vidas = 3

    resultado = ""

    tempo_restante = tempo_por_pergunta

    tempo_inicio = pygame.time.get_ticks()

# ==================================================
# DESENHAR MENU
# ==================================================

def desenhar_menu():

    desenhar_degrade()

    titulo = fonte_titulo.render(
        "QUIZ VERDE",
        True,
        BRANCO
    )

    tela.blit(
        titulo,
        (
            LARGURA // 2
            - titulo.get_width() // 2,
            100
        )
    )

    subtitulo = fonte_pequena.render(
        "Teste seus conhecimentos sobre o meio ambiente!",
        True,
        BRANCO
    )

    tela.blit(
        subtitulo,
        (
            LARGURA // 2
            - subtitulo.get_width() // 2,
            190
        )
    )

    desenhar_botao(
        "JOGAR",
        botao_jogar,
        VERDE_ESCURO
    )

    desenhar_botao(
        "SAIR",
        botao_sair,
        VERDE_MUITO_ESCURO
    )

# ==================================================
# DESENHAR QUIZ
# ==================================================

def desenhar_quiz():

    desenhar_degrade()

    # ------------------------------
    # Pontos
    # ------------------------------

    texto_pontos = fonte_pequena.render(
        f"Pontos: {pontos}",
        True,
        BRANCO
    )

    tela.blit(
        texto_pontos,
        (20, 20)
    )

    # ------------------------------
    # Vidas
    # ------------------------------

    texto_vidas = fonte_pequena.render(
        f"Vidas: {vidas}",
        True,
        BRANCO
    )

    tela.blit(
        texto_vidas,
        (680, 20)
    )

    # ------------------------------
    # Pergunta atual
    # ------------------------------

    texto_progresso = fonte_pequena.render(
        f"Pergunta {pergunta_atual + 1}/{len(perguntas)}",
        True,
        BRANCO
    )

    tela.blit(
        texto_progresso,
        (
            LARGURA // 2
            - texto_progresso.get_width() // 2,
            20
        )
    )

    # ------------------------------
    # Tempo
    # ------------------------------

    cor_tempo = BRANCO

    if tempo_restante <= 5:
        cor_tempo = VERMELHO

    texto_tempo = fonte_pequena.render(
        f"Tempo: {tempo_restante}",
        True,
        cor_tempo
    )

    tela.blit(
        texto_tempo,
        (20, 55)
    )

    # ------------------------------
    # Barra de tempo
    # ------------------------------

    pygame.draw.rect(
        tela,
        PRETO,
        (200, 55, 400, 15),
        border_radius=5
    )

    largura_barra = int(
        400
        * tempo_restante
        / tempo_por_pergunta
    )

    if largura_barra < 0:
        largura_barra = 0

    pygame.draw.rect(
        tela,
        VERDE,
        (200, 55, largura_barra, 15),
        border_radius=5
    )

    # ------------------------------
    # Pergunta
    # ------------------------------

    linhas_pergunta = quebrar_texto(
        perguntas[pergunta_atual],
        fonte_pergunta,
        700
    )

    y_pergunta = 90

    for linha in linhas_pergunta:

        texto = fonte_pergunta.render(
            linha,
            True,
            BRANCO
        )

        tela.blit(
            texto,
            (
                LARGURA // 2
                - texto.get_width() // 2,
                y_pergunta
            )
        )

        y_pergunta += 40

    # ------------------------------
    # Respostas
    # ------------------------------

    for i in range(4):

        pygame.draw.rect(
            tela,
            VERDE_ESCURO,
            botoes[i],
            border_radius=10
        )

        linhas_resposta = quebrar_texto(
            respostas[pergunta_atual][i],
            fonte_resposta,
            550
        )

        altura_total = len(linhas_resposta) * 28

        y_texto = (
            botoes[i].centery
            - altura_total // 2
        )

        for linha in linhas_resposta:

            texto_resposta = fonte_resposta.render(
                linha,
                True,
                BRANCO
            )

            tela.blit(
                texto_resposta,
                (
                    botoes[i].centerx
                    - texto_resposta.get_width() // 2,
                    y_texto
                )
            )

            y_texto += 28

    # ------------------------------
    # Resultado
    # ------------------------------

    if resultado != "":

        if resultado == "Resposta correta!":
            cor_resultado = VERDE

        elif resultado == "Resposta incorreta!":
            cor_resultado = VERMELHO

        else:
            cor_resultado = AMARELO

        texto_resultado = fonte_pequena.render(
            resultado,
            True,
            cor_resultado
        )

        tela.blit(
            texto_resultado,
            (
                LARGURA // 2
                - texto_resultado.get_width() // 2,
                550
            )
        )

# ==================================================
# DESENHAR RESULTADO FINAL
# ==================================================

def desenhar_resultado_final():

    desenhar_degrade()

    titulo = fonte_titulo.render(
        "QUIZ CONCLUÍDO!",
        True,
        BRANCO
    )

    tela.blit(
        titulo,
        (
            LARGURA // 2
            - titulo.get_width() // 2,
            70
        )
    )

    texto_pontos = fonte_resultado.render(
        f"Pontuação: {pontos}",
        True,
        BRANCO
    )

    tela.blit(
        texto_pontos,
        (
            LARGURA // 2
            - texto_pontos.get_width() // 2,
            180
        )
    )

    texto_acertos = fonte_resultado.render(
        f"Você acertou {pontos} de {len(perguntas)}!",
        True,
        BRANCO
    )

    tela.blit(
        texto_acertos,
        (
            LARGURA // 2
            - texto_acertos.get_width() // 2,
            240
        )
    )

    # ------------------------------
    # Mensagem
    # ------------------------------

    porcentagem = (
        pontos / len(perguntas)
    ) * 100

    if porcentagem == 100:

        mensagem = "Excelente! Você acertou tudo!"

    elif porcentagem >= 70:

        mensagem = (
            "Muito bom! Você conhece bastante "
            "sobre o meio ambiente!"
        )

    elif porcentagem >= 50:

        mensagem = (
            "Bom trabalho! Continue aprendendo!"
        )

    else:

        mensagem = (
            "Você pode tentar novamente e melhorar!"
        )

    linhas_mensagem = quebrar_texto(
        mensagem,
        fonte_pequena,
        650
    )

    y_mensagem = 310

    for linha in linhas_mensagem:

        texto_mensagem = fonte_pequena.render(
            linha,
            True,
            VERDE
        )

        tela.blit(
            texto_mensagem,
            (
                LARGURA // 2
                - texto_mensagem.get_width() // 2,
                y_mensagem
            )
        )

        y_mensagem += 30

    # ------------------------------
    # Botões
    # ------------------------------

    desenhar_botao(
        "JOGAR NOVAMENTE",
        botao_jogar_novamente,
        VERDE_ESCURO
    )

    desenhar_botao(
        "SAIR",
        botao_sair_final,
        VERDE_MUITO_ESCURO
    )

# ==================================================
# LOOP PRINCIPAL
# ==================================================

rodando = True

while rodando:

    # ==================================================
    # DESENHA A TELA
    # ==================================================

    if estado == "menu":

        desenhar_menu()

    elif estado == "quiz":

        # ------------------------------
        # Atualiza o tempo
        # ------------------------------

        tempo_atual = pygame.time.get_ticks()

        segundos_passados = (
            tempo_atual - tempo_inicio
        ) // 1000

        tempo_restante = (
            tempo_por_pergunta
            - segundos_passados
        )

        # ------------------------------
        # Tempo acabou
        # ------------------------------

        if tempo_restante <= 0:

            tempo_restante = 0

            resultado = "Tempo esgotado!"

            vidas -= 1

            desenhar_quiz()

            pygame.display.flip()

            pygame.time.delay(1000)

            if vidas <= 0:

                estado = "final"

            elif pergunta_atual < len(perguntas) - 1:

                pergunta_atual += 1

                resultado = ""

                tempo_inicio = pygame.time.get_ticks()

            else:

                estado = "final"

        desenhar_quiz()

    elif estado == "final":

        desenhar_resultado_final()

    # ==================================================
    # EVENTOS
    # ==================================================

    for evento in pygame.event.get():

        # ------------------------------
        # Fechar o jogo
        # ------------------------------

        if evento.type == pygame.QUIT:

            rodando = False

        # ------------------------------
        # Clique
        # ------------------------------

        if evento.type == pygame.MOUSEBUTTONDOWN:

            posicao_mouse = evento.pos

            # ==========================================
            # MENU
            # ==========================================

            if estado == "menu":

                if botao_jogar.collidepoint(
                    posicao_mouse
                ):

                    iniciar_quiz()

                elif botao_sair.collidepoint(
                    posicao_mouse
                ):

                    rodando = False

            # ==========================================
            # QUIZ
            # ==========================================

            elif estado == "quiz":

                for i in range(4):

                    if botoes[i].collidepoint(
                        posicao_mouse
                    ):

                        # ------------------------------
                        # Resposta correta
                        # ------------------------------

                        if i == respostas_corretas[
                            pergunta_atual
                        ]:

                            resultado = (
                                "Resposta correta!"
                            )

                            pontos += 1

                        # ------------------------------
                        # Resposta incorreta
                        # ------------------------------

                        else:

                            resultado = (
                                "Resposta incorreta!"
                            )

                            vidas -= 1

                        desenhar_quiz()

                        pygame.display.flip()

                        pygame.time.delay(1000)

                        # ------------------------------
                        # Acabaram as vidas
                        # ------------------------------

                        if vidas <= 0:

                            estado = "final"

                        # ------------------------------
                        # Próxima pergunta
                        # ------------------------------

                        elif pergunta_atual < len(perguntas) - 1:

                            pergunta_atual += 1

                            resultado = ""

                            tempo_inicio = (
                                pygame.time.get_ticks()
                            )

                        # ------------------------------
                        # Terminou o quiz
                        # ------------------------------

                        else:

                            estado = "final"

            # ==========================================
            # RESULTADO FINAL
            # ==========================================

            elif estado == "final":

                if botao_jogar_novamente.collidepoint(
                    posicao_mouse
                ):

                    iniciar_quiz()

                elif botao_sair_final.collidepoint(
                    posicao_mouse
                ):

                    rodando = False

    # ==================================================
    # ATUALIZA A TELA
    # ==================================================

    pygame.display.flip()

    relogio.tick(60)

# ==================================================
# FINALIZA
# ==================================================

pygame.quit()
sys.exit()
