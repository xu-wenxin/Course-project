var express = require('express');
var pg = require('pg');
var crud = require('express').Router();
var fs = require('fs');

// get username
var os = require('os')
const userInfo = os.userInfo();
const username = userInfo.username;
console.log(username);

// login detail
var configtext = ""+fs.readFileSync("/home/"+username+"/certs/postGISConnection.js");

// configuration file format
var configarray = configtext.split(",");
var config = {};
for (var i = 0; i < configarray.length; i++) {
    var split = configarray[i].split(':');
    config[split[0].trim()] = split[1].trim();
}
var pool = new pg.Pool(config);
console.log(config);

// data parser
const bodyParser = require('body-parser');
crud.use(bodyParser.urlencoded({ extended: true }));


// test endpoint for get
crud.get('/testCRUD',function (req,res) {
    res.json({message:req.originalUrl+" " +"GET REQUEST"});
});

// test endpoint for post
crud.post('/testCRUD',function (req,res) {
    res.json({message:req.body});
});




// get user_id
crud.get('/getUserId',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }

        var querystring = "select user_id from ucfscde.users where user_name = current_user ";

        client.query(querystring,function(err,result){
            done();
            if(err){
                console.log(err);
                res.status(400).send(err);
            }
            // return data in row
            res.status(200).send(result.rows);
        });
    });
});

// insert functionality
crud.post('/insertAssetPoint',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log("not able to get connection "+ err);
            res.status(400).send(err);
        }

        // delete
        // res.json('inserted: \n'+ {message:req.body});

        var longitude = req.body.longitude;
        var latitude = req.body.latitude;
        var asset_name = req.body.asset_name;
        var installation_date = req.body.installation_date;

        console.log(longitude,latitude,asset_name,installation_date);


        var geometrystring = "st_geomfromtext('POINT("+req.body.longitude+ " "+req.body.latitude +")',4326) ";
        var querystring = "INSERT into cege0043.asset_information (asset_name,installation_date,location) values ";
        querystring += "($1,$2,";
        querystring += geometrystring + ")";

        client.query(querystring,[asset_name,installation_date],function(err,result){
            done();
            if(err){
                alert('asset name already exist, please insert again.\n',err);
                console.log('asset name already exist, please insert again.\n',err);
                res.status(400).send('asset name already exist, please insert again.\n'+err);
            }
            res.status(200).send("Asset "+ asset_name + " has been inserted");
        });
    });
});

// insert condition information
crud.post('/insertConditionInformation',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }

        var asset_name = req.body.asset_name;
        var condition_description = req.body.condition_description;

        var querystring = "INSERT into cege0043.asset_condition_information (asset_id, condition_id) values (";
        querystring += "(select id from cege0043.asset_information where asset_name = $1),(select id from cege0043.asset_condition_options where condition_description = $2))";    

        client.query(querystring,[asset_name,condition_description],function(err,result){
            done();
            if(err){
                console.log(err);
                res.status(400).send(err);
            }
            // return data in row
            // res.json('inserted: \n'+ {message:req.body});
            res.status(200).send('the condition of '+asset_name+' have been saved');
        });
    });
});

crud.post('/deleteAsset',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }

        var id = req.body.id;
        var querystring = "DELETE from cege0043.asset_information where id = $1";

        client.query(querystring,[id],function(err,result){
            done();
            if(err){
                console.log(err);
                res.status(400).send(err);
            }
            // return data in row
            // res.json('inserted: \n'+ {message:req.body});
            res.status(200).send('asset has been deleted');
        });
    });
});

crud.post('/deleteConditionReport',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }

        var id = req.body.id;
        var querystring = "DELETE from cege0043.asset_condition_information where id = $1";

        client.query(querystring,[id],function(err,result){
            done();
            if(err){
                console.log(err);
                res.status(400).send(err);
            }
            // return data in row
            // res.json('inserted: \n'+ {message:req.body});
            res.status(200).send('delte condition report');
        });
    });
});




module.exports = crud;