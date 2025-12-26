# Smart Business Intelligence & Sales Prediction System

A web-based Business Intelligence application that analyzes historical sales data and predicts future sales using Machine Learning. The system supports data-driven decision-making for sales forecasting, revenue planning, and business strategy.

## Project Description

This project implements a Smart Business Intelligence system that combines sales analytics with predictive modeling. Historical retail sales data is processed to extract insights, and a trained machine learning model is used to forecast monthly sales based on business attributes such as category, sub-category, region, and time.

## Core Functionalities

- Sales Prediction  
  Predicts monthly sales using machine learning based on user inputs.

- Sales Analytics  
  Provides aggregated sales metrics and trend-ready data for dashboards.

- Business Insights  
  Identifies best-performing categories, regions, and peak sales periods.

- Dataset Overview  
  Displays dataset statistics including available years, categories, and regions.

## Tech Stack

Backend: Python, Flask  
Data Processing: Pandas  
Machine Learning: Scikit-learn, Joblib  
Frontend: HTML, CSS, JavaScript  

## Dataset

Superstore Sales Dataset (Kaggle)  
Structured tabular retail sales data  
Aggregated at monthly level for stable forecasting  

## Project Structure

smart-bi-sales-prediction/
├── backend/
│   ├── app.py
│   ├── preprocess.py
│   ├── train_model.py
│   └── templates/
│       ├── landing.html
│       └── predict.html
├── data/
│   └── processed_sales.csv
├── models/
│   └── sales_model.pkl
└── README.md

## How to Run

Install dependencies:
pip install flask pandas scikit-learn joblib

Run the backend server:
python backend/app.py

Open in browser:
http://127.0.0.1:5000/

## Project Status

Sales prediction module implemented.  
Analytics and UI enhancements in progress.
