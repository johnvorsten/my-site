// Imports

// Variable declaration
const add_instance_elements = document.getElementsByClassName("add_instance");
let remove_instance_elements = document.getElementsByClassName("remove_instance");
const run_prediction_element = document.getElementById("run_prediction");
const PREDICTOR_ORIGIN = 'http://localhost:8000/mil-prediction';
const URL_MAP = new Map([
    ['CompNB',`${PREDICTOR_ORIGIN}/CompNBPredictor/`],
    ['MultiNB',`${PREDICTOR_ORIGIN}/MultiNBPredictor/`],
    ['SVMCL1SI',`${PREDICTOR_ORIGIN}/SVMCL1SIPredictor/`],
    ['SVMCRBFSI',`${PREDICTOR_ORIGIN}/SVMCRBFSIPredictor/`],
    ['SVMCL1MILES',`${PREDICTOR_ORIGIN}/SVMCL1MILESPredictor/`],
    ['SVMCRBFMILES',`${PREDICTOR_ORIGIN}/SVMCRBFMILESPredictor/`],
]);

// Events
for (const ele of add_instance_elements) {
    ele.addEventListener('click', add_instance);
}
for (const ele of remove_instance_elements) {
    ele.addEventListener('click', remove_instance);
}
run_prediction_element.addEventListener('click', run_prediction);
window.onload = function() {
    // Add two instances from the template
    add_instance();
    add_instance();
}

// functions
function add_instance() {
    // Append an instance onto the instance_table element
    // Find table element
    const table = document.querySelector("tbody")

    // Retrieve templated table row / instance
    const row_template = document.getElementById("instance_template")
    var clone = row_template.content.cloneNode(true);
    remove_instance_element = clone.querySelector(".remove_instance")
    remove_instance_element.addEventListener('click', remove_instance)

    // Append cloned row
    table.append(clone)
}
function remove_instance(event) {
    // Find element ID and remove row
    let row = event.currentTarget.closest("tr");
    // Remove element
    row.remove();
}
function run_prediction() {
    // Run prediction API call
    // Aggregate instances and format data
    instances = gather_instances();
    instances_json = JSON.stringify(instances);
    
    // Call API
    const predictor_type = document.querySelector(".predictor_type").value;
    fetch(URL_MAP.get(predictor_type), {
        method:'POST', 
        mode: 'cors', 
        cache:'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        body: instances_json,
    })
    .then(response => update_prediction_text(response.prediction))
    .catch(response => update_prediction_text("Error: " + response.status));

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
    let elements = document.querySelectorAll("tr");
    let instances = [];
    // Start at 1st instance (skip header)
    for (i = 1; i < elements.length; i++) {
        json_inst = parse_instance(elements[i]);
        instances.push(json_inst);
    }
    return instances;
}
function parse_instance(element) {
    // Input a single DOM table row, and for each column in the row
    // insert the row feature (column name) into a JSON object
    let template = {
        // Strings
        "NAME":null,
        "DESCRIPTOR":null,
        "TYPE":null,
        "DEVUNITS":null,
        "FUNCTION":null,
        "CS":null,
        "SENSORTYPE":null,
        "NETDEVID":null,
        "SYSTEM":null,
        // Float / number
        "DEVICEHI":null,
        "DEVICELO":null,
        "SIGNALHI":null,
        "SIGNALLO":null,
        "SLOPE":null,
        "INTERCEPT":null,
        // Boolean
        "VIRTUAL":false,
    }
    button_map = new Map([['on',true],['off',false]]);
    template.NAME = element.querySelector(".NAME").value;
    template.DESCRIPTOR = element.querySelector(".DESCRIPTOR").value;
    template.TYPE = element.querySelector(".TYPE").value;
    template.DEVUNITS = element.querySelector(".DEVUNITS").value;
    template.FUNCTION = element.querySelector(".FUNCTION").value;
    template.CS = element.querySelector(".CS").value;
    template.SENSORTYPE = element.querySelector(".SENSORTYPE").value;
    template.NETDEVID = element.querySelector(".NETDEVID").value;
    template.SYSTEM = element.querySelector(".SYSTEM").value;
    template.DEVICEHI = element.querySelector(".DEVICEHI").value;
    template.DEVICELO = element.querySelector(".DEVICELO").value;
    template.SIGNALHI = element.querySelector(".SIGNALHI").value;
    template.SIGNALLO = element.querySelector(".SIGNALLO").value;
    template.SLOPE = element.querySelector(".SLOPE").value;
    template.INTERCEPT = element.querySelector(".INTERCEPT").value;
    template.VIRTUAL = button_map.get(element.querySelector(".VIRTUAL").checked);

    return template;
}