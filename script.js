document.addEventListener('DOMContentLoaded', function() {
    // Object to store user selections
    let userSelections = {
        // Mapping each indicator to its corresponding action
    };

    function updateActionOptions(indicatorSelectorId, actionSelectorId) {
        const indicatorSelector = document.getElementById(indicatorSelectorId);
        const actionSelector = document.getElementById(actionSelectorId);

        indicatorSelector.addEventListener('change', function() {
            // Update action options based on indicator selection
            updateActionSelectorOptions(this.value, actionSelector);

            // Ensure the actionSelectorId is reset when the indicator changes
            userSelections[indicatorSelectorId] = { indicator: this.value, action: '' };

            // Update disable state for options in other indicator selectors
            updateDisableStateForIndicatorOptions();
        });

        actionSelector.addEventListener('change', function() {
            // Update user selections object with the corresponding action
            if (userSelections[indicatorSelectorId]) {
                userSelections[indicatorSelectorId].action = this.value;
            } else {
                // In case the indicator is not yet selected, just save the action
                userSelections[indicatorSelectorId] = { indicator: '', action: this.value };
            }
        });
    }

    function updateActionSelectorOptions(indicatorValue, actionSelector) {
        actionSelector.innerHTML = '<option selected disabled>Choose Action</option>';
        let options = [];
        switch (indicatorValue) {
            case 'RSI':
                options = ['Above 70', 'Below 30'];
                break;
            case 'MACD':
                options = ['Above 0', 'Below 0', 'Cross above', 'Cross below'];
                break;
            case '200MA':
                options = ['Above Price', 'Below Price', 'Golden Cross', 'Death Cross'];
                break;
            case '100MA':
                options = ['Above Price', 'Below Price'];
                break;
            case '50MA':
                options = ['Golden Cross', 'Death Cross'];
                break;
            case 'Bollinger Band':
                options = ['Reach Top', 'Reach Bottom'];
                break;
        }
        options.forEach(function(option) {
            const opt = document.createElement('option');
            opt.value = option;
            opt.textContent = option;
            actionSelector.appendChild(opt);
        });
    }

    function updateDisableStateForIndicatorOptions() {
        const selectedOptions = [
            document.getElementById('indicator1').value,
            document.getElementById('indicator2').value,
            document.getElementById('indicator3').value
        ];
        ['indicator1', 'indicator2', 'indicator3'].forEach(selectorId => {
            const selector = document.getElementById(selectorId);
            Array.from(selector.options).forEach(option => {
                option.disabled = selectedOptions.includes(option.value) && option.value !== selector.value;
            });
        });
    }

    // Initialize action options update mechanism, disable logic, and selections saving
    updateActionOptions('indicator1', 'indicator4');
    updateActionOptions('indicator2', 'indicator5');
    updateActionOptions('indicator3', 'indicator6');

    // Initial call to set correct disable state upon page load
    updateDisableStateForIndicatorOptions();

    // Optional: For demonstration, you could have a button to log the final selections
    document.getElementById('submitButton').addEventListener('click', () => {
        console.log(userSelections);
    });
});
