from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route("/", methods = ['GET'])
def Home():
    return render_template('index.html')

sc = pickle.load(open('scaler.pkl', 'rb'))

@app.route("/predict", methods = ['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == "POST":
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present Price'])
        KMS_Driven = int(request.form['KMS Driven'])
        #KMS_Driven2 = np.log(KMS_Driven)
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel Type']
        if Fuel_Type_Petrol == "Petrol":
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif Fuel_Type_Petrol == "Diesel":
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
        Year = 2021 - Year
        Seller_Type_Individual = request.form['Seller Type']
        if Seller_Type_Individual == "Individual":
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Manual = request.form['Transmission Manual']
        if Transmission_Manual == "Manual":
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        input = sc.transform([[Year,Present_Price,KMS_Driven,Owner,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,
                                    Transmission_Manual]])

        prediction = model.predict(input)
        output = round(prediction[0], 2)

        if output<0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text= "You Can Sell The Car at {} Lakhs".format(output))
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)
