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

<img width="778" height="853" alt="Screenshot 2025-12-31 013657" src="https://github.com/user-attachments/assets/5923bc9e-7076-47c5-9169-0b9de53f14fe" />
<img width="832" height="873" alt="Screenshot 2025-12-31 013618" src="https://github.com/user-attachments/assets/d7431ebd-ac16-46df-a3f0-7156c20a1228" />
<img width="1901" height="947" alt="Screenshot 2025-12-31 013152" src="https://github.com/user-attachments/assets/8def255e-e585-4394-8cfa-82a5163d7e75" />
<img width="1907" height="904" alt="Screenshot 2025-12-31 013123" src="https://github.com/user-attachments/assets/cbb0cc3f-27e6-4cca-bf22-564ed42d7d13" />
<img width="1919" height="894" alt="Screenshot 2025-12-31 013110" src="https://github.com/user-attachments/assets/6dd12133-5aa7-4748-a0a7-8f9993d693f7" />
<img width="1910" height="899" alt="Screenshot 2025-12-31 013057" src="https://github.com/user-attachments/assets/40055765-8cab-4fd6-bbd3-892a5b452af0" />
<img width="1919" height="869" alt="Screenshot 2025-12-31 012951" src="https://github.com/user-attachments/assets/60672cf2-35a7-4ff3-94b1-b1d80c1de88c" />
<img width="1918" height="904" alt="Screenshot 2025-12-31 013043" src="https://github.com/user-attachments/assets/82c0bf69-9b69-4ca3-a7b8-6738386b0b5e" />
<img width="1902" height="901" alt="Screenshot 2025-12-31 012910" src="https://github.com/user-attachments/assets/28c6fae7-07d1-4ee2-a204-37d6aba25d13" />
<img width="1900" height="900" alt="Screenshot 2025-12-31 012736" src="https://github.com/user-attachments/assets/2fa51a59-bc32-4973-87e5-56dd101b0b26" />
<img width="1900" height="909" alt="Screenshot 2025-12-31 012721" src="https://github.com/user-attachments/assets/67b3a214-c304-464f-b17c-f91e4fa3b43f" />
<img width="1916" height="907" alt="Screenshot 2025-12-31 012650" src="https://github.com/user-attachments/assets/5571a931-a945-4d25-8717-a4645c04b510" />
