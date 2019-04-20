/**
 * Load the svg into #svg1
*/
var width = 800;
var height = 700;
var svg = d3.select("#svg1").append('svg')
  .attr('width', width)
  .attr('height', height);

getGameBySteamID(10, res => console.log(res));
getGameByName("Counter-Strike", res => console.log(res));

/**
 * Retrieves game information from the databse by Steam id
 * @param id steam id of the entry to retrieve
 * @param callback the function to call with the response results
 */
function getGameBySteamID(steam_id, callback) {
  var url = "http://127.0.0.1:8000/query";
  var params = queryString({
    "query-type": "get-game-by-steam-id",
    "steam-id": steam_id
  });
  getCallback(url + params, res => callback(res.game))
}

/**
 * Retrieves game information from the databse by game name
 * @param name name of the entry to retrieve
 * @param callback the function to call with the response results
 */
function getGameByName(name, callback) {
  var url = "http://127.0.0.1:8000/query";
  var params = queryString({
    "query-type": "get-game-by-name",
    "name": name
  });
  getCallback(url + params, res => callback(res.game))
}

/**
 * Sends GET query and calls a callback function on response
 * @param url query url
 * @param callback the function to call with the response results
 */
function getCallback(url, callback) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = processRequest;

  function processRequest() {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      var response = JSON.parse(xhttp.response);
      callback(response);
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

/**
  * Use the form data to access the game info by its name
*/
function processFormData() {
  svg.selectAll("*").remove();
  var name_element = document.getElementById("Autocomplete1");
  var name = name_element.value;
  getGameByName(name, res => initializeUI(res));
}

function initializeUI(game) {
  processGame(game);
  var rec_number_element = document.getElementById("recnumber");
  var rec_number = rec_number_element.value;
  //getRecommendations(game_list = [game['steam_id']], num = rec_number, res => populateGraph(game['steam_id'], res));
  var ids = [289650,359550,230410,440];
  var input = game['steam_id']
  //populateGraph(input, ids);
  var holder = [];
  var counter = 0;
  getGameObjects(game, ids, holder, ids.length, counter);
}

function processGame(game) {
  printNamePrice(game);
  //getTags(game['steam_id'], res => printTags(res));
  //getTopReview(game['steam_id'], res => printTopReview(res));
}

function printNamePrice(game) {
  document.getElementById("title_id").innerHTML = "Title: " + game['name'];
  document.getElementById("price_id").innerHTML = "Price: $" + game['price'];
}

function printTags(tag_list) {
  document.getElementById("tag_id").innerHTML = "Tags: ";
  for (i in tags) {
    if (i < tags.length - 1) {
      document.getElementById("tag_id").innerHTML += " " + tags[i] + ",";
    } else {
      document.getElementById("tag_id").innerHTML += " " + tags[i];
    }
  }
}

function printTopReview(review) {
  document.getElementById("review_id").innerHTML = "Top Review: " + review;
}

function getGameObjects(game, rec_list, obj_list, length, counter) {
  console.log(obj_list);
  console.log(rec_list);
  if (counter == length) {
    populateGraph(game, obj_list);
  } else {
    console.log(rec_list[counter])
    getGameBySteamID(rec_list[counter], res => getGameObjects(game, rec_list, obj_list[counter] = res, length, counter + 1));
  }
}


///////////////////////////////
/**
  * Use the form data to access the game info by its name
*/
/**function processFormData() {
  var name_element = document.getElementById("Autocomplete1");
  var name = name_element.value;
  getGameByName(name, res => printNamePrice(res));
}*/

/**
  * Populate the Title and Price paragraphs and get the recommendations
  * @param game the Game object returned from getGameByName
*/
/**function printNamePrice(game) {
  document.getElementById("title_id").innerHTML = "Title: " + game['name'];
  document.getElementById("price_id").innerHTML = "Price: $" + game['price'];
  var rec_number_element = document.getElementById("recnumber");
  var rec_number = rec_number_element.value;
  //....., res => populateGraph(game['steam_id'], res));
  var source = game['steam_id'];
  var ids = [578080,289650,359550,230410,440];
  populateGraph(source, ids);
}*/

/**
  * Populate the network graph
  * @param input the id of the searched game
  * @param rec_list the ids returned form the recommendation algorithm
*/
function populateGraph(input, rec_list) {
  console.log(input, rec_list);
  /**var links = [];
  for (i in ids) {
    links.push({"source": input, "target": ids[i]});
  }

  var nodes = {};

  // Compute the distinct nodes from the links
  links.forEach(function(link) {
    link.source = nodes[link.source] ||
        (nodes[link.source] = {name: link.source});
    link.target = nodes[link.target] ||
        (nodes[link.target] = {name: link.target});
  });

  var force = d3.forceSimulation()
    .nodes(d3.values(nodes))
    .force("link", d3.forceLink(links).distance(100))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force("x", d3.forceX())
    .force("y", d3.forceY())
    .force("charge", d3.forceManyBody().strength(-750))
    .alphaTarget(1)
    .on("tick", tick);

  // add the links and the arrows
  var path = svg.append("g")
    .selectAll("path")
    .data(links)
    .enter()
    .append("path")
    .attr("class", function(d) { return "link " + d.type; });

  // define the nodes
  var node = svg.selectAll(".node")
    .data(force.nodes())
    .enter().append("g")
    .attr("class", "node")
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended)
      );

  // add the nodes
  node.append("circle")
    .attr("r", 35)
    .attr("class", function(d) {
      if (d.name == input) {
        return "source";
      } else {
        return "target";
      }
    });

  // Pin/Unpin nodes on double click
  node.on("dblclick", function(d) {
        if (d.fixed == true) {
            d.fixed = false;
            d.fx = null;
            d.fy = null;
        } else {
          d.fixed = true;
          d.fx = d.x;
          d.fy = d.y;
        }
    });

  // Show game information on click
  node.on("click", function(d) {
    getGameBySteamID(d.name, res => processGame(res));
  });

  // label the nodes
  var label = svg.selectAll("text")
   .data(force.nodes())
   .enter()
   .append("text")
   .text(function(d) {
      return d.name;
   })
   .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended)
   );

  // add the curvy lines
  function tick() {
    path.attr("d", function(d) {
        var dx = d.target.x - d.source.x,
            dy = d.target.y - d.source.y,
            dr = Math.sqrt(dx * dx + dy * dy);
        return "M" +
            d.source.x + "," +
            d.source.y + "A" +
            dr + "," + dr + " 0 0,1 " +
            d.target.x + "," +
            d.target.y;
    });

    node
        .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")"; })
    label
        .attr("transform", function(d) {
        return "translate(" + d.x + "," + (d.y + 35 + 5) + ")"; })
  };

  function dragstarted(d) {
      if (!d3.event.active) force.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    };

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  };

  function dragended(d) {
    if (!d3.event.active) force.alphaTarget(0);
    if (d.fixed == true){
      d.fx = d.x;
      d.fy = d.y;
    }
    else{
      d.fx = null;
      d.fy = null;
    }

  };*/
  }

