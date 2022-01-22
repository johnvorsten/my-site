// Imports

// Variable declaration
const add_instance_elements = document.getElementsByClassName("add_instance");
let remove_instance_elements = document.getElementsByClassName("remove_instance");
const run_prediction_element = document.getElementById("run_prediction");
const PREDICTOR_ORIGIN = 'https://johnvorsten.me/mil-prediction'; // TODO Change for prod, should be https://johnvorsten.me/mil-prediction
const STATIC_SERVE_ORIGIN = 'https://johnvorsten.me/static-serve'; // TODO Change for prod, should be https://johnvorste.me/static-serve
const URL_MAP = new Map([
    ['CompNB',`${PREDICTOR_ORIGIN}/CompNBPredictor/`],
    ['MultiNB',`${PREDICTOR_ORIGIN}/MultiNBPredictor/`],
    ['SVMCL1SI',`${PREDICTOR_ORIGIN}/SVMCL1SIPredictor/`],
    ['SVMCRBFSI',`${PREDICTOR_ORIGIN}/SVMCRBFSIPredictor/`],
    ['SVMCL1MILES',`${PREDICTOR_ORIGIN}/SVMCL1MILESPredictor/`],
    ['SVMCRBFMILES',`${PREDICTOR_ORIGIN}/SVMCRBFMILESPredictor/`],
    ['TemplateJSON', `${STATIC_SERVE_ORIGIN}/projects/TemplateJSON.json`],
]);
const fill_template_instances = document.getElementById("fill_template_instances");
input_map = new Map([['on',true],['off',false],["",0],[]]);

// Events
for (const ele of add_instance_elements) {
    ele.addEventListener('click', add_instance);
}
for (const ele of remove_instance_elements) {
    ele.addEventListener('click', remove_instance);
}
run_prediction_element.addEventListener('click', run_prediction);
fill_template_instances.addEventListener('click', fill_table);
window.onload = function() {
    // Add two instances from the template
    add_instance(null);
    add_instance(null);

    // Load static JSON template data
    // Asyncronously request static JSON file from server
    // Load file into JSON object and assign to global variable
    // When this function is called, the global data will be added to the table
    fetch(URL_MAP.get('TemplateJSON'), {
        method:'GET', 
        mode: 'cors', 
        cache:'default',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
    })
    .then(response => {
        return response.json()
        .then(data => {
            window.TEMPLATE_INSTANCES = data;
        });
    })
    .catch(response => {
        console.log("Template instances not available");
    });
}

