import pygame
import os
import random

telaLargura = 500
telaAltura = 800

imagemCano = pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'pipe.png')))
imagemChao = pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'base.png')))
imagemBackGround = pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bg.png')))
imagensPassaro = [pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bird1.png'))),
                 pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bird2.png'))), 
                 pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bird3.png')))]

pygame.font.init()
fontePontos = pygame.font.SysFont('arial', 50)


class Passaro:
    imagens = imagensPassaro
    # animações da movimentação do pássaro.
    rotacaoMaxima = 25
    velocidadeRotacao = 10
    tempoAnimacao = 20

    # atributos do pássaro.
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagemImagem = 0
        self.imagem = self.imagens[0]

    def pular(self):
        self.velocidade = -10
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 0.7
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # angulo do passaro 
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacaoMaxima:
                self.angulo = self.rotacaoMaxima
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidadeRotacao
        
    def desenhar(self, tela):
        # definir os movimentos de batidade de asa

        self.contagemImagem += 1

        if self.contagemImagem < self.tempoAnimacao:
            self.imagem = self.imagens[0]
        elif self.contagemImagem < self.tempoAnimacao*2:
            self.imagem = self.imagens[1]
        elif self.contagemImagem < self.tempoAnimacao*3:
            self.imagem = self.imagens[2]
        elif self.contagemImagem < self.tempoAnimacao*4:
            self.imagem = self.imagens[1]
        elif self.contagemImagem >= self.tempoAnimacao*4 + 1:
            self.imagem = self.imagens[0]
            self.contagemImagem = 0

        # se o passaro tiver caindo
        if self.angulo <= -70:
            self.imagem = self.imagens[1]
            self.contagemImagem = self.tempoAnimacao * 2
    
        # desenhar a imagem
        imagemRotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        posicaoCentroImagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        localDeDesenhoRotacionado = imagemRotacionada.get_rect(center=posicaoCentroImagem)
        tela.blit(imagemRotacionada, localDeDesenhoRotacionado.topleft)

    # pegando a máscara correta do pássaro.
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

    
class Cano:
    distanciaEntreCanos = 240
    velocidadeMovimCanos = 4

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posicaoTopo = 0
        self.posicaoBase = 0
        self.imagemCanoTopo = pygame.transform.flip(imagemCano, False, True)
        self.imagemCanoBase = imagemCano
        self.canoPassou = False
        self.definirAltura()

    def definirAltura(self):
        self.altura = random.randrange(50, 450)
        self.posicaoTopo = self.altura - self.imagemCanoTopo.get_height()
        self.posicaoBase = self.altura + self.distanciaEntreCanos
        
    def mover(self):
        self.x -= self.velocidadeMovimCanos
        
    def desenhar(self, tela):
        tela.blit(self.imagemCanoTopo, (self.x, self.posicaoTopo))
        tela.blit(self.imagemCanoBase, (self.x, self.posicaoBase))

    def colisao(self, passaro):
        passaroMask = passaro.get_mask()
        topoMask = pygame.mask.from_surface(self.imagemCanoTopo)
        baseMask = pygame.mask.from_surface(self.imagemCanoBase)

        distanciaTopo = (self.x - passaro.x, self.posicaoTopo - round(passaro.y))
        distanciaBase = (self.x - passaro.x, self.posicaoBase - round(passaro.y))

        topoPonto = passaroMask.overlap(topoMask, distanciaTopo)
        basePonto = passaroMask.overlap(baseMask, distanciaBase)

        if basePonto or topoPonto:
            return True
        else:
            return False
            
class Chao:
    velocidadeChao = 5
    larguraChao =  imagemChao.get_width()
    imagem = imagemChao

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.larguraChao

    def mover(self):
        self.x0 -= self.velocidadeChao
        self.x1 -= self.velocidadeChao

        if self.x0 + self.larguraChao < 0:
            self.x0 = self.x1 + self.larguraChao
        if self.x1 + self.larguraChao < 0:
            self.x1 = self.x0 + self.larguraChao
        
    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x0, self.y))
        tela.blit(self.imagem, (self.x1, self.y))

def desenharTela(tela, passaros, canos, chao, pontos):
    tela.blit(imagemBackGround, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = fontePontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (telaLargura - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((telaLargura, telaAltura))
    pontos = 0
    relogio = pygame.time.Clock()


    rodando = True
    while rodando:
        relogio.tick(31)  # FPS do jogo

        # interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
        
        # mover as coisas
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionarCano = False
        removerCanos = []

        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colisao(passaro):
                    passaros.pop(i)
                if not cano.canoPassou and passaro.x > cano.x:
                    cano.canoPassou = True
                    adicionarCano = True
            cano.mover()
            if cano.x + cano.imagemCanoTopo.get_width() < 0:
                removerCanos.append(cano)
        
        if adicionarCano:
            pontos += 1
            canos.append(Cano(600))
        for cano in removerCanos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)


        desenharTela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':
    main()
