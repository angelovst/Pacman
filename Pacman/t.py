'''
0 0 F 0
0 F 0 0
0 0 1 0
0 0 0 F

'''
def calculoRaio(posicaoFantasmas, posicaoComida): #Calcula a pontuacao da comida, considerando os fantamas num raio de 4 posicoes
	maxX = 4
	maxY = 4
	#print('Max X: {}, Max Y:{}'.format(maxX, maxY))

	raio = 2

	xO = max(posicaoComida[0] - raio, 0)
	yO = max(posicaoComida[1] - raio, 0)

	xF = min(posicaoComida[0] + raio + 1, maxX)
	yF = min(posicaoComida[0] + raio + 1, maxY)

	cont = 0
	for i in range(xO, xF):
		for j in range(yO, yF):
			print(i, j)
			if (i, j) in posicaoFantasmas:
				cont = cont + 1

	return cont


posicaoFantasmas = [(0, 2), (1, 1), (3, 3)]
posicaoComida = (2, 2)
t = calculoRaio(posicaoFantasmas, posicaoComida)
print(t)
