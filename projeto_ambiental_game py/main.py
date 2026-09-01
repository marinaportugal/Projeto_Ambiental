import pygame,sys
import game
pygame.init()

W,H=800,600
tela=pygame.display.set_mode((W,H))
pygame.display.set_caption("Quiz Verde")
clock=pygame.time.Clock()

BRANCO=(255,255,255); VERDE=(144,238,144)
ESCURO=(0,100,0); ESCURO2=(0,50,0); VERMELHO=(255,0,0)
f1=pygame.font.Font(None,70); f2=pygame.font.Font(None,40)
f3=pygame.font.Font(None,30); f4=pygame.font.Font(None,28); f5=pygame.font.Font(None,45)

perguntas=[
"Qual é um dos principais objetivos da reciclagem?",
"Por que a reciclagem ajuda a preservar recursos naturais?",
"Qual destes materiais possui maior potencial de reciclagem?",
"Qual atitude contribui mais para a reciclagem?",
"Quais são os principais benefícios da reciclagem?",
"Quais problemas podem ocorrer com o descarte inadequado?"
]

respostas=[
["Aumentar a quantidade de lixo produzido","Transformar resíduos em novos produtos","Eliminar completamente todos os resíduos","Evitar o uso de qualquer tipo de material"],
["Porque reduz a necessidade de retirar novas matérias-primas da natureza","Porque impede qualquer tipo de poluição","Porque transforma resíduos em alimentos","Porque elimina a necessidade de energia"],
["Papel","Plástico","Vidro","Todos os materiais possuem o mesmo potencial"],
["Misturar todos os resíduos no lixo comum","Separar corretamente os materiais recicláveis","Queimar materiais recicláveis","Descartar resíduos em terrenos vazios"],
["Redução da poluição e economia de recursos naturais","Aumento da quantidade de resíduos nos aterros","Maior consumo de matérias-primas","Aumento da poluição dos rios"],
["Poluição do solo, da água e do ar","Apenas mudanças na aparência das cidades","Somente aumento da quantidade de lixo","Nenhum impacto significativo"]
]

corretas=[1,0,3,1,0,0]
botoes=[pygame.Rect(100,190+i*80,600,60) for i in range(4)]

estado=0; q=pontos=0; vidas=3; resultado=""; TEMPO=15
inicio=pygame.time.get_ticks()


def degrade():
    for y in range(H):
        t=y/H
        cor=(int(15+35*t),int(70+80*t),int(40+45*t))
        pygame.draw.line(tela,cor,(0,y),(W,y))


def texto(txt,f,y,cor=BRANCO):
    img=f.render(txt,True,cor)
    tela.blit(img,(W//2-img.get_width()//2,y))


def quebrar(txt,f,w):
    ls=[]; atual=""
    for p in txt.split():
        t=(atual+" "+p).strip()
        if f.size(t)[0]<=w: atual=t
        else: ls.append(atual); atual=p
    if atual: ls.append(atual)
    return ls


def botao(txt,r,cor=ESCURO):
    pygame.draw.rect(tela,cor,r,border_radius=10)
    texto(txt,f2,r.centery-f2.get_height()//2)
    


def iniciar():
    global estado,q,pontos,vidas,resultado,inicio
    estado,q,pontos,vidas,resultado=1,0,0,3,""
    inicio=pygame.time.get_ticks()


def proxima():
    global q,estado,resultado,inicio
    if q<len(perguntas)-1:
        q+=1; resultado=""; inicio=pygame.time.get_ticks()
    else: estado=2


def menu():
    texto("QUIZ VERDE",f1,100)
    texto("Teste seus conhecimentos sobre o meio ambiente!",f4,190)
    botao("PLAY GAME",pygame.Rect(250,250,300,70))
    botao("JOGAR",pygame.Rect(250,350,300,70))
    botao("SAIR",pygame.Rect(250,450,300,70),ESCURO2)


def quiz():
    tela.blit(f4.render(f"Pontos: {pontos}",True,BRANCO),(20,20))
    tela.blit(f4.render(f"Vidas: {vidas}",True,BRANCO),(680,20))

    tempo=max(0,TEMPO-(pygame.time.get_ticks()-inicio)//1000)
    tela.blit(f4.render(f"Tempo: {tempo}",True,
        VERMELHO if tempo<=5 else BRANCO),(20,55))

    pygame.draw.rect(tela,BRANCO,(200,55,400,15),border_radius=5)
    pygame.draw.rect(tela,ESCURO,(200,55,400*tempo//TEMPO,15),border_radius=5)

    for i,l in enumerate(quebrar(perguntas[q],f2,700)):
        texto(l,f2,90+i*40)

    for i,r in enumerate(botoes):
        pygame.draw.rect(tela,ESCURO,r,border_radius=10)
        ls=quebrar(respostas[q][i],f3,550)
        for j,l in enumerate(ls):
            texto(l,f3,r.centery-len(ls)*28//2+j*28)

    if resultado:
        texto(resultado,f4,550,
              VERDE if "correta" in resultado else VERMELHO)


def final():
    texto("QUIZ CONCLUÍDO!",f1,70)
    texto(f"Pontuação: {pontos}",f5,180)
    texto(f"Você acertou {pontos} de {len(perguntas)}!",f5,240)

    p=pontos/len(perguntas)*100
    msg=("Excelente! Você acertou tudo!" if p==100 else
         "Muito bom! Você conhece bastante sobre o meio ambiente!" if p>=70 else
         "Bom trabalho! Continue aprendendo!" if p>=50 else
         "Você pode tentar novamente e melhorar!")

    for i,l in enumerate(quebrar(msg,f4,650)):
        texto(l,f4,310+i*30,VERDE)

    botao("JOGAR NOVAMENTE",pygame.Rect(200,400,400,70))
    botao("SAIR",pygame.Rect(250,490,300,60),ESCURO2)


rodando=True
while rodando:
    degrade()
    [menu,quiz,final][estado]()

    for e in pygame.event.get():
        if e.type==pygame.QUIT: rodando=False

        elif e.type==pygame.MOUSEBUTTONDOWN:
            pos=e.pos

            if estado==0:
                if pygame.Rect(250,250,300,70).collidepoint(pos):
                    game.game()
                elif pygame.Rect(250,350,300,70).collidepoint(pos):
                    iniciar()
                elif pygame.Rect(250,450,300,70).collidepoint(pos):
                    rodando=False

            elif estado==1:
                for i,r in enumerate(botoes):
                    if r.collidepoint(pos):
                        if i==corretas[q]:
                            resultado="Resposta correta!"; pontos+=1
                        else:
                            resultado="Resposta incorreta!"; vidas-=1
                        quiz(); pygame.display.flip(); pygame.time.delay(700)
                        if vidas<=0: estado=2
                        else: proxima()
                        break

            else:
                if pygame.Rect(200,400,400,70).collidepoint(pos): iniciar()
                elif pygame.Rect(250,490,300,60).collidepoint(pos): rodando=False

    if estado==1 and max(0,TEMPO-(pygame.time.get_ticks()-inicio)//1000)==0:
        resultado="Tempo esgotado!"; vidas-=1
        quiz(); pygame.display.flip(); pygame.time.delay(700)
        if vidas<=0: estado=2
        else: proxima()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
