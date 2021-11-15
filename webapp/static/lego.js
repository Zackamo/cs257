/* lego.js
*  Zack Johnson and Amir Al-Sheikh
*  November 9, 2021
*
* Based on a template by Jeff Ondich
*/

window.onload = initialize;

function initialize() {
  let sets_search = document.getElementById('sets_search');
  if (sets_search) {
    sets_search.onchange = searchSetsWithParameters;
  }
  let figsSearch = document.getElementById("minifigs_search");
  if (figsSearch){
    figsSearch.onchange = searchFigsWithParameters;
  }
  let setsByTheme = document.getElementById("sets_by_theme");
  if (setsByTheme){
    setsByTheme.onchange = searchSetsWithParameters;
  }

  let order = document.getElementById("order");
  let sort_by = document.getElementById("sort_by");

 //pre-populate a query based on the page
  let path = window.location.pathname;
  let page = path.split("/").pop();
  switch (page) {
    case "sets":
      if (sort_by) {
          sort_by.onchange = searchSetsWithParameters;
      }
      if (order) {
          order.onchange = searchSetsWithParameters;
      }
      setupSetsFilters();
      searchSets();
      break;
    case "minifigs":
      if (sort_by) {
          sort_by.onchange = searchFigsWithParameters;
      }
      if (order) {
          order.onchange = searchFigsWithParameters;
      }
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

function setupSetsFilters(){
  let theme_options = {158:"Star Wars", 494:"Friends", 324:"Bionicle", 435:"Ninjago",
  1:"Technic", 22:"Creator", 504:"Duplo", 246:"Harry Potter", 610:"Brickheadz", 605:"Nexo Knights",
  571:"Legends of Chima", 690:"Super Mario", 577:"Minecraft", 579:"Disney Princess",
  621:"Classic", 696:"Super Heroes Marvel", 602:"Jurassic World", 601:"Speed Champions",
  713:"VIDIYO", 599:"LEGO Exclusive", 576:"LEGO Ideas", 252:"Architecture",
  695:"Super Heroes DC", 578:"The LEGO Movie"};

  let selectBody = '<option value="" selected disabled hidden>Choose</option>';
  for (const key in theme_options){
    selectBody += "<option value='" + key + "'>" + theme_options[key] + "</option>"
  }
  select = document.getElementById("sets_by_theme");
  select.innerHTML = selectBody;
}

function searchSetsWithParameters(){
  let parameters = {};
  let sets_search = document.getElementById('sets_search');
  if (sets_search) {
      parameters = Object.assign(parameters, {search_for:sets_search.value})
  }
  let sortBy = document.getElementById('sort_by');
  if(sortBy){
    parameters = Object.assign(parameters, {sort_by:sortBy.value})
  }
  let order = document.getElementById('order');
  if(order){
    parameters = Object.assign(parameters, {order:order.value})
  }
  let theme = document.getElementById('sets_by_theme');
  if(theme){
    parameters = Object.assign(parameters, {theme:theme.value})
  }

  searchSets(parameters);
}

function searchSets(args={}){
  let url = getAPIBaseURL() + "/sets";
  if (Object.keys(args).length > 0){
    url += "?" + new URLSearchParams(args);
  }
  fetch(url, {method: 'get'})
  .then((response) => response.json())
  .then(function(sets) {
    let tableBody = '';
    for (let k = 0; k < sets.length; k++){
      let set = sets[k];
      tableBody += "<tr><td>" + set['set_num'] + "</td>";
      tableBody += "<td>" + set['name'] + "</td>";
      tableBody += "<td>" + set['theme'] + "</td>";
      tableBody += "<td class='num'>" + set['num_parts'] + "</td>";
      tableBody += "<td class='num'>" + set['num_figs'] + "</td>";
      tableBody += "<td class'num'>" + set['year'] + "</td></tr>";
    }
    let table = document.getElementById('results_table');
    if (table) {
        table.innerHTML = tableBody;
    }
    table = document.getElementById("table");
    tableContents = table.innerHTML;
    table.innerHTML = tableContents;
  })
  .catch(function(error) {
      console.log(error);
    });
}

function searchFigsWithParameters(){
  let parameters = {};
  let figs_search = document.getElementById('minifigs_search');
  if (figs_search) {
      parameters = Object.assign(parameters, {search_for:figs_search.value})
  }
  let sortBy = document.getElementById('sort_by');
  if(sortBy){
    parameters = Object.assign(parameters, {sort_by:sortBy.value})
  }
  let order = document.getElementById('order');
  if(order){
    parameters = Object.assign(parameters, {order:order.value})
  }
  searchMinifigs(parameters);
}

function searchMinifigs(args={}){
  let url = getAPIBaseURL() + "/minifigs";
  if (Object.keys(args).length > 0){
    url += "?" + new URLSearchParams(args);
  }

  fetch(url, {method: 'get'})
  .then((response) => response.json())
  .then(function(figs) {
    let tableBody = '';
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
    table = document.getElementById("table");
    tableContents = table.innerHTML;
    table.innerHTML = tableContents;
  })
  .catch(function(error) {
      console.log(error);
    });
}
