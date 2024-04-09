function fetchDataAndProcessIt() {
    // Example symbol - replace with the user's choice if dynamic selection is required
    const symbol = 'AAPL';

    fetch(`/bollinger_bands?symbol=${symbol}`)
        .then(response => response.json())
        .then(bollingerData => {
            // Assuming you have another endpoint to fetch the current price or it's included in bollingerData
            const currentPriceData = { last: bollingerData.currentPrice }; // Adjust according to actual data structure

            processData(currentPriceData, bollingerData);
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Initialize polling
setInterval(() => {
    fetchDataAndProcessIt();
}, 5000);
