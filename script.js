document.addEventListener('DOMContentLoaded', function() {
    // Object to store user selections
    let userSelections = {};

    // Setup the dynamic options for the action selectors based on indicator selection
    function updateActionOptions(indicatorSelectorId, actionSelectorId) {
        const indicatorSelector = document.getElementById(indicatorSelectorId);
        const actionSelector = document.getElementById(actionSelectorId);

        // When the indicator changes, update the action options and disable state
        indicatorSelector.addEventListener('change', function() {
            updateActionSelectorOptions(this.value, actionSelector);
            userSelections[indicatorSelectorId] = { indicator: this.value, action: '' };
            updateDisableStateForIndicatorOptions();
        });

        // When an action is selected, update the corresponding entry in the userSelections object
        actionSelector.addEventListener('change', function() {
            if (userSelections[indicatorSelectorId]) {
                userSelections[indicatorSelectorId].action = this.value;
            }
        });
    }

    // Populate the action selector based on the selected indicator
    function updateActionSelectorOptions(indicatorValue, actionSelector) {
        actionSelector.innerHTML = '<option selected disabled>Choose Action</option>';
        let options = [];
        switch (indicatorValue) {
            case 'RSI': options = ['Above 70', 'Below 30']; break;
            case 'MACD': options = ['Above 0', 'Below 0', 'Cross above', 'Cross below']; break;
            case '200MA': options = ['Above Price', 'Below Price', 'Golden Cross', 'Death Cross']; break;
            case '100MA': options = ['Above Price', 'Below Price']; break;
            case '50MA': options = ['Above Price', 'Below Price']; break;
            case 'Bollinger Band': options = ['Reach Top', 'Reach Bottom']; break;
            // Additional indicators and their actions can be added here
        }

        options.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option;
            opt.textContent = option;
            actionSelector.appendChild(opt);
        });
    }

    // Ensure an indicator can't be selected more than once across all dropdowns
    function updateDisableStateForIndicatorOptions() {
        const allSelectors = ['indicator1', 'indicator2', 'indicator3'];
        const selectedValues = allSelectors.map(id => document.getElementById(id).value);

        allSelectors.forEach(selectorId => {
            const selector = document.getElementById(selectorId);
            Array.from(selector.options).forEach(option => {
                option.disabled = selectedValues.includes(option.value) && option.value !== selector.value;
            });
        });
    }

    // Setup each indicator-action pair
    updateActionOptions('indicator1', 'indicator4');
    updateActionOptions('indicator2', 'indicator5');
    updateActionOptions('indicator3', 'indicator6');

    // Correctly set the disable state on page load
    updateDisableStateForIndicatorOptions();

    // Save the user's selections when the "Place Order" button is clicked
    document.getElementById('place-order').addEventListener('click', function() {
        console.log("User Selections:", userSelections);
        displayUserSelections(userSelections);
    });

    // Display the user's selections in a specific element
    function displayUserSelections(selections) {
        const statusDiv = document.getElementById('statusDiv');
        statusDiv.innerHTML = ''; // Clear previous entries
        Object.keys(selections).forEach(key => {
            const {indicator, action} = selections[key];
            const content = document.createElement('p');
            content.textContent = `Indicator: ${indicator}, Action: ${action}`;
            statusDiv.appendChild(content);
        });
    }
});
