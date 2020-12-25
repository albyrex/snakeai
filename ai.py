
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

class ai:
    def __init__(self, epochs=500):
        self.epochs = epochs
        self.trained_model = None
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        self.hidden_layer = 2

    def data_segregation(self, dataset):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(dataset["data"], dataset["target"])

    def data_segregation(self, data, target):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(data, target)

    def train(self):
        self.trained_model = MLPClassifier((10, 10, 10), max_iter=self.epochs, random_state=1).fit(self.x_train, self.y_train)

    def evaluation(self):
        score = self.trained_model.score(self.x_test, self.y_test)
        return score







"""
ai = ai()
data = dict()
data["data"] = []
data["target"] = []

for i in range(250):
    a = (0,0)
    b = (0,1)
    c = (1,0)
    d = (1,1)
    data["data"].append(a)
    data["data"].append(b)
    data["data"].append(c)
    data["data"].append(d)
    a = 0
    b = 1
    c = 1
    d = 0
    data["target"].append(a)
    data["target"].append(b)
    data["target"].append(c)
    data["target"].append(d)


ai.data_segregation(data)
ai.train()
print("Score: " + str(ai.evaluation()))
print(ai.trained_model.predict([(0, 0)]))
print(ai.trained_model.predict([(1, 0)]))
print(ai.trained_model.predict([(0, 1)]))
print(ai.trained_model.predict([(1, 1)]))

"""