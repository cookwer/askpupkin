var http = require("http");
var url = require("url");

var requests = [];
var currentProgress = 0;

function onRequest(request, response) {
	var path = url.parse(request.url).pathname;
	console.log("Request for " + path);

	switch (path)
	{
	case "/update/":	
		requests.push(response);
		console.log("Request added (" + requests.length + " total)");
		break;
	case "/":
		response.writeHead(200, {"Content-Type": "text/plain"});
		response.write("Hai from NodeJS!");
		response.end();
		break;
	}
}

http.createServer(onRequest).listen(8888);
console.log("Server has started.");

function onUpdate() {
	currentProgress = (currentProgress + 10) % 100;
	console.log("onUpdate called (with " + requests.length + " requests total)");

	for (var i = 0; i < requests.length; i++) {	
		var response = requests.pop();
		
		response.writeHead(200, {"Content-Type": "application/json"});
		response.write(currentProgress.toString());
		response.end();
	}
}

setInterval(onUpdate, 1000);