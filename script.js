document.addEventListener('DOMContentLoaded', function() {
    // Function to update action options based on the selected indicator
    function updateActionOptions(indicatorSelectorId, actionSelectorId) {
        const indicatorSelector = document.getElementById(indicatorSelectorId);
        const actionSelector = document.getElementById(actionSelectorId);

        indicatorSelector.addEventListener('change', function() {
            // Update action options based on indicator selection
            updateActionSelectorOptions(this.value, actionSelector);

            // Update disable state for options in other indicator selectors
            updateDisableStateForIndicatorOptions();
        });
    }

    function updateActionSelectorOptions(indicatorValue, actionSelector) {
        // Clear existing options in action selector
        actionSelector.innerHTML = '<option selected disabled>Choose Action</option>';

        // Define actions based on selected indicator
        let options = [];
        if (indicatorValue === 'RSI') {
            options = ['Above 70', 'Below 30'];
        }

        else if (indicatorValue === 'MACD') {
            options = ['Above 0', 'Below 0', 'Cross lines above 0', 'Cross lines below 0'];
        }

        else if (indicatorValue === '200MA') {
            options = ['Uptrend', 'Downtrend', 'Golden cross', 'Death cross'];
        }

        else if (indicatorValue === '100MA') {
            options = ['Uptrend', 'Downtrend', 'support', 'Resistance'];
        }

        else if (indicatorValue === '50MA') {
            options = ['Uptrend', 'Downtrend', 'support', 'Resistance'];
        }

        else if (indicatorValue === 'Bollinger Band') {
            options = ['Above upper band', 'Below lower band'];
        }

        // Populate action selector with new options
        options.forEach(function(option) {
            const opt = document.createElement('option');
            opt.value = option;
            opt.textContent = option;
            actionSelector.appendChild(opt);
        });
    }

    function updateDisableStateForIndicatorOptions() {
        // Get current selections
        const selectedOptions = [
            document.getElementById('indicator1').value,
            document.getElementById('indicator2').value,
            document.getElementById('indicator3').value
        ];

        // Iterate over all indicator selectors to update option disable state
        ['indicator1', 'indicator2', 'indicator3'].forEach(selectorId => {
            const selector = document.getElementById(selectorId);
            Array.from(selector.options).forEach(option => {
                // Disable option if it's selected in any other selector
                if (selectedOptions.includes(option.value) && option.value !== selector.value) {
                    option.disabled = true;
                } else {
                    option.disabled = false;
                }
            });
        });
    }

    // Initialize action options update mechanism and disable logic
    updateActionOptions('indicator1', 'indicator4');
    updateActionOptions('indicator2', 'indicator5');
    updateActionOptions('indicator3', 'indicator6');

    // Initial call to set correct disable state upon page load
    updateDisableStateForIndicatorOptions();
});
