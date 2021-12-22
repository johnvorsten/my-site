// Imports

// Variable declaration
const add_instance_elements = document.getElementsByClassName("add_instance");
let remove_instance_elements = document.getElementsByClassName("remove_instance");
const run_prediction_element = document.getElementById("run_prediction");

// Events
for (const ele of add_instance_elements) {
    ele.addEventListener('click', add_instance);
}
for (const ele of remove_instance_elements) {
    ele.addEventListener('click', remove_instance);
}
run_prediction_element.addEventListener('click', run_prediction);

// functions
function add_instance() {
    console.log("Adding instance");
}

function remove_instance() {
    // Find element ID
    // Remove element
    console.log("Removing instance");
}

function run_prediction() {
    // Run prediction API call
    // Validate data
    // Aggregate instances and format data
    // Call API
    let prediction = "Some text temporary"
    // Return result
    update_prediction_text(prediction);
}

function update_prediction_text(prediction) {
    // Change text in prediction_result
    const run_prediction_element = document.getElementById("prediction_result");
    run_prediction_element.textContent = prediction;
    // TODO remove
    console.log("Updated prediction");
}

function gather_instances() {
    // aggregate all instances with class 'tr' (table row) into a JSON string for use in API header
}