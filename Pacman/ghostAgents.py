# ghostAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import Agent
from game import Actions
from game import Directions
from util import manhattanDistance
import util
from searchAgents import PositionSearchProblem
import random


class fantasmaAStar(Agent):

  def __init__( self, index ):
        self.index = index

  def getAction( self, state ):
    acoes     = state.getLegalActions(self.index)
    fantasmas = state.getGhostState(self.index)  
    medo      = fantasmas.scaredTimer > 0       #Diz se o fantasma esta com medo
    problema = PositionSearchProblem(state)     #O problema atual
    problema.startState = state.getGhostPosition(self.index)    #Estado Inicial
    problema.goal = state.getPacmanPosition()     #Objetivo e a posicao do pacman
    inicio = problema.getStartState()         #O inicio e o estado inicial do problema

             
    heap = util.PriorityQueue()
    origemEstado = {}             
    custos = {inicio: 0}          
    custosFinais = {inicio: util.manhattanDistance(inicio, problema.goal)} 
    visitados = set()

    heap.push(inicio, custosFinais[inicio])

    estadoEscolhido = None

    #Busca comeca aqui
    while not heap.isEmpty():         
      estadoAtual = heap.pop()
      visitados.add(estadoAtual)

      if problema.isGoalState(estadoAtual):     #Encontrou o objetivo
        caminhoArvore = [estadoAtual]
        
        while estadoAtual in origemEstado.keys():				#Verifica se o estadoAtual nao eh o inicial, senao for continua subindo na arvore
        	estadoAtual = origemEstado[estadoAtual]
        	caminhoArvore.append(estadoAtual)

        estadoEscolhido = caminhoArvore[-2]						#A penultima posicao corresponde ao estado apos o inicial
        break

      #Gerando sucessores
      for sucessor in problema.getSuccessors(estadoAtual):
        posicaoFantasmas = state.getGhostPositions()
        posicaoFantasmas.remove(state.getGhostPosition(self.index))
        
        if not sucessor[0] in posicaoFantasmas:

          if sucessor[0] in visitados:
            continue

          origemEstado[sucessor[0]] = estadoAtual 
          custos[sucessor[0]] = custos[estadoAtual] + sucessor[2]
          custosFinais[sucessor[0]] = custos[sucessor[0]] + util.manhattanDistance(sucessor[0], problema.goal) #Soma custo com a heuristica (f(x) = g(x) + h(x))

          if not heap.contains(sucessor[0]):
            heap.push(sucessor[0], custosFinais[sucessor[0]])


    acaoEscolhida = None

    #Retorna a melhor acao legal
    for sucessor in problema.getSuccessors(inicio):
      if estadoEscolhido == sucessor[0]:
        if sucessor[1] in acoes:
          acaoEscolhida = sucessor[1]

    #Fantasmas assustados vao pra qualquer direcao.
    if medo and acaoEscolhida != None and len(acoes) > 1:
      acoes.remove(acaoEscolhida)
      acaoEscolhida = random.choice(acoes)
    elif acaoEscolhida == None:
      acaoEscolhida = random.choice(acoes)

    return acaoEscolhida

class GhostAgent( Agent ):
  def __init__( self, index ):
    self.index = index

  def getAction( self, state ):
    dist = self.getDistribution(state)
    if len(dist) == 0: 
      return Directions.STOP
    else:
      return util.chooseFromDistribution( dist )
    
  def getDistribution(self, state):
    "Returns a Counter encoding a distribution over actions from the provided state."
    util.raiseNotDefined()

class RandomGhost( GhostAgent ):
  "A ghost that chooses a legal action uniformly at random."
  def getDistribution( self, state ):
    dist = util.Counter()
    for a in state.getLegalActions( self.index ): dist[a] = 1.0
    dist.normalize()
    return dist

class DirectionalGhost( GhostAgent ):
  "A ghost that prefers to rush Pacman, or flee when scared."
  def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
    self.index = index
    self.prob_attack = prob_attack
    self.prob_scaredFlee = prob_scaredFlee
      
  def getDistribution( self, state ):
    # Read variables from state
    ghostState = state.getGhostState( self.index )
    legalActions = state.getLegalActions( self.index )
    pos = state.getGhostPosition( self.index )
    isScared = ghostState.scaredTimer > 0
    
    speed = 1
    if isScared: speed = 0.5
    
    actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
    newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
    pacmanPosition = state.getPacmanPosition()

    # Select best actions given the state
    distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
    if isScared:
      bestScore = max( distancesToPacman )
      bestProb = self.prob_scaredFlee
    else:
      bestScore = min( distancesToPacman )
      bestProb = self.prob_attack
    bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]
    
    # Construct distribution
    dist = util.Counter()
    for a in bestActions: dist[a] = bestProb / len(bestActions)
    for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
    dist.normalize()
    return dist
