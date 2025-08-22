console.log("Javascript loaded successfully!")

const predictionForm = document.getElementById('prediction-form')

predictionForm.addEventListener('submit', function(event){
  event.preventDefault();

  const formData = new FormData(predictionForm)
  const data = Object.fromEntries(formData.entries());

  for (const key in data){
    data[key] = parseFloat(data[key]);
  }

  const jsonPayload = JSON.stringify(data);

    fetch('http://127.0.0.1:5000/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: jsonPayload
    })
    .then(response =>{
    if(!response.ok){
      throw new Error('Server responded with an error: ${response.status}');
    }
    return response.json();
  })
  .then(predictionData => {
    console.log("Success! Received prediction from API:", predictionData);
    const resultContainer = document.getElementById('result-container');

        // Step 2: Extract the data we want to display from the response object.
        const label = predictionData.prediction_label;
        const confidenceNonDiabetic = (predictionData.confidence_scores['Non-Diabetic'] * 100).toFixed(2);
        const confidenceDiabetic = (predictionData.confidence_scores['Diabetic'] * 100).toFixed(2);

        // Step 3: Build the HTML string to display the result.
        // We use template literals (backticks ``) to easily construct the string.
        const resultHTML = `
            <h2>Prediction Result</h2>
            <p><strong>Outcome:</strong> ${label}</p>
            <p><strong>Confidence Scores:</strong></p>
            <ul>
                <li>Non-Diabetic: ${confidenceNonDiabetic}%</li>
                <li>Diabetic: ${confidenceDiabetic}%</li>
            </ul>
        `;

        // Step 4: Inject the HTML into our result container.
        resultContainer.innerHTML = resultHTML;

        // Step 5 (Enhancement): Change the text color based on the prediction.
        if (label === 'Diabetic') {
            resultContainer.style.color = 'red';
        } else {
            resultContainer.style.color = 'green';
        }
  })
  .catch(error => {
    console.error("Error communicating with API", error);
    const resultContainer = document.getElementById('result-container');
    resultContainer.innerHTML = `<p style="color: red;">Error: Could not get a prediction. Please check the console for details.</p>`;
  });
});
