var express = require('express');
var http = require('http');

var bodyParser = require("body-parser");
var ws = require('ws');

var WebSocketServer = ws.Server;

var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true,
}));

var server = app.listen(1984, function(){
  console.log("HTTP Server listening");
});

var wss = new WebSocketServer({
  server: server,
});

app.post('/api_requests/', function(req, res) {
  var data = req.body;

  console.log("POST request for APIRequest | data: %s", JSON.stringify(data));

  if(typeof(data) == 'undefined') {
    res.send("No value provided");
    return;
  }

  wss.broadcast("api_requests", null, data);

  res.send("Success");
});

app.post('/channels/:id/', function(req, res) {
  var id = req.params.id;
  var data = req.body;

  var value = data.value;

  console.log("POST request for Channel | id: %s, data: %s", id, JSON.stringify(data));

  if(typeof(value) == 'undefined') {
    res.send("No value provided");
    return;
  }

  wss.broadcast("channels", id, value);

  res.send("Success");
});


function parseWSEndpoint(ws) {
  var path = ws['upgradeReq']['url'];
  var tokens = path.split('/');

  var name = tokens[1];
  var id = tokens[2];

  return {
    'name': name,
    'id': id,
  }
}

wss.broadcast = function broadcast(name, id, data) {
  console.log("Broadcasting %s to endpoint | name: %s, id: %s", data, name, id);

  wss.clients.forEach(function each(ws) {
    var endpoint = parseWSEndpoint(ws);

    var client_name = endpoint['name'];
    var client_id = endpoint['id'];

    console.log("Client endpoint | name: %s, id: %s", client_name, client_id);

    if(client_name == name) {
      if(id == null ){
        ws.send(JSON.stringify(data));
      } else if(client_id == id) {
        ws.send(data);
      }
    }
  });
};

wss.on('connection', function connection(ws) {
  var headers = ws['upgradeReq']['headers'];

  var public_key = headers['public_key'];
  var private_key = headers['private_key'];

  var host = headers['host'];

  console.log("Websocket client connected");
});