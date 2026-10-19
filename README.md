# AI-Based Structural Damage Detection and Infrastructure Risk Prediction System

## Overview
The Structural Damage Prediction system is a machine-learning-based application designed to estimate the potential damage level of buildings using their structural characteristics. It helps users assess building risk through a simple web interface.

## Features
- Building information input and assessment
- Machine-learning-based damage prediction
- Damage-level and risk assessment
- Interactive web interface
- Python-based prediction backend
- React-based frontend

## Technologies Used
- **Frontend:** React, JavaScript, CSS, Vite
- **Backend:** Python, FastAPI
- **Machine Learning:** Scikit-learn
- **Data Processing:** Pandas, NumPy
- **Version Control:** Git and GitHub

## Project Structure
```text
Structural-Damage-Prediction/
├── backend/
│   └── main.py
├── frontend/
│   ├── src/
│   ├── index.html
│   └── package.json
├── app.py
├── simple_model.py
├── model_metrics.json
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/pasulavidisha5-ui/Structural-Damage-Prediction.git
cd Structural-Damage-Prediction
```

### 2. Set up the Python environment
```bash
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
```

### 3. Set up the frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Run the backend
Follow the backend startup instructions in `backend/main.py` and configure the required machine-learning model file before running predictions.

## Machine Learning Model
The application uses a trained machine-learning model to estimate building damage. The model file must be available locally or through the configured model-storage service before predictions can run.

## Disclaimer
This project is intended for educational and preliminary assessment purposes. Its predictions are not a substitute for a professional structural inspection or engineering assessment.

## Author
**Pasula Vidisha**

GitHub: https://github.com/pasulavidisha5-ui
