from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os
import plotly.graph_objs as go
import json
import plotly

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "secretkey"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global DataFrame
data = pd.DataFrame()

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# File upload route
@app.route("/upload", methods=["GET", "POST"])
def upload():
    global data
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file uploaded")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and file.filename.endswith(".csv"):
            try:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                uploaded_data = pd.read_csv(file_path)

                # Update global data
                data = uploaded_data
                flash("File uploaded and data loaded successfully!")
                return redirect(url_for("dashboard"))
            except Exception as e:
                flash(f"Error processing file: {e}")
                return redirect(request.url)
        else:
            flash("Invalid file format. Please upload a CSV file.")
            return redirect(request.url)
    return render_template("upload.html")

# Dashboard route
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    global data
    if data.empty:
        flash("No data available. Please upload a file.")
        return redirect(url_for("upload"))

    # Extract column names and types
    column_names = data.columns.tolist()
    numeric_columns = data.select_dtypes(include="number").columns.tolist()

    # Get user-selected columns for analysis
    x_axis = request.form.get("x_axis")
    y_axis = request.form.get("y_axis")

    # Default chart (if columns are not selected yet)
    chart_data = {}
    if x_axis and y_axis:
        chart = go.Figure()
        chart.add_trace(go.Scatter(
            x=data[x_axis],
            y=data[y_axis],
            mode='lines+markers',
            name=f"{y_axis} vs {x_axis}"
        ))
        chart_data = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        "dashboard.html",
        columns=column_names,
        numeric_columns=numeric_columns,
        chart_data=chart_data
    )

if __name__ == "__main__":
    app.run(debug=True)
