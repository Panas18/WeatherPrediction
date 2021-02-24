import joblib
import pandas as pd 
max_model = joblib.load("maxModel.sav")
x = pd.read_csv("maxData/testx.csv", index_col = 0)
y = pd.read_csv("maxData/testy.csv", index_col = 0)

y = y.to_numpy().ravel()
x = x.to_numpy()
print(x[0].reshape(1,-1).shape)

def pred_temp(test_data):
    pred_temperature = max_model.predict(x[test_data].reshape(1,-1))
    actual_temperature = y[test_data]
    print(actual_temperature, pred_temperature)
    return pred_temperature, actual_temperature

if __name__ == "__main__":
    pred_temp(10)
