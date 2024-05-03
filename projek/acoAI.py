import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.image import imread
import random

class AntColonyOptimization():
    def __init__(self, cities, totalAnt, alpha, beta,evaporation):
        self.cities = cities
        self.totalAnt = totalAnt
        self.alpha = alpha # nentuin seberapa pengaruhnya pheromone nanti buat nentuin kota yang bakal di pilih di iterasi
        self.beta = beta # nentuin seberapa pengaruhnya jauh kota nanti buat nentuin kota yang bakal di pilih di iterasi
        self.evaporation= evaporation
        self.pheromone = self.setPheromone()

    def setPheromone(self):
        pheromone = {}
        for city1 in self.cities:
            pheromone[city1] = {}
            for city2 in self.cities:
                if city1 != city2:
                    pheromone[city1][city2] = 1.0
        return pheromone

    def calculateDistance(self, city1, city2):
        xC1 = self.cities[city1][0]
        yC1 = self.cities[city1][1]
        xC2 = self.cities[city2][0]
        yC2 = self.cities[city2][1]
        return (((xC1 - xC2) ** 2 + (yC1 - yC2) ** 2)) ** 0.5
    
    def moveToNextCity(self, currentCity, visitedCities):
        unvisitedCities = []
        for city in self.cities:
            if city not in visitedCities:
                unvisitedCities.append(city)
            
        probabilities = []
        totalProbability = 0
        for city in unvisitedCities:
            pheromone = self.pheromone[currentCity][city]
            distance = self.calculateDistance(currentCity, city)

            #rumus atasnya pheromone^alpha * 1/jarak^beta
            probability = pheromone ** self.alpha * (1.0 / distance) ** self.beta 

            probabilities.append((city, probability))
            totalProbability += probability # akses probabilitynya untuk di tambahkan
    
        cityList = []
        probabilityList = []
        for city, probability in probabilities:
            probability = probability / totalProbability # yang dimana rumusnya probabiltiy / total probability semua kota
            cityList.append(city)
            probabilityList.append(probability)
                    
    
        choice = random.choices([city for city, _ in probabilities], [probability for _, probability in probabilities]) # ambil kota secara random
        return choice[0] # kota selanjutnya yang bakal di return
    
    def updatePheromone(self, ants):
        totalLength = 0
        for ant in ants:
            totalLength += 1.0/ant.pathLength # rumus sigma yang dimana tsp menggunakan 1/total length

        for city1 in self.cities:
            for city2 in self.cities:
                if city1 != city2:
                    self.pheromone[city1][city2] = (1-self.evaporation) * self.pheromone[city1][city2] + totalLength # update pheromone
                    # rumusnya evaporation *  pheromone + total length
    
    def run(self,iterasi):
        bestPath = None
        bestPathLength = float('inf')
        antList=[]

        for i in range(iterasi):
            counter =0
            for ant in range(self.totalAnt):
                ant = Ant()
                currentCity = random.choice(list(self.cities.keys()))# ngerandom posisi awal semut
                unvisitedCities = set(cities.keys()) - {currentCity}
                ant.appendPath(currentCity)

                while unvisitedCities: # selama kota belum di visit semua
                    nextCity = self.moveToNextCity(currentCity,ant.path)
                    ant.appendPath(nextCity)
                    ant.pathLength += self.calculateDistance(currentCity, nextCity)
                    # ant.path.remove(nextCity)
                    currentCity = nextCity
                    unvisitedCities.remove(currentCity)
                antList.append(ant)

                # ant.pathLength += self.calculateDistance(currentCity,ant.path[0]) # hitung jarak kota awal dgn kota akhir
                # ant.appendPath(ant.path[0])

                if ant.pathLength < bestPathLength: # kalau jaraknya lebih pendek di tandain
                    bestPathLength = ant.pathLength
                    bestPath = ant.path
                    counterAnt = counter
                
                counter+=1
                self.updatePheromone(antList)

            # ngeprint path yang paling bagus di iterasi
            print("Iterasi ke ",i, "Semut Ke ",counterAnt)
            print("Path : ",bestPath)
            print("Path Length : ",bestPathLength)
            print("--------------------------------------")

        return bestPath, bestPathLength

