// express server from nodejs
var express = require('express');
var path = require("path"); 
var app = express(); 
var fs = require('fs');

// add http server
var http = require('http');
var https = require('https');

// link app with http server
var httpServer = http.createServer(app);

// listen port
httpServer.listen(4480);



app.get('/',function (req,res) { 
    res.send("hello world from the Data API"); 
});

// allow cross-origin queries when phonegap running
app.use(function(req,res,next){
    res.setHeader("Access-Control-Allow-Origin","*");
    res.setHeader("Access-Control-Allow-Headers","Origin,X-Requested-With,Content-Type,Accept");
    res.setHeader("Access-Control-Allow-Methods",'GET,PUT,POST,DELETE');
    next();
});

// // allow cross-origin queries when phonegap running
// app.use(function(req,res,next){
//     res.setHeader("Access-Control-Allow-Origin","*");
//     res.setHeader("Access-Control-Allow-Headers","X-Requested-With");
//     res.setHeader("Access-Control-Allow-Methods",'GET,PUT,POST,DELETE');
//     next();
// });

// log the requests on console
app.use(function (req, res, next) {
	var filename = path.basename(req.url);
	var extension = path.extname(filename);
	console.log("The file " + filename + " was requested.");
	next();
});


// load route of geoJSON
const geoJSON = require('./routes/geoJSON');
app.use('/', geoJSON);

// // allow cross-origin queries when phonegap running
// app.use(function(req,res,next){
//     res.setHeader("Access-Control-Allow-Origin","*");
//     res.setHeader("Access-Control-Allow-Headers","Origin,X-Requested-With,Content-Type,Accept");
//     res.setHeader("Access-Control-Allow-Methods",'GET,PUT,POST,DELETE');
//     next();
// });

// load route of crud
const crud = require('./routes/crud');
app.use('/', crud);