// functions
function add_instance(event, instance_data = null) {
    // Append an instance onto the instance_table element
    // Find table element
    const table = document.querySelector("tbody")

    // Retrieve templated table row / instance
    const row_template = document.getElementById("instance_template")
    var clone = row_template.content.cloneNode(true);
    // Event listners
    remove_instance_element = clone.querySelector(".remove_instance");
    remove_instance_element.addEventListener('click', remove_instance);
    TYPE_instance_element = clone.querySelector(".TYPE");
    TYPE_instance_element.addEventListener('input', disable_on_TYPE);

    // Append data if passed
    if (instance_data) {
        clone.querySelector(".NAME").value = instance_data.NAME
        clone.querySelector(".DESCRIPTOR").value = instance_data.DESCRIPTOR
        clone.querySelector(".TYPE").value = instance_data.TYPE
        clone.querySelector(".DEVUNITS").value = instance_data.DEVUNITS
        clone.querySelector(".FUNCTION").value = instance_data.FUNCTION
        clone.querySelector(".CS").value = instance_data.CS
        clone.querySelector(".SENSORTYPE").value = instance_data.SENSORTYPE
        clone.querySelector(".NETDEVID").value = instance_data.NETDEVID
        clone.querySelector(".SYSTEM").value = instance_data.SYSTEM
        clone.querySelector(".DEVICEHI").value = instance_data.DEVICEHI
        clone.querySelector(".DEVICELO").value = instance_data.DEVICELO
        clone.querySelector(".SIGNALHI").value = instance_data.SIGNALHI
        clone.querySelector(".SIGNALLO").value = instance_data.SIGNALLO
        clone.querySelector(".SLOPE").value = instance_data.SLOPE
        clone.querySelector(".INTERCEPT").value = instance_data.INTERCEPT
        clone.querySelector(".VIRTUAL").value = instance_data.VIRTUAL
        clone.querySelector(".TYPE").dispatchEvent(new Event('input'));
    }

    // Append cloned row
    table.append(clone)
}
function remove_instance(event) {
    // Find element ID and remove row
    let row = event.currentTarget.closest("tr");
    // Remove element
    row.remove();
}
function disable_on_TYPE(event) {
    let row = event.currentTarget.closest("tr");
    let type = event.currentTarget.closest(".TYPE").value;
    if (type == "LDI" || type == "LDO" || type == "L2SL") {
        row.querySelector(".SENSORTYPE").disabled = true;
        row.querySelector(".DEVICEHI").disabled = true;
        row.querySelector(".DEVICELO").disabled = true;
        row.querySelector(".SIGNALHI").disabled = true;
        row.querySelector(".SIGNALLO").disabled = true;
        row.querySelector(".SLOPE").disabled = true;
        row.querySelector(".INTERCEPT").disabled = true;
    }
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
        cache:'no-store',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        body: instances_json,
    })
    .then(response => update_prediction_text(response))
    .catch(response => update_prediction_text(response));

}
function update_prediction_text(response) {
    // Change text in prediction_result
    const run_prediction_element = document.getElementById("prediction_result");
    if (response.status == 200) {
        run_prediction_element.textContent = response.prediction;
    }
    else {
        run_prediction_element.textContent = "Error: " + response.status;
    }
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
        "DESCRIPTOR":"",
        "TYPE":"LDI",
        "DEVUNITS":"",
        "FUNCTION":"Value",
        "CS":"",
        "SENSORTYPE":"VOLTAGE",
        "ALARMTYPE":"Standard",
        "NETDEVID":"",
        "SYSTEM":"",
        // Float / number
        "DEVICEHI":0,
        "DEVICELO":0,
        "SIGNALHI":0,
        "SIGNALLO":0,
        "SLOPE":0,
        "INTERCEPT":0,
        // Boolean
        "VIRTUAL":false,
    }
    
    template.ALARMTYPE = element.querySelector(".ALARMTYPE").value;
    template.NAME = element.querySelector(".NAME").value;
    template.DESCRIPTOR = element.querySelector(".DESCRIPTOR").value;
    template.TYPE = element.querySelector(".TYPE").value;
    template.DEVUNITS = element.querySelector(".DEVUNITS").value;
    if (element.querySelector(".FUNCTION").value != "") {
        template.FUNCTION = element.querySelector(".FUNCTION").value;
    }
    template.CS = element.querySelector(".CS").value;
    if (element.querySelector(".SENSORTYPE").value != "") {
        template.SENSORTYPE = element.querySelector(".SENSORTYPE").value;
    }
    template.NETDEVID = element.querySelector(".NETDEVID").value;
    template.SYSTEM = element.querySelector(".SYSTEM").value;
    if (element.querySelector(".DEVICEHI").value != "") {
        template.DEVICEHI = element.querySelector(".DEVICEHI").value;
    }
    if (element.querySelector(".DEVICELO").value != "") {
        template.DEVICELO = element.querySelector(".DEVICELO").value;
    }
    if (element.querySelector(".SIGNALHI").value != "") {
        template.SIGNALHI = element.querySelector(".SIGNALHI").value;
    }
    if (element.querySelector(".SIGNALLO").value != "") {
        template.SIGNALLO = element.querySelector(".SIGNALLO").value;
    }
    if (element.querySelector(".SLOPE").value != "") {
        template.SLOPE = element.querySelector(".SLOPE").value;
    }
    if (element.querySelector(".INTERCEPT").value != "") {
        template.INTERCEPT = element.querySelector(".INTERCEPT").value;
    }
    template.VIRTUAL = element.querySelector(".VIRTUAL").checked;

    return template;
}
function fill_table(event) {
    // Remove all existing rows from table
    let rows = document.querySelectorAll("tbody > tr");
    for (let i=0; i<rows.length; i++) {
        rows[i].remove();
    }

    // For each instances in the instances list, create a clone and append it to the table
    for (let i=0; i<window.TEMPLATE_INSTANCES.length; i++) {
        add_instance(null, window.TEMPLATE_INSTANCES[i]);
    }
}