from genetic import *

class myIndividual(Individual):
    """ ... """

    # Gene:     Codifica um simples parametro
    # Alelos:   Valores que o gene pode assumir
    # Exemplo: Gene represetando cor de um objeto pode ter alelos como azul, preto, amerelo

    # Genes do passive walker, cada posicao contem um range que representa os possiveis 
    # valores do gene(alelos)
    #alleles = [(537,537), (0,400), (10, 200), (10, 200), (1, 60), (0, 2*pi), (0, 2*pi), (0, 2*pi), (0, 2*pi)]
    alleles = [(537,537), (500,500), (50, 50), (50, 50), (45, 45), (pi/4, pi/4), (-2*pi/4, -2*pi/4), (0, 0), (0, 0)]
    length = 9

    """ Passive walker genes                                        alleles values range based in 600x600 resolution
        pos_w -- the initial position           (fixed)             x-position 537 to all chromosomes
        pos_h -- the initial position                               y-position alleles 0 to 400
        ul -- the length of the upper leg                           10 to 200
        ll -- the length of the lower leg                           10 to 200
        w -- the width of the robot                                 1 to 60
        lua -- the angle of the left hip                            0 to 360 degrees
        lla -- the angle of the left ankle                          0 to 360 degrees
        rua -- the angle of the right hip                           0 to 360 degrees
        rla -- the angle of the right ankle                         0 to 360 degrees
    """
    def __init__(self, chromosome=None):
        self.chromosome = chromosome or self._makechromosome()
        self.score = None  # set during evaluation

    def _makechromosome(self):
        return [random.uniform(self.alleles[gene][0], self.alleles[gene][1]) for gene in range(self.length)]

    # sample mutation method
    def _pick(self, gene):
        "chooses a random allele to replace this gene's allele."
        self.chromosome[gene] = random.uniform(self.alleles[gene][0], self.alleles[gene][1])


    def evaluate(self, indiv=0, optimum=None):
        "Evaluate individual fitness score."

        if indiv%10 == 0:                       # apresenta a simulacao grafica a cada 10 individuos no processo de avaliacao
            s = simulation(show=True)
        else:
            s = simulation(show=False)

        sim_time, pos_x, height = s.individual_sim((self.chromosome[0], self.chromosome[1]), self.chromosome[2], self.chromosome[3], self.chromosome[4], self.chromosome[5], self.chromosome[6], self.chromosome[7], self.chromosome[8])



        ## mostrar uma simulacao a cada 10

        ## algoritmo para calcular score


        #dist = sqrt(pos[0]**2 + pos[1]**2)

        #dist = pos[0]
        dist = 0

        score = (600-dist)/6 # 0 - 100

        # score = ke**2 + iterations - dist**3

        self.score = score

        return 0

    def __repr__(self):
        "returns string representation of self"
        chromosome_str = ''
        for gene in range (len(self.chromosome)):
            chromosome_str += ' ' + str(self.chromosome[gene])

        return '<%s chromosome="%s" \nscore=%s>' % \
               (self.__class__.__name__,
                chromosome_str, self.score)

g = Environment(myIndividual, size=200, maxgenerations=200, crossover_rate=0.95, mutation_rate=0.04, optimum=100)
#g.run()




""" 

from genetic import *
from time import sleep

palavra_secreta = 'HELLOWORLD'

class Palavra(Individual):
    global palavra_secreta
    alleles = list(range(ord('A'),ord('Z')+1))
    length = len(palavra_secreta)
    seperator = ''
    optimization = MINIMIZE
    def __init__(self, chromosome=None):
        self.segredo = [ord(letra) for letra in palavra_secreta]
        super(Palavra, self).__init__(chromosome)
    def evaluate(self, generation=0, optimum=None):
        erro = 0
        for x,y in zip(self.segredo, self.chromosome):
            erro += (x-y)**2
        self.score = erro
        sleep(0.01)


from palavra import Palavra
from genetic import Environment

e = Environment(Palavra, None, 100, 100, 0, 0.95, 0.02, optimum=0)
e.run()

"""