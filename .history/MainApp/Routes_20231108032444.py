from flask import Flask, render_template, request, session, redirect
import requests
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


app = Flask(__name__)
app.secret_key = "Hello World"

def RandomForest():
      

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
    return render_template('Report.html')

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

if __name__ == '__main__':
    app.run(debug=True, port=8000)