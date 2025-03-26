from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import csv
import pandas as pd
import os

app = Flask(__name__)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://Fisayo:<Walexy1994>@cluster0.vxqlf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["survey_db"]
collection = db["responses"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if collection.count_documents({}) >= 10:
            return "Survey limit reached. Maximum of 10 users allowed."
        
        data = {
            "age": request.form['age'],
            "gender": request.form['gender'],
            "total_income": request.form['total_income'],
            "expenses": {
                "utilities": request.form.get('utilities', 0),
                "entertainment": request.form.get('entertainment', 0),
                "school_fees": request.form.get('school_fees', 0),
                "shopping": request.form.get('shopping', 0),
                "healthcare": request.form.get('healthcare', 0)
            }
        }
        collection.insert_one(data)
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/export', methods=['GET'])
def export_data():
    data = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data)
    csv_file = "survey_data.csv"
    df.to_csv(csv_file, index=False)
    return f"Data exported to {csv_file}" 

if __name__ == '__main__':
    app.run(debug=True)
