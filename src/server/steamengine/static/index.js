/**
 * Load the svg into #svg1
*/
var width = 800;
var height = 700;
var svg = d3.select("#svg1").append('svg')
  .attr('width', width)
  .attr('height', height);

/**
 * Add autocomplete to search bar
*/
getAllGames().then(games => games.map(game => game.name)).then(tags => {
  $(function() {
    $( "#Autocomplete1" ).autocomplete({
      source: tags
    });
  });
});

/**
 * Create a global variable to hold liked games
*/
var liked_games = [];

/**
 * Retrieves game information from the databse by Steam id
 * @param steam_id steam id of the entry to retrieve
 */
function getGameBySteamID(steam_id) {
  var url = "http://127.0.0.1:8000/query";
  var params = queryString([
    ["query-type", "get-game-by-steam-id"],
    ["steam-id", steam_id],
  ]);
  return fetchJSON(url + params).then(res => res.game);
}

/**
 * Retrieves game information from the databse by game name
 * @param name name of the entry to retrieve
 */
function getGameByName(name) {
  var url = "http://127.0.0.1:8000/query";
  var params = queryString([
    ["query-type", "get-game-by-name"],
    ["name", name]
  ]);
  return fetchJSON(url + params).then(res => res.game);
}

/**
 * Retrieves game recommendations from a list of steam ids
 * @param ids list of steam ids to base recommendations on
 * @param num number of recommendations to return
 * @param rec recommender system to use
 */
function getRecommendations(ids, num=10, rec=1) {
  var url = "http://127.0.0.1:8000/query";
  var attrs = [["query-type", "get-recommendations"], ["max", num], ["rec", rec]];
  if (!Array.isArray(ids)) ids = [ids];
  attrs = attrs.concat(ids.map(id => ["game-id", id]));
  var params = queryString(attrs);
  return fetchJSON(url + params).then(res => res.games);
}

/**
 * Retrieves game reviews from a steam ids
 * @param ids steam id to return reviews of
 */
function getReviews(id) {
  var url = "http://127.0.0.1:8000/query";
  var attrs = [["query-type", "get-reviews"], ["steam-id", id]];
  var params = queryString(attrs);
  return fetchJSON(url + params).then(res => res.review);
}

/**
 * Retrieves game tags for a steam id
 * @param id steam id for which to return tags
*/
function getTags(id, num=5) {
  var url = "http://127.0.0.1:8000/query";
  var attrs = [["query-type", "get-tags"], ["steam-id", id], ["max", num]];
  var params = queryString(attrs);
  return fetchJSON(url + params).then(res => res.tags);
}

/**
 * Retrieves a list of all known games
 */
function getAllGames() {
  var url = "http://127.0.0.1:8000/query";
  var attrs = [["query-type", "get-all-games"]];
  var params = queryString(attrs);
  return fetchJSON(url + params).then(res => res.games);
}

/**
 * Returns the json result of a GET Promise
 * @param url query url
 */
function fetchJSON(url) {
  return fetch(url).then(res => res.json());
}

/**
 * Generates a GET request string with the given arguments
 * @param args list with entries of the form (name, value), where name is a GET
               request argument name, and value is its value
 */
function queryString(args) {
  if (args.length == 0) return "";
  var first_arg = args[0];
  var first_string = "?" + first_arg[0] + "=" + first_arg[1];
  var last_args = args.slice(1);
  var last_string = last_args.map(p => "&" + p[0] + "=" + p[1]).join("");
  return first_string + last_string;
}

/**
  * Use the form data to access the game info by its name
*/
function processFormData() {
  svg.selectAll("*").remove();
  var name_element = document.getElementById("Autocomplete1");
  var name = name_element.value;
  //document.getElementById("#svg1").style.backgroundImage = "none";
  getGameByName(name).then(initializeUI);
}

function initializeUI(game) {
  processGame(game);
  var numRecsElement = document.getElementById("recnumber");
  var numRecs = numRecsElement.value;
  if (numRecs <= 0) {
    numRecs = 5;
  }
  getRecommendations(game.steam_id, numRecs, 2)
    .then(ids => Promise.all(ids.map(getGameBySteamID)))
    .then(recList => populateGraph(game, recList));
}

function processGame(game) {
  getTags(game['steam_id']).then(res => printTags(res));
  getReviews(game['steam_id']).then(res => printTopReview(res));
  printNamePrice(game);
}

function printNamePrice(game) {
  document.getElementById("title_id").innerHTML = "Title: " + game['name'];
  document.getElementById("price_id").innerHTML = "Price: $" + game['price'];
}

function printTags(tags) {
  document.getElementById("tag_id").innerHTML = "Tags:";
  if (tags == 0) {
    document.getElementById("tag_id").innerHTML += " Pending";
  }
  else {
    for (i in tags) {
      if (i < tags.length - 1) {
        document.getElementById("tag_id").innerHTML += " " + tags[i].trim() + ",";
      } else {
        document.getElementById("tag_id").innerHTML += " " + tags[i].trim();
      }
    }
  }
}

function printTopReview(review) {
  if (review == null | review == "\n") {
    document.getElementById("review_id").innerHTML = "Top Review: Pending";
  } else {
    document.getElementById("review_id").innerHTML = "Top Review: " + review;
  }
}

/**
  * Populate the network graph
  * @param input the id of the searched game
  * @param rec_list the ids returned form the recommendation algorithm
*/
function populateGraph(input, rec_list) {
  var links = [];
  for (game of rec_list) {
    if (game == null) continue;
    links.push({"source": input.name, "target": game.name});
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
      if (d.name == input.name) {
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
    getGameByName(d.name).then(processGame);
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

  };
  }

  function processLike() {
    var game_title = document.getElementById("title_id").textContent;
    if (game_title == "Title: ") {
      ;
    }
    else {
      getGameByName(game_title.replace("Title: ", "")).then(addLike);
    }
  }

  function addLike(game) {
    liked_games.push(game['steam_id']);
  }
