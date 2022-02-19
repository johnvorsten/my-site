// Imports

// Variable declaration
const run_prediction_element = document.getElementById("run_prediction");
const PREDICTOR_ORIGIN = 'https://johnvorsten.me/clustering-ranking/model4predict/';
const fill_template_instances = document.getElementById("fill_template_instances");

// Events
run_prediction_element.addEventListener('click', run_prediction);
fill_template_instances.addEventListener('click', fill_table);
window.onload = function() {
    // Add single instances to table
    add_instance(null);
}

// functions
function add_instance(event) {
    // Append an instance onto the instance_table element
    // Find table element
    const table = document.querySelector("tbody")

    // Retrieve templated table row / instance
    const row_template = document.getElementById("instance_template")
    var clone = row_template.content.cloneNode(true);
    // Event listners
    n_instance_element = clone.querySelector(".n_instance");
    n_instance_element.addEventListener('input', calculate_uniq_ratio);
    n_features_element = clone.querySelector(".n_features");
    n_features_element.addEventListener('input', calculate_uniq_ratio);
    clone.querySelector(".len_var").onchange = set_two_decimal_places;
    clone.querySelector(".uniq_ratio").onchange = set_two_decimal_places;
    clone.querySelector(".n_len1").onchange = set_two_decimal_places;
    clone.querySelector(".n_len2").onchange = set_two_decimal_places;
    clone.querySelector(".n_len3").onchange = set_two_decimal_places;
    clone.querySelector(".n_len4").onchange = set_two_decimal_places;
    clone.querySelector(".n_len5").onchange = set_two_decimal_places;
    clone.querySelector(".n_len6").onchange = set_two_decimal_places;
    clone.querySelector(".n_len7").onchange = set_two_decimal_places;


    // Append cloned row
    table.append(clone)
}
function set_two_decimal_places(event) {
    this.value = parseFloat(this.value).toFixed(2);
}
function calculate_uniq_ratio(event) {
    console.log(event);
    let row = event.currentTarget.closest("tr");
    let uniq_ratio_element = document.querySelector(".uniq_ratio");
    let n_instance = document.querySelector(".n_instance").value;
    let n_features = document.querySelector(".n_features").value;

    if (n_features == 0) {
        uniq_ratio_element.value = 0;
    }
    else {
        uniq_ratio_element.value = n_instance / n_features;
    }
}
function run_prediction() {
    // Run prediction API call
    // Aggregate instances and format data
    instances = gather_instances();
    instances_json = JSON.stringify(instances[0]);
    
    // Call API
    fetch(PREDICTOR_ORIGIN, {
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
    // .then(response => update_prediction_text(response))
    .then(response => {
        if (response.status !== 200) {
            throw new Error("Error:");
        }
        return response.json();
    })
    .then(json_body => update_prediction_text(json_body))
    .catch(error => {
        console.error("There has been an error", error);
        update_prediction_text({"prediction":"Error: " + error});
    });
}
function update_prediction_text(json_body) {
    // Change text in prediction_result
    const run_prediction_element = document.getElementById("prediction_result");
    run_prediction_element.textContent = JSON.stringify(json_body);
}
function gather_instances() {
    // aggregate all instances with class 'tr' (table row) into a JSON string for use in API POST
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
        // floats
        "n_instance":0.0,
        "n_features":0.0,
        "len_var":0.0,
        "uniq_ratio":0.0,
        "n_len1":0.0,
        "n_len2":0.0,
        "n_len3":0.0, 
        "n_len4":0.0, 
        "n_len5":0.0, 
        "n_len6":0.0, 
        "n_len7":0.0,
    }
    
    template.n_instance = element.querySelector(".n_instance").value;
    template.n_features = element.querySelector(".n_features").value;
    template.len_var = element.querySelector(".len_var").value;
    template.uniq_ratio = element.querySelector(".uniq_ratio").value;
    template.n_len1 = element.querySelector(".n_len1").value;
    template.n_len2 = element.querySelector(".n_len2").value;
    template.n_len3 = element.querySelector(".n_len3").value;
    template.n_len4 = element.querySelector(".n_len4").value;
    template.n_len5 = element.querySelector(".n_len5").value;
    template.n_len6 = element.querySelector(".n_len6").value;
    template.n_len7 = element.querySelector(".n_len7").value;

    return template;
}
function fill_table(event) {

    // Appropriate for each feature in the table
    let ranges = {
        // floats
        "n_instance": new Int16Array([0,4000]),
        "n_features": new Int16Array([0,10000]),
        "len_var": new Int16Array([0,1]),
        "uniq_ratio":null, //Calculated
        "n_len1": new Int16Array([0,1]),
        "n_len2": new Int16Array([0,1]),
        "n_len3": new Int16Array([0,1]), 
        "n_len4": new Int16Array([0,1]), 
        "n_len5": new Int16Array([0,1]), 
        "n_len6": new Int16Array([0,1]), 
        "n_len7": new Int16Array([0,1]),
    }
    
    // Generate random values within the ranges defined above
    const n_instance = document.querySelector(".n_instance");
    n_instance.value = Math.round(Math.random() * ranges.n_instance[1]);
    
    const n_features = document.querySelector(".n_features");
    n_features.value = Math.round(Math.random() * ranges.n_features[1]);
    
    const uniq_ratio = document.querySelector(".uniq_ratio");
    uniq_ratio.value = parseFloat((n_instance.value / n_features.value)).toFixed(2);

    // Number of tokenized text features
    // Sume of length ratios should equal 1. Scale random value by remaining possible proportion
    let remaining = 1.0;
    const n_len1 = document.querySelector(".n_len1");
    n_len1.value = parseFloat(Math.random()).toFixed(2); // Proportion of instances with 1-length feature
    remaining = remaining - n_len1.value; // Update remaining proportion
    const n_len2 = document.querySelector(".n_len2");
    n_len2.value = parseFloat(Math.random() * remaining).toFixed(2);
    remaining = remaining - n_len2.value;
    const n_len3 = document.querySelector(".n_len3");
    n_len3.value = parseFloat(Math.random() * remaining).toFixed(2);
    remaining = remaining - n_len3.value;
    const n_len4 = document.querySelector(".n_len4");
    n_len4.value = parseFloat(Math.random() * remaining).toFixed(2);
    remaining = remaining - n_len4.value;
    const n_len5 = document.querySelector(".n_len5");
    n_len5.value = parseFloat(Math.random() * remaining).toFixed(2);
    remaining = remaining - n_len5.value;
    const n_len6 = document.querySelector(".n_len6");
    n_len6.value = parseFloat(Math.random() * remaining).toFixed(2);
    remaining = remaining - n_len6.value;
    const n_len7 = document.querySelector(".n_len7");
    n_len7.value = parseFloat(remaining).toFixed(2);

    // Variance is the sum of squared deviations from the mean
    // Calculate mean token length
    const mean = ((n_len1.value * 1) + (n_len2.value * 2) + (n_len3.value * 3) + 
        (n_len4.value * 4) + (n_len5.value * 5) + (n_len6.value * 6) +
        (n_len7.value * 7)) / 7;
    // Calculate expected value of squared deviation from population mean
    const variance = (Math.pow(n_len1.value - mean, 2) +
        Math.pow(n_len2.value - mean, 2) + 
        Math.pow(n_len3.value - mean, 2) + 
        Math.pow(n_len4.value - mean, 2) + 
        Math.pow(n_len5.value - mean, 2) + 
        Math.pow(n_len6.value - mean, 2) + 
        Math.pow(n_len7.value - mean, 2)) / 7;

    const len_var = document.querySelector(".len_var");
    len_var.value = parseFloat(variance).toFixed(2);
}