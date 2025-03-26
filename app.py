from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import csv
import pandas as pd
import os
from waitress import serve  # Required for production hosting

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
            "income": request.form['total_income'],  # Changed column name for consistency
            "expenses": {
                "utilities": float(request.form.get('utilities', 0)),
                "entertainment": float(request.form.get('entertainment', 0)),
                "school_fees": float(request.form.get('school_fees', 0)),
                "shopping": float(request.form.get('shopping', 0)),
                "healthcare": float(request.form.get('healthcare', 0))
            }
        }
        collection.insert_one(data)
        return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route('/export', methods=['GET'])
def export_data():
    data = list(collection.find({}, {"_id": 0}))
    
    if not data:
        return "No data available to export."

    df = pd.DataFrame(data)
    csv_file = "survey_data.csv"
    df.to_csv(csv_file, index=False)
    
    return f"Data exported to {csv_file}" 

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)  # Required for Cyclic deployment
