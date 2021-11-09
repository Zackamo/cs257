/* lego.js
*  Zack Johnson and Amir Al-Sheikh
*  November 9, 2021
*
* Based on a template by Jeff Ondich
*/

window.onload = initialize;

function initialize() {


  let basicButton = document.getElementById("basic_button");
  if (basicButton){
    basicButton.onclick = onBasicButtonClicked;
  }

}

// Returns the base URL of the API, onto which endpoint
// components can be appended.
function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}

function onBasicButtonClicked(){
  let url = getAPIBaseURL() + "/minifigs";

  // Send the request to the books API /authors/ endpoint
  fetch(url, {method: 'get'})

  // When the results come back, transform them from a JSON string into
  // a Javascript object (in this case, a list of author dictionaries).
  .then((response) => response.json())

  .then(function(figs) {
    let tableBody = '';
    tableBody += "<tr><th>Minifigure Name</th><th>Minifigure ID</th><th>Found in Set:</th></tr>";
    for (let k = 0; k < figs.length; k++){
      let fig = figs[k];
      tableBody += "<tr><td>" + fig['name'] + "</td>";
      tableBody += "<td>" + fig['fig_num'] + "</td>";
      tableBody += "<td>" + fig['set_name'] + "</td></tr>";
    }
    let table = document.getElementById('minifig_table');
    if (table) {
        table.innerHTML = tableBody;
    }
  })

  // Log the error if anything went wrong during the fetch.
  .catch(function(error) {
      console.log(error);
    });
}
