from flask import Flask, render_template, request, session, redirect
import requests
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVC
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import numpy as np


app = Flask(__name__)
app.secret_key = "Hello World"

### Feature Importance Calculator function for SVM
def permutation_importance_score(estimator, X, y):
    score = permutation_importance(estimator, X, y, scoring='accuracy')
    return score.mean(axis=1)

#### Function for handling Non-numerical Data
def handle_non_numerical_data(df):
    columns = df.columns.values
    for column in columns:
        text_digit_vals = {}
        def convert_to_int(val):
            return text_digit_vals[val]

        if df[column].dtype != np.int64 and df[column].dtype != np.float64:
            column_contents = df[column].values.tolist()
            unique_elements = set(column_contents)
            x = 0
            for unique in unique_elements:
                if unique not in text_digit_vals:
                    text_digit_vals[unique] = x
                    x+=1

            df[column] = list(map(convert_to_int, df[column]))

    return df

### Function for Implementing Random Forest Algorithm
def MLApplier(MLALGO):
    try:
        #Step1 To read Dataframe 
        df = handle_non_numerical_data(pd.read_excel('ChurnAnalysis.xlsx'))
        print(df.head())


        # Step 2: Split the data into features and target
        X = df.drop(session['OutputFields'], axis=1)  # Features
        y = df[session['OutputFields']]  # Target

        if MLALGO == "Random Forest":
            # Step 3: Create and train a Random Forest Regressor
            random_forest = RandomForestRegressor()
            random_forest.fit(X, y)

            # Step 4: Get feature importances
            feature_importances = random_forest.feature_importances_

            # Step 5: Associate feature importances with feature names
            feature_importance_dict = dict(zip(X.columns, feature_importances))
        elif MLALGO == "SVM":
            # Step 3: Create and train an SVM classifier
            svm = SVC()
            svm.fit(X, y)

            # Step 4: Get feature importances using the coefficients
            feature_importances = permutation_importance_score(svm, X, y)

            # Step 5: Associate feature importances with feature names
            feature_importance_dict = dict(zip(X.columns, feature_importances))
            print(feature_importance_dict)
        elif MLALGO == "Linear Regression":
            # Step 3: Create and train a Linear Regression model
            linear_regression = LinearRegression()
            linear_regression.fit(X, y)

            # Step 4: Get feature importances using coefficients
            feature_importances = linear_regression.coef_

            # Step 5: Associate feature importances with feature names
            feature_importance_dict = dict(zip(X.columns, feature_importances))

        elif MLALGO == "Logistic Regression":
            # Step 3: Create and train a Logistic Regression model
            logistic_regression = LogisticRegression()
            logistic_regression.fit(X, y)

            # Step 4: Get feature importances using coefficients
            feature_importances = logistic_regression.coef_[0]

            # Step 5: Associate feature importances with feature names
            feature_importance_dict = dict(zip(X.columns, feature_importances))
        else:
            feature_importance_dict = {"MLAlgo Selected": "Under Development"}

        return feature_importance_dict
    
    except Exception as e:
        return f"Caught an error Error: {str(e)}"






## Home Page
@app.route("/")
def HomePage():
    ## Showing all the columns in the uploaded Excel Sheet
    if 'ChoosingOutputFields' not in session:
        session['ChoosingOutputFields'] = "Upload Excel Sheets"
    ## Column choosen as output for Machine Learning Algorithms
    if 'OutputFields' not in session:
        session['OutputFields'] = "Upload Excel Sheets"
    ## Temp Variable
    if 'ShowData' not in session:
        session['ShowData'] = 0
    ## Contains the descriptive stats of Uploaded Dataframe
    if 'DescriptiveData' not in session:
        session['DescriptiveData'] = "Upload Excel Sheets"
    ## For future Use
    if 'DividingDataFields' not in session:
        session['DividingDataFields'] = "Upload Excel Sheets"
    ## Contains the Output of ML Model applied
    if 'MLOutput' not in session:
        session['MLOutput'] = "Upload Excel Sheets"
    ## Contains the list of Machine Learning Algorithms
    if 'MLAlgoList' not in session:
        session['MLAlgoList'] = "Not Connected"
    ## Choose ML Algorithm to be used
    if 'MLAlgo' not in session:
        session['MLAlgo'] = "Not Selected"
    ## Particular Attribute Choosen
    if 'Attribute' not in session:
        session ['Attribute'] = "Not Selected"
    return render_template('HomePage.html')


