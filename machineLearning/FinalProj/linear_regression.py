import numpy as np 


class linearRegression():

    def __init__(self, learning_rate = 0.001, epchos = 1000):
        self.learning_rate = learning_rate
        self.epchos = epchos
        self.weight = None
        self.bias = None
    
    def fit(self, x, y):
        m , n = x.shape
        self.weight= np.zeros((n,1))
        self.bias = 0
        y = y.reshape(m,1)
        losses = []
        regression = True
        #for epchos in range(1000):
        while regression:
            y_hat = np.dot(x, self.weight) + self.bias
            loss = np.mean((y_hat- y) ** 2)
            losses.append(loss)
            #print(f"epchos: {epchos} loss: {loss}")
            #print(loss)
            dw = (1/m)* np.dot(x.T, (y_hat - y))
            db = (1/m)* np.sum((y_hat- y))
            self.weight -= self.learning_rate*dw
            self.bias -= self.learning_rate*db
            if len(losses) > 2:
                loss_1 = losses[len(losses)-1]
                loss_2 = losses[len(losses)-2]
                dl = loss_2- loss_1
                #print(f"Clange in loss:{dl}")
                if dl < 0.00001:
                   regression = False
        print(f"Loss: {loss}")
        return self.weight, self.bias, losses

    def predict(self, x):
        return np.dot(x, self.weight) +self.bias