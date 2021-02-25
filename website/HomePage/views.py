import os, sys
from pathlib import Path
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import joblib


#Directory of base and main project folder
BASE_DIR = Path(__file__).resolve().parent.parent
MAIN_DIR = Path(__file__).resolve().parent.parent.parent


#Adding path of raspberry  code and machine learning to python
RASPBERRY_DIR = os.path.join(MAIN_DIR, "RaspberryHardware")
PREDICTION_DIR = os.path.join(MAIN_DIR, "machineLearning")
sys.path.insert(1,RASPBERRY_DIR)
sys.path.insert(2, PREDICTION_DIR)

#import main
data_path = os.path.join(RASPBERRY_DIR,"data.csv")

#loading max and min models
max_model_dir = os.path.join(PREDICTION_DIR, "maxModel.sav")
min_model_dir = os.path.join(PREDICTION_DIR, "minModel.sav")
max_model = joblib.load(max_model_dir)
min_model = joblib.load(min_model_dir)


#Test data path
max_testX_dir = os.path.join(PREDICTION_DIR,"maxData","testx.csv")
max_testY_dir = os.path.join(PREDICTION_DIR,"maxData","testy.csv")

min_testX_dir = os.path.join(PREDICTION_DIR,"minData","testx.csv")
min_testy_dir = os.path.join(PREDICTION_DIR,"minData","testy.csv")


x_max = pd.read_csv(max_testX_dir, index_col = 0)
y_max = pd.read_csv(max_testY_dir, index_col = 0)
y_max = y_max.to_numpy().ravel()
x_max = x_max.to_numpy()

x_min = pd.read_csv(min_testX_dir, index_col = 0)
y_min = pd.read_csv(min_testy_dir, index_col = 0)
y_min = y_min.to_numpy().ravel()
x_min = x_min.to_numpy()


def pred_max(data): #predicts max temperature from test data set
    input_data = x_max[data].reshape(1,-1)
    pred_temperature = max_model.predict(input_data)
    actual_temperature = y_max[data]
    return round(pred_temperature[0], 2), actual_temperature

def pred_min(data): #predicts min temperature from test dataset
    input_data = x_min[data].reshape(1,-1)
    pred_temperature = min_model.predict(input_data)
    actual_temperature = y_min[data]
    return round(pred_temperature[0], 2), actual_temperature


# Create your views here.
def index(request):
    database = pd.read_csv(data_path)
    data=request.POST.get("inputs")
    if data is None:
        data = 10
    pred_max_temp, actual_max_temp=pred_max(int(data))
    pred_min_temp, actual_min_temp = pred_min(int(data))
 
    #humidity , temperature, dustDensity,pressure = main.data()
    all_data =[]
    for i in range(database.shape[0]):
        temp = database.iloc[i]
        all_data.append(dict(temp))
        
    context={"data": all_data[database.shape[0]-16:],
            "temperature": "20 C",
            "humidity": "59%",
            "pressure": "120 hPa",
            "dust": "390 ug/m^3",
            "uv": "210 mW/cm^2",
            "MaxTemperature":actual_max_temp,
            "MaxPred": pred_max_temp,
            "MinTemperature":actual_min_temp,
            "MinPred": pred_min_temp,
        }
    
    return render(request,"index.html",context )


