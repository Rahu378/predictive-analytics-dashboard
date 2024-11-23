import joblib

def get_predictions(day):
    # Load trained model
    model = joblib.load("models/sales_model.pkl")
    # Make prediction
    predicted_sales = model.predict([[day]])
    return predicted_sales[0]
