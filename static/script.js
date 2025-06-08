document.getElementById('predict-btn').addEventListener('click', function () {
    const stockName = document.getElementById('stock-name').value;
    const days = document.getElementById('days').value;

    if (stockName && days) {
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stock: stockName, days })
        })
        .then(response => response.json())
        .then(data => {
            const predicted = data.predictions;
            const futureChartCtx = document.getElementById('futureChart').getContext('2d');
            new Chart(futureChartCtx, {
                type: 'line',
                data: {
                    labels: predicted.map((_, i) => `Day ${i + 1}`),
                    datasets: [{
                        label: `Predicted Price for ${days} Days`,
                        data: predicted,
                        borderColor: 'rgba(153, 102, 255, 1)',
                        fill: false
                    }]
                }
            });
        })
        .catch(error => {
            console.error('Prediction error:', error);
            alert('Prediction failed. Try again.');
        });
    } else {
        alert('Please enter valid stock details!');
    }
});