import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv('sales_data.csv')
data['Date'] = pd.to_datetime(data['Date'])
data['Day'] = data['Date'].dt.day

# Features and target variable
X = data[['Day']]
y = data['Sales']

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Save predictions to the dataset
data['Predicted Sales'] = model.predict(data[['Day']])
data.to_csv('sales_data_with_predictions.csv', index=False)

# Visualization
plt.scatter(X_test, y_test, color='blue', label='Actual Sales')
plt.plot(X_test, y_pred, color='red', label='Predicted Sales')
plt.title('Sales Prediction')
plt.xlabel('Day of Month')
plt.ylabel('Sales')
plt.legend()
plt.show()

print("Model Coefficients:", model.coef_)
print("Model Intercept:", model.intercept_)