class Ant:
    def __init__(self):
        self.path = []
        self.pathLength = 0
    
    def appendPath(self,city):
        self.path.append(city)
        
def addCities(graph,cities):
        for city in cities:
            graph.add_node(city)
        

cities = {
    "Washington": (-24, 11),
    "Oregon": (-24, 6),
    "California": (-24, 0),
    "Los Angeles": (-21, -6),
    "Nevada": (-19, 1),
    "Idaho": (-18, 10),
    "Las Vegas": (-18, -3),
    "Utah": (-14, 0),
    "Arizona": (-14, -5),
    "Montana": (-13, 10),
    "Wyoming": (-11, 5),
    "Colorado": (-9, 0),
    "New Mexico": (-9, -6),
    "North Dakota": (-4, 11),
    "South Dakota": (-4, 7),
    "Nebraska": (-3, 3),
    "Texas": (-3, -8),
    "Kansas": (-2, -1),
    "Oklahoma": (-1, -4),
    "Minnesota": (1, 9),
    "Houston": (1, -10),
    "Iowa": (3, 4),
    "Missouri": (3, -1),
    "Arkansas": (4, -5),
    "Louisiana": (4, -10),
    "Wisconsin": (6, 7),
    "Mississippi": (6, -7),
    "Illinois": (7, 2),
    "Indiana": (9, 1),
    "Tennessee": (9, -4),
    "Alabama": (9, -7),
    "Kentucky": (10, -2),
    "Michigan": (11, 6),
    "Georgia": (12, -7),
    "West Virginia": (14, 0),
    "South Carolina": (14, -6),
    "Florida": (14, -13),
    "Virginia": (16, -2),
    "North Carolina": (16, -4),
    "Pennsylvania": (17, 2),
    "New York": (19, 5),
    "Delaware": (19, 0),
    "New York City": (21, 2),
    "Vermont": (22, 7),
    "Massachusetts": (22, 4),
    "Connecticut": (22, 3),
    "Maine": (25, 8),

}

graph = nx.Graph()
addCities(graph,cities)
ant_colony = AntColonyOptimization(cities, totalAnt=47, alpha=1.0, beta=3.0, evaporation=0.5)

bestPath, bestPathLength = ant_colony.run(iterasi=10)
print("Best Path Route:")
for i in range(len(bestPath)):
    print(i,".",bestPath[i])
print("Best Path Length:", bestPathLength)

#MEMBUAT WINDOW 
plt.figure(figsize=(10,8))

#TITIK KOORDINAT SEMUA CITY
x_coordinate = [cities[city][0] for city in cities] 
y_coordinate = [cities[city][1] for city in cities] 

#PLOT SEMUA KOTA SESUAI KOORDINAT
plt.scatter(x_coordinate, y_coordinate, color='red')

#NAMA KOTA
for city, (x, y) in cities.items():
    plt.text(x, y, city, fontsize=8)

#LABEL 
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Cities')

# Load the image
image = imread("Map_of_USA_with_state_names_2.svg.png")

# Display the image
plt.imshow(image, extent=[min(x_coordinate)*1.2, max(x_coordinate)*1.2, min(y_coordinate)*1.3, max(y_coordinate)*1.35])

# Hide the axis labels
plt.axis('on')

# Plot the best path
path_x = [cities[city][0] for city in bestPath]
path_y = [cities[city][1] for city in bestPath]
path_x.append(path_x[0])  # Connect the last city to the first city
path_y.append(path_y[0])  # Connect the last city to the first city


# Plot the path segments
for i in range(len(path_x) - 1):
    if i == 0 :
        # path pertama warna merah
        plt.plot(path_x[i:i+2], path_y[i:i+2], color='red', linewidth=2.0)
    elif i == len(path_x) - 2:
        # path terakhir warna hijau
        plt.plot(path_x[i:i+2], path_y[i:i+2], color='green', linewidth=2.0)
    else:
        # path selain itu berwarna biru
        plt.plot(path_x[i:i+2], path_y[i:i+2], color='blue', linewidth=1.0)
   

#DISPLAY
plt.show()