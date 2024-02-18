import random


class Product:
    def __init__(self, name, characteristics, cost):
        self.name = name
        self.characteristics = characteristics
        self.cost = cost


class Chromosome:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0


def genetic_algorithm(products, target_characteristics, population_size=10000, num_generations=5, mutation_rate=0.1):
    population = generate_population(population_size, len(products))
    count_fitness(population, products, target_characteristics)
    current_generation = 0
    while len(population) > 1 and num_generations > current_generation:
        best_of_population = best_half_of_population(population)
        population = crossover(best_of_population, mutation_rate)
        count_fitness(population, products, target_characteristics)
        current_generation += 1

    for chromosome in population[:]:
        print(chromosome.fitness, chromosome.genes)
        if chromosome.fitness == -1:
            population.remove(chromosome)
    if len(population) == 0:
        return "Генетический алгоритм сработал безуспешно"
    print(population)
    return sorted(population, key=lambda x: (x.fitness, get_chromosome_cost(x, products)))[0]


def get_chromosome_cost(chromosome, products):
    sum = 0
    for i in range(len(chromosome.genes)):
        sum += products[i].cost if chromosome.genes[i] == 1 else 0
    return sum


def generate_population(population_size, len_products):
    return [Chromosome(generate_chromosome_genes(len_products)) for _ in range(population_size)]


def generate_chromosome_genes(len_products):
    return [random.randint(0, 1) for _ in range(len_products)]


# Подсчет приспособленности для хромосом в популяции
# То есть функция приспособленности
def count_fitness(population, products, target_characteristics):
    length = len(population)
    for i in range(length):
        genes_sum = [0 for _ in target_characteristics]
        for j in range(len(population[i].genes)):
            if population[i].genes[j] == 1:
                for m in range(len(products[j].characteristics)):
                    genes_sum[m] += products[j].characteristics[m]
        for j in range(len(genes_sum)):
            if genes_sum[j] < target_characteristics[j]:
                population[i].fitness = -1
                break
            population[i].fitness += (genes_sum[j] - target_characteristics[j]) ** 2


# Ранговый метод
def best_half_of_population(population):
    return sorted(population, key=lambda x: x.fitness)[:len(population)//2]


def crossover(population, mutation_rate):
    child_population = list()
    for i in range(len(population) - 1):
        child = get_child(population[i], population[i+1])
        # Мутация потомства
        if random.random() < mutation_rate:
            mutation_gene = random.randint(0, len(child.genes) - 1)
            child.genes[mutation_gene] = 1 if child.genes[mutation_gene] == 0 else 0
        child_population.append(child)
        i += 2
    return child_population


def get_child(first_parent, second_parend):
    crossover_point = random.randint(1, len(first_parent.genes))
    # Создадим потомка, объединив части генов от обоих родителей
    return Chromosome(first_parent.genes[:crossover_point] + second_parend.genes[crossover_point:])



products = [
    Product("Продукт1", [1000, 10, 8, 12], 10),
    Product("Продукт2", [1000, 12, 12, 9], 15),
    Product("Продукт3", [1000, 10, 8, 12], 9)
    # Добавьте больше продуктов при необходимости
]


target_characteristics = [2000, 20, 20, 20]  # Пример целевых значений

