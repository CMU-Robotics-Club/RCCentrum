/*
 * Listens for POST requests on private API from Django application
 * for model changes and broadcasts that data to connected clients subscribed to 
 * the specific model and ID.  Check __init__.py for the list of model hooks
 * that POST to this server.  A websocket client can also connect to all requests originating
 * from a specific model or all requests regardless of which model it is coming from.
 * 
 * ex.)
 * ws://roboticsclub.org:1984/ -> all model updates
 * ws://roboticsclub.org:1984/channels/ -> all Channel model updates
 * ws://roboticsclub.org:1984/channels/1/ -> all Channel 1 model updates
 *
 */

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

/*
 * Listen for POST requests and broadcast model and ID
 * to websocket clients.
 */
app.post('*', function(req, res){
  var model = req.path.split('/')[1];

  var data = req.body;
  var id = data['id'];

  console.log("POST request | model: %s | id: %s | data: %s", model, id, JSON.stringify(data));

  wss.broadcast(model, id, data);

  res.send("Success");
});

/*
 * For a given websocket client returns a dictionary of the 'model' and 'id'
 * filter the client is interested in receiving.
 * If 'id' is null the client is interested in receiving all notifications
 * related to the specified 'model'.  If 'model' is null all notifications should
 * be sent to the client.
 */
function parseWSEndpoint(ws) {
  var path = ws['upgradeReq']['url'];
  var tokens = path.split('/');

  var model = tokens[1];
  var id = tokens[2];

  if(model == ''){
    model = null;
  }

  if(id == ''){
    id = null;
  }

  return {
    'model': model,
    'id': id,
  }
}

wss.broadcast = function broadcast(model, id, data) {
  wss.clients.forEach(function(ws) {
    var endpoint = parseWSEndpoint(ws);

    var client_model = endpoint['model'];
    var client_id = endpoint['id'];

    console.log("Client | model: %s | id: %s", client_model, client_id);

    if(client_model == null) {
      // Client receives all model push info
      ws.send(JSON.stringify(data));
    } else if(client_model == model) {
      // Client requests only specific model

      if(client_id == null){
        ws.send(JSON.stringify(data));
      } else if(client_id == id) {
        ws.send(JSON.stringify(data));
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
