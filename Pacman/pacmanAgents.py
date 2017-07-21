# pacmanAgents.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from pacman import Directions
from game import Agent
from searchAgents import PositionSearchProblem
import random
import util

class pacmanAStar(Agent):
  def getAction( self, state ):
    acoes = state.getLegalActions()
    posicaoFantasmas = state.getGhostPositions()
    problema = PositionSearchProblem(state)
    problema.startState = state.getPacmanPosition()
    inicio = problema.getStartState()
    problema.goal = min([(util.manhattanDistance(inicio, comida) + calculoRaio(posicaoFantasmas, comida, state), comida) for comida in state.getFood().asList()])[1]     #Objetivo


    heap = util.PriorityQueue()        
    origemEstado = {}                   #Tabela de origem do estado
    custos = {inicio: 0}                
    custosFinais = {inicio: util.manhattanDistance(inicio, problema.goal)}
    visitados = set()

    heap.push(inicio, custosFinais[inicio])       #Insere o estado inicial na heap

    estadoEscolhido = None

    while not heap.isEmpty():        
      estadoAtual = heap.pop()
      visitados.add(estadoAtual)

      #Se chegarmos ao estado final, recriamos um caminho de estados ate o inicio da busca, tirando o estado inicial
      if problema.isGoalState(estadoAtual):
        caminhoArvore = [estadoAtual]
        
        while estadoAtual in origemEstado.keys():				#Verifica se o estadoAtual nao eh o inicial, senao for continua subindo na arvore
        	estadoAtual = origemEstado[estadoAtual]
        	caminhoArvore.append(estadoAtual)

        estadoEscolhido = caminhoArvore[-2]						#A penultima posicao corresponde ao estado apos o inicial
        break


      for sucessor in problema.getSuccessors(estadoAtual):       #Gerando novos estados
        
        medo = False
        # sucessor[0] eh o elemento 0 da tri-pla retornada por PositionSearchProblem.getSucessors que eh o estado
        if sucessor[0] in posicaoFantasmas:
          for index in xrange(1, state.getNumAgents()):
            if state.getGhostState(index).scaredTimer > 0 and state.getGhostPosition(index) == sucessor[0]:
              medo = True

        if (sucessor[0] in posicaoFantasmas and medo) or sucessor[0] not in posicaoFantasmas:

          if sucessor[0] in visitados:
            continue

          origemEstado[sucessor[0]] = estadoAtual 
          custos[sucessor[0]] = custos[estadoAtual] + sucessor[2]			#Soma custo atual com os anteriores
          custosFinais[sucessor[0]] = custos[sucessor[0]] + util.manhattanDistance(sucessor[0], problema.goal) #Soma custo com a heuristica (f(x) = g(x) + h(x))

          if not heap.contains(sucessor[0]):
            heap.push(sucessor[0], custosFinais[sucessor[0]])
          

    acaoEscolhida = None 				#Ainda nao se sabe a acao que leva ao estado escolhido

    # sucessor[1] eh o elemento 1 da tri-pla retornada por PositionSearchProblem.getSucessors que eh a acao
    #Retorna a melhor acao legal
    for sucessor in problema.getSuccessors(inicio):
      if estadoEscolhido == sucessor[0]:
        if sucessor[1] in acoes:
          acaoEscolhida = sucessor[1]

    if acaoEscolhida == None:
      acaoEscolhida = random.choice(acoes)

    return acaoEscolhida

def calculoRaio(posicaoFantasmas, posicaoComida, state): #Calcula a pontuacao da comida, considerando os fantamas num raio de 4 posicoes
	maxX = state.data.layout.width
	maxY = state.data.layout.height

	print('max X:{}, max Y:{}'.format(maxX, maxY))
	raio = min(int((maxX + maxY)*0.15), 4)
	print('RAIO:{}'.format(raio))
	#Posicoes iniciais
	xO = max(posicaoComida[0] - raio, 0)
	yO = max(posicaoComida[1] - raio, 0)

	#Posicoes limite
	xF = min(posicaoComida[0] + raio + 1, maxX)
	yF = min(posicaoComida[1] + raio + 1, maxY)

	cont = 0.
	for i in range(xO, xF):
		for j in range(yO, yF):
			if (i, j) in posicaoFantasmas and (i != posicaoComida[0] and j != posicaoComida[1]):
				dist = util.manhattanDistance(posicaoComida, (i, j))
				cont = cont + (15 * (1. / dist**2))							#Uma heuristica doida que pune comidas proximas a fantasmas

	return cont

class LeftTurnAgent(Agent):
  "An agent that turns left at every opportunity"
  
  def getAction(self, state):
    legal = state.getLegalPacmanActions()
    current = state.getPacmanState().configuration.direction
    if current == Directions.STOP: current = Directions.NORTH
    left = Directions.LEFT[current]
    if left in legal: return left
    if current in legal: return current
    if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
    if Directions.LEFT[left] in legal: return Directions.LEFT[left]
    return Directions.STOP

class GreedyAgent(Agent):
  def __init__(self, evalFn="scoreEvaluation"):
    self.evaluationFunction = util.lookup(evalFn, globals())
    assert self.evaluationFunction != None
        
  def getAction(self, state):
    # Generate candidate actions
    legal = state.getLegalPacmanActions()
    if Directions.STOP in legal: legal.remove(Directions.STOP)
      
    successors = [(state.generateSuccessor(0, action), action) for action in legal] 
    scored = [(self.evaluationFunction(state), action) for state, action in successors]
    bestScore = max(scored)[0]
    bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
    return random.choice(bestActions)
  
def scoreEvaluation(state):
  return state.getScore()  