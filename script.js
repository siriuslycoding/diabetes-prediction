document.getElementById('prediction-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const age = document.getElementById('age').value;
    const gender = document.getElementById('gender').value;
    const Hypertension = document.getElementById('Hypertension').value;
    const bmi = document.getElementById('bmi').value;
    const heartDisease = document.getElementById('heartDisease').value;
    const smokingHistory = document.getElementById('smokingHistory').value;
    const HbA1c = document.getElementById('HbA1c').value;
    const bloodGlucose = document.getElementById('bloodGlucose').value;

    // Assuming you have an API endpoint to get the prediction
    fetch('http://your-backend-api-url/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            age: age,
            gender: gender;
            Hypertension: Hypertension;
            bmi: bmi,
            heartDisease: heartDisease;
            smokingHistory: smokingHistory;
            HbA1c: HbA1c;
            bloodGlucose: bloodGlucose;
            
        }),
    })
    function predict() {
        const notebookPath = document.getElementById('notebook-path').value;
    
        fetch('/run_notebook', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ notebook_path: notebookPath })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('result').innerText = Error: ${data.error};
            } else {
                document.getElementById('result').innerText = Output: ${data.output};
            }
        })
        .catch(error => {
            document.getElementById('result').innerText = Error: ${error};
        });
    }
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        const resultText = document.getElementById('result-text');

        resultText.textContent = `Prediction: ${data.prediction}`;
        resultDiv.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