## Preparation
@app.route("/preparation")
def Preparation():
    try:
        df = pd.read_excel('ChurnAnalysis.xlsx')
        session['DescriptiveData'] = {
            "1" : 20,
            "2" : 30,
            "3" : 50,
            "4" : 40
        }
        print("Dataframe Read")
        session['ChoosingOutputFields'] = [i for i in df.columns]
    except:
        session['ChoosingOutputFields'] = 'Empty'
    return render_template('Preparation.html', ChoosingOutputFields=session['ChoosingOutputFields'], DescriptiveData=session['DescriptiveData'], DividingDataFields=session['DividingDataFields'], OutputFields=session['OutputFields'], )

@app.route("/preparation/<Option>", methods=['GET', 'POST'])
def prepOption(Option):
    if Option == "1":
        if request.method == 'POST':
            file = request.files['file']
            if file:
                file.save("ChurnAnalysis.xlsx")
                session['ShowData'] = 1
                print("File Uploaded")
                return redirect("/preparation")
                
    

    return f'{Option} : {Option == "1"}'

## Prediction
@app.route("/prediction")
def Prediction():
    df = pd.read_excel('ChurnAnalysis.xlsx')
    # Prepare the dataframe for the API call
    df_json = df.to_json(orient='records')
    session['MLAlgoList'] = requests.get("http://127.0.0.1:8080/ML_Available").json()
    #session['MLOutput'] = requests.get(f"http://127.0.0.1:8080/TrainData/{session['OutputFields']}/{df_json}").json()
    print("Main App")
    print(session['MLTechniques'], session['MLOutput'])
    return render_template('Prediction.html', 
                           MLAlgoList=session['MLAlgoList'], 
                           MLOutput=session['MLOutput'], 
                           MLAlgo=session['MLAlgo'],
                           ListOfAttribute=[i for i in session['ChoosingOutputFields'] if i != session['OutputFields']],
                           Attribute=session['Attribute'])

## Report
@app.route("/report")
def Report():
    #print(RandomForest())
    return render_template('Report.html', GeneratedWeights=MLApplier("Random Forest"))

## Login
@app.route("/login")
def Login():
    return render_template('Login.html')

## Sign-Up
@app.route("/Sign-Up")
def SignUp():
    return render_template('Sign Up.html')

## Show Table
@app.route("/showData/<Option>")
def showTable(Option):
    if Option == '1':
        try:
            df = pd.read_excel('ChurnAnalysis.xlsx')
            return df.to_html()
        except:
            return redirect('/preparation')
    elif Option == '2':
        try:
            df = pd.read_excel('ChurnAnalysis.xlsx')
            return df.describe().to_html()
        except:
            return redirect('/preparation')
    
## ChoosingOutputFields => Preparation Tab
@app.route("/ChoosingOutputFields/<Option>")
def ChoosingOutputFields(Option):
    session['OutputFields'] = Option
    return redirect('/preparation')

## ChoosingMLAlgorithm => Prediction Tab
@app.route("/ChoosingMLAlgorithm/<Option>")
def ChoosingMLAlgorithm(Option):
    session['MLAlgo'] = Option
    return redirect('/prediction')

## ChoosingAttribute => Prediction Tab
@app.route("/ChoosingAttribute/<Option>")
def ChoosingAttribute(Option):
    session['Attribute'] = Option
    return redirect('/prediction')

## Prediction => Training Data on mentioned Machine Learning Models
@app.route("/trainData/<MLAlgo>")
def trainData(MLAlgo):
    session['MLOutput'] = MLApplier(MLAlgo)
    return redirect('/prediction')

### Preperation => Data to be plotted
@app.route("/DataPlot")
def DataPlot():
    

if __name__ == '__main__':
    app.run(debug=True, port=8000)