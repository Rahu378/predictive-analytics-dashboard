import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

# Load data
data = pd.read_csv("data/sales_data.csv")
data['Day'] = pd.to_datetime(data['Date']).dt.day

# Features and target
X = data[['Day']]
y = data['Sales']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "models/sales_model.pkl")

# Generate predictions
data['Predicted Sales'] = model.predict(data[['Day']])
data.to_csv("data/sales_data_with_predictions.csv", index=False)

print("Model trained and predictions saved!")
