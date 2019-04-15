var width = 500;
var height = 500;
svg = d3.select("#svg-div").append("svg")
        .attr("width", width).attr("height", height);
svg.append("line")
   .attr("x1", 100)
   .attr("y1", 100)
   .attr("x2", 200) 
   .attr("y2", 200)
   .style("stroke", "rgb(255,0,0)")
   .style("stroke-width", 2);

/**
 * Retrieves game information from the databse by Steam id
 * @param id steam id of the entry to retrieve
 * @param callback the function to call with the response results
 */
function getGameBySteamID(steam_id, callback) {
  var xhttp = new XMLHttpRequest();
  var url = "http://127.0.0.1:8000/query";
  var params;
  params = queryString({
    "query-type": "get-game-by-steam-id",
    "steam-id": steam_id
  });
  url = url + params;
  xhttp.onreadystatechange = processRequest;

  function processRequest() {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      var response = JSON.parse(xhttp.response);
      callback(response.game);
    }
  }
  xhttp.open("GET", url, true);
  xhttp.send();
}

/**
 * Generates a GET request string with the given arguments
 * @param args dictionary with entries form name: value, where name is a GET
               request argument name, and value is its value
 */
function queryString(args) {
  var first = true;
  var str = "";
  for (var arg in args) {
    if (first) {
      first = false;
      str = str + "?" + arg + "=" + args[arg]
    } else {
      str = str + "&" + arg + "=" + args[arg]
    }
  }
  return str;
}