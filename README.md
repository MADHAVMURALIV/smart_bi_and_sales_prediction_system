A web-based Business Intelligence application that analyzes sales data and predicts future sales trends using machine learning.

## Project Overview
This project allows users to upload sales data in CSV format and generates interactive visual insights. It applies machine learning models to forecast future sales, compare actual vs predicted performance, and assist in inventory planning through data-driven recommendations.

## Features
- Upload CSV-based sales data
- Interactive dashboard with dynamic charts
- Sales prediction using Random Forest Regression
- Future sales forecasting
- Actual vs Predicted sales comparison
- Inventory planning (Reorder, Excess, Optimal stock)
- Downloadable PDF business report
- Light / Dark theme toggle
- Live date and time display

## Tech Stack
- Python
- Flask
- Scikit-learn
- Pandas
- NumPy
- ReportLab
- HTML, CSS, JavaScript
- Chart.js

## Project Structure
- `app.py` – Flask backend and ML pipeline
- `utils/` – Data preprocessing, ML model, forecasting, inventory logic
- `templates/`
  - `landing.html` – Landing page UI
  - `dashboard.html` – Main dashboard UI
- `static/`
  - `css/` – Styling
  - `js/` – Chart rendering and client-side logic
- `requirements.txt` – Python dependencies

## Setup Instructions
pip install -r requirements.txt

## Run backend 
python app.py 

`The application will automatically open in the browser at : http://http://127.0.0.1:5000/`


## Inventory Planning Logic
- **Reorder Stock** – Predicted demand exceeds average sales, indicating restocking is required.
- **Excess Stock** – Inventory exceeds forecasted demand, suggesting overstock.
- **Optimal Stock** – Inventory levels are well balanced with demand.

## Project Objective
The Smart BI & Sales Prediction System aims to bridge the gap between raw sales data and strategic business decision-making by combining data analytics, machine learning, and intuitive visualization.

# UI and Outputs

<img width="1919" height="914" alt="image" src="https://github.com/user-attachments/assets/9f909ca9-7fab-4208-8c0f-f4b58f591662" />
<img width="1902" height="1078" alt="Screenshot 2026-01-01 190309" src="https://github.com/user-attachments/assets/9b1851e0-9f56-4497-9e44-5035641b085a" />
<img width="1898" height="1077" alt="Screenshot 2026-01-01 190201" src="https://github.com/user-attachments/assets/9c414894-8781-410b-ba92-b8a9d79f98ac" />

<img width="1905" height="1029" alt="Screenshot 2026-01-01 190132" src="https://github.com/user-attachments/assets/df8999ac-cb1a-4bf9-98af-210c81b2296a" />
<img width="1902" height="1079" alt="Screenshot 2026-01-01 190243" src="https://github.com/user-attachments/assets/5666537a-5fe9-474d-ae14-a5b2c53743b6" />
<img width="1910" height="1069" alt="Screenshot 2026-01-01 190235" src="https://github.com/user-attachments/assets/b542360f-0984-4c2e-949d-dba17f6b420a" />

<img width="1917" height="1069" alt="Screenshot 2026-01-01 190257" src="https://github.com/user-attachments/assets/1026c8d5-a63d-43d9-9e35-ea85fa73a2e8" />

<img width="789" height="851" alt="Screenshot 2026-01-02 172457" src="https://github.com/user-attachments/assets/fc8a86e4-be11-4622-b10b-e648704b166e" />
<img width="798" height="855" alt="Screenshot 2026-01-02 172508" src="https://github.com/user-attachments/assets/83f1f997-f368-48f7-a8a3-0325fd48d94d" />





