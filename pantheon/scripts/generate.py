import random
import name
from numpy.random import choice as npchoice
from process import *

# noun_tokens = {}
# verb_tokens = {}
#
# female_names = []
# male_names = []
# nb_names = []

male = 'M'
female = 'F'
non_binary = 'NB'

# def load_texts():
#     texts = get_texts()
#     global noun_tokens
#     global verb_tokens
#     noun_tokens = get_tokens(texts, ['NNS'])
#     verb_tokens = get_tokens(texts, ['VBG'])
#
# def load_names(ethnicity):
#     names = name.load_names(ethnicity)
#     random.shuffle(names)
#     global female_names
#     global male_names
#     global andro_names
#     female_names = [name for name,gender,*desc in names if gender == 'girl']
#     male_names = [name for name,gender,*desc in names if gender == 'boy']
#     andro_names = [name for name,gender,*desc in names if gender == 'boygirl'] + male_names

# texts = get_texts()
# noun_tokens = get_tokens(texts, ['NNS'])
# verb_tokens = get_tokens(texts, ['VBG'])
#
# names = name.load_names('germanic')
# random.shuffle(names)
# female_names = [name for name,gender,*desc in names if gender == 'girl']
# male_names = [name for name,gender,*desc in names if gender == 'boy']
# andro_names = [name for name,gender,*desc in names if gender == 'boygirl'] + male_names

class Pantheon:
    def __init__(self, mother_of_creation, father_of_creation):
        self.mother_of_creation = mother_of_creation
        self.father_of_creation = father_of_creation
        self.gods = [mother_of_creation, father_of_creation]


    def spawn(self, generations):
        egg_donors = [god for god in self.gods if god.chromosomes == 'XX']
        sperm_donors = [god for god in self.gods if god.chromosomes == 'XY']

        for i in range(generations):
            print("\nGENERATION %d\n" % (i+1))

            for egg_donor in egg_donors:
                sperm_donor = random.choice(sperm_donors)
                offspring = self.fertilize(egg_donor, sperm_donor)
                send_birth_announcement(egg_donor, sperm_donor, offspring)
                offspring.parents = [egg_donor, sperm_donor]

                # offspring joins pantheon
                self.gods.append(offspring)
                if offspring.chromosomes == 'XX':
                    egg_donors.append(offspring)
                else:
                    sperm_donors.append(offspring)


    def fertilize(self, egg_donor, sperm_donor):
        egg_word = egg_donor.get_gamete()
        sperm_word = sperm_donor.get_gamete()
        offspring = God(egg_word, sperm_word)
        return offspring


class God:
    def __init__(self, egg_word, sperm_word):
        self.chromosomes = random.choice(['XX','XY'])
        self.gender = get_gender(self.chromosomes)
        self.parents = []

        # 'mother' and 'father' in the sense of egg/sperm donor, not the roles 'mommy' and 'daddy'
        self.genes_from_mother = self.get_egg(egg_word)
        self.genes_from_father = self.get_sperm(sperm_word)
        self.genome = self.genes_from_mother + self.genes_from_father

        self.name = self.get_name()
        self.epithet = self.get_epithet()


    def get_egg(self, egg_word):
        probabilities = [0.9,0.1]
        gene_pool = npchoice([noun_tokens, verb_tokens], 1, p=probabilities)[0]

        phenotype = get_overlapping_matches(egg_word, gene_pool, 23)
        genotype = [gene for gene,expression in phenotype]
        return genotype


    def get_sperm(self, sperm_word):
        probabilities = [0.9,0.1]
        gene_pool = npchoice([noun_tokens, verb_tokens], 1, p=probabilities)[0]

        phenotype = get_overlapping_matches(sperm_word, gene_pool, 23)
        genotype = [gene for gene,expression in phenotype]
        return genotype


    def get_name(self):
        if self.gender == female:
            return female_names.pop()
        elif self.gender == male:
            return male_names.pop()
        else:
            return andro_names.pop()


    def get_epithet(self):
        if self.gender == female:
            title = 'Godess'
        elif self.gender == male:
            title = 'God'
        else:
            title = 'God'

        domains = random.sample(self.genome, 3)
        return '%s of %s, %s, and %s' % (title, *domains)


    def change_epithet(self):
        self.epithet = self.get_epithet()
        print(self.epithet)


    def get_gamete(self):
        return random.choice(self.genome)


"""Miscellaneous helpers"""

def send_birth_announcement(parent_a, parent_b, offspring=None):
    if offspring.gender == male:
        child = 'son'
    elif offspring.gender == female:
        child = 'daughter'
    else:
        child = 'child'

    #print ("%s, %s - %s of %s and %s" % (offspring.name, offspring.epithet, child, parent_a.name, parent_b.name))
    print("%s - %s" % (offspring.name, offspring.epithet))

def get_gender(chromosomes):
    genders = [male, female, non_binary]
    probabilities = [0.8, 0.1, 0.1] if chromosomes == 'XY' else [0.1, 0.8, 0.1]
    return npchoice(genders, 1, p=probabilities)[0]