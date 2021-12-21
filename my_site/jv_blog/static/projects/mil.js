// Imports

// Variable declaration
const add_instance_elements = document.getElementsByClassName("add_instance")
let remove_instance_elements = document.getElementsByClassName("remove_instance")
const prediction_result_element = document.getElementById("prediction_result")

// Main
for (const ele of add_instance_elements) {
    ele.addEventListener('click', add_instance)
}
add_instance_elements.addEventListener('click', add_instance)
for (const ele of remove_instance_elements) {
    ele.addEventListener('click', remove_instance)
}
prediction_result_element.addEventListener('click', update_prediction)

// functions
function add_instance() {

}

function remove_instance() {

}

function update_prediction() {
    alert("Updated prediction")
}
