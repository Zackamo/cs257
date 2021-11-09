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
  let sort_by = document.getElementById('sort_by');
  if (sort_by) {
      sort_by.onchange = onSortChange;
  }
  let order = document.getElementById('order');
  if (order) {
      order.onchange = onSortChange;
  }
 //pre-populate a query based on the page
  let path = window.location.pathname;
  let page = path.split("/").pop();
  switch (page) {
    case "sets":
      searchSets();
      break;
    case "minifigs":
      searchMinifigs();
      break;
    default:

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
    tableBody += "<tr><th>Minifigure Name</th><th>Minifigure ID</th><th>Comes In:</th></tr>";
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

function searchSets(){
  let url = getAPIBaseURL() + "/sets";

  fetch(url, {method: 'get'})
  .then((response) => response.json())
  .then(function(figs) {
    let tableBody = '';
    tableBody += "<tr><th>Set Number</th><th>Name</th><th>Theme</th><th>Parts</th><th>Minifigures</th><th>Year</th></tr>";
    for (let k = 0; k < figs.length; k++){
      let fig = figs[k];
      tableBody += "<tr><td>" + fig['set_num'] + "</td>";
      tableBody += "<td>" + fig['name'] + "</td>";
      tableBody += "<td>" + fig['theme'] + "</td>";
      tableBody += "<td>" + fig['num_parts'] + "</td>";
      tableBody += "<td>" + fig['num_figs'] + "</td>";
      tableBody += "<td>" + fig['year'] + "</td></tr>";
    }
    let table = document.getElementById('results_table');
    if (table) {
        table.innerHTML = tableBody;
    }
  })
  .catch(function(error) {
      console.log(error);
    });
}

function searchMinifigs(){
  let url = getAPIBaseURL() + "/minifigs";

  fetch(url, {method: 'get'})
  .then((response) => response.json())
  .then(function(figs) {
    let tableBody = '';
    tableBody += "<tr><th>Minifigure Name</th><th>Minifigure ID</th><th>Parts</th><th>Found in Set:</th></tr>";
    for (let k = 0; k < figs.length; k++){
      let fig = figs[k];
      tableBody += "<tr><td>" + fig['name'] + "</td>";
      tableBody += "<td>" + fig['fig_num'] + "</td>";
      tableBody += "<td>" + fig['num_parts'] + "</td>";
      tableBody += "<td>" + fig['num_sets'] + "</td></tr>";
    }
    let table = document.getElementById('results_table');
    if (table) {
        table.innerHTML = tableBody;
    }
  })
  .catch(function(error) {
      console.log(error);
    });
}

function onSortChange(){
  sortBy = document.getElementById('sort_by').value;
  order = document.getElementById('order').value;
  sortTable(sortBy, order);
}

function sortTable(column, dir){
  let table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("resultsTable");
  switching = true;
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) { //row 0 is headers
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[column];
      y = rows[i + 1].getElementsByTagName("TD")[column];
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}
