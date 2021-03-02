import os, sys
from pathlib import Path
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import joblib


# Directory of base and main project folder
BASE_DIR = Path(__file__).resolve().parent.parent
MAIN_DIR = Path(__file__).resolve().parent.parent.parent


# Adding path of raspberry  code and machine learning to python
RASPBERRY_DIR = os.path.join(MAIN_DIR, "RaspberryHardware")
PREDICTION_DIR = os.path.join(MAIN_DIR, "machineLearning", "FinalProj")
PRED_DATA_DIR = os.path.join(PREDICTION_DIR, "Datasets")
sys.path.insert(1, RASPBERRY_DIR)
sys.path.insert(2, PREDICTION_DIR)
sys.path.insert(3, PRED_DATA_DIR)

# import main

data_path = os.path.join(RASPBERRY_DIR, "data.csv")

# loading max and min models
#max_model_dir = os.path.join(PREDICTION_DIR, "maxModel.sav")
#min_model_dir = os.path.join(PREDICTION_DIR, "minModel.sav")
max_model = joblib.load(os.path.join(PREDICTION_DIR, "maxModel.sav"))
min_model = joblib.load(os.path.join(PREDICTION_DIR, "minModel.sav"))

max_pred = pd.read_csv(os.path.join(PRED_DATA_DIR, "MaxPrediction.csv"), index_col=0)
min_pred = pd.read_csv(os.path.join(PRED_DATA_DIR, "MinPrediction.csv"), index_col=0)


def test_pred(index):
    actual_max, pred_max = max_pred.iloc[index]
    actual_min, pred_min = min_pred.iloc[index]
    return actual_max, actual_min, round(pred_max, 1), round(pred_min, 1)

def pred_tomorrow(data):
    max_temp = max_model.predict(data)
    min_temp = min_model.predict(data)
    return round(max_temp[0], 1), round(min_temp[0], 1)

# Create your views here.
def index(request):
    temp_data = [25,24,24,23,23,11,14,13,11,10]
    database = pd.read_csv(data_path)
    data = request.POST.get("inputs")
    if data is None:
        data = 10
    actual_max, actual_min, pred_max, pred_min = test_pred(int(data))
    tomorrow_max, tomorrow_min = pred_tomorrow(temp_data)

    # humidity, temperature, dustDensity, pressure = main.data()
    # humidity = str(humidity) + " %"
    # temperature = str(temperature) + " C"
    # dustDensity = str(dustDensity) + " mW/cm^2"
    # pressure = str(pressure) + " hPa"
    humidity = 90
    temperature = 18
    dustDensity = 89
    pressure = 1000

    all_data = []
    for i in range(database.shape[0]):
        temp = database.iloc[i]
        all_data.append(dict(temp))

    context = {
        "data": all_data[database.shape[0] - 16 :],
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "dust": dustDensity,
        "uv": "210",
        "MaxTemperature": actual_max,
        "MaxPred": pred_max,
        "MinTemperature": actual_min,
        "MinPred": pred_min,
        "MaxTomorrow": tomorrow_max,
        "MinTomorrow": tomorrow_min
    }

    return render(request, "index.html", context)
