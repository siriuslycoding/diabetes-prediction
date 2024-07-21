from flask import Flask, request, jsonify, render_template
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def run_notebook(notebook_path, params):
    print(f"Running notebook: {notebook_path}")
    
    with open(notebook_path) as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Ensure the notebook starts with correct initialization
    first_cell = notebook.cells[0]
    
    # Prepare the code to inject
    first_cell_source = f"""
import pandas as pd
import json

# Initialize input_data with the data from the request
input_data = {json.dumps(params)}

def finalprediction(input_data):
    columns = ["gender", "age", "hypertension", "heart_disease", "smoking_history", "bmi", "HbA1c_level", "blood_glucose_level"]
    
    # Convert the input data to a DataFrame with the correct column names
    input_data_df = pd.DataFrame(input_data, columns=columns)
    y_pred = voting_clf.predict(input_data_df)
    
    # If the model output is binary (0: Non-diabetic, 1: Diabetic)
    result = "Diabetic" if y_pred[0] == 1 else "Non-diabetic"
    
    # Return result
    return json.dumps({"Prediction": result})

# Call the function with the input_data
prediction_result = finalprediction(input_data)
print(prediction_result)
"""
    first_cell['source'] = first_cell_source
    
    # Execute the notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(notebook, {'metadata': {'path': './'}})
    
    # Collect the output
    output = []
    for cell in notebook.cells:
        if 'outputs' in cell:
            for out in cell['outputs']:
                if 'text' in out:
                    output.append(out['text'])
                elif 'data' in out:
                    output.append(out['data']['text/plain'])
    
    result = ''.join(output).strip()
    
    print(f"Notebook output: {result}")
    return result

@app.route('/run_notebook', methods=['POST'])
def run_notebook_route():
    data = request.json
    notebook_path = "LGBM.ipynb"  # Path to your notebook
    
    try:
        output = run_notebook(notebook_path, data)
        return jsonify({'Prediction': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
