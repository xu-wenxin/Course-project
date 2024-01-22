var express = require('express');
var pg = require('pg');
var geoJSON = require('express').Router();
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

// test the code is working
geoJSON.route('/textGeoJSON').get(function(req,res){
    res.json({message:req.originalUrl});
});

// export function of geoJSON route
module.exports = geoJSON;


// // create api sub-route
// // return to data in table
// geoJSON.get('/postgistest',function(req,res){
//     pool.connect(function(err,client,down){
//         if(err){
//             console.log('not able to get connection '+err);
//             res.status(400).send(err);
//         }
//         // SQL language
//         client.query('select * from information_schema.columns',function(err,result){
//             down();
//             if(err){
//                 console.log(err);
//                 res.status(400).send(err);
//             }
//             // return data in row
//             res.status(200).send(result.rows);
//         });
//     });
// });


// // get sensors point from postgis
// geoJSON.get('/getSensors',function(req,res){
//     // connect to postgis pool
//     pool.connect(function(err,client,down){
//         if(err){    // connection error
//             console.log('not able to get connection '+err);
//             res.status(400).send(err);
//         }

//         // SQL language
//         var querystring = " SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM ";
//         querystring = querystring + "(SELECT 'Feature' As type , ST_AsGeoJSON(st_transform(lg.location,4326))::json As geometry, ";
//         querystring = querystring + "row_to_json((SELECT l FROM (SELECT sensor_id, sensor_name, sensor_make, sensor_installation_date, room_id) As l)) As properties";
//         querystring = querystring + " FROM ucfscde.temperature_sensors As lg limit 100 ) As f";

//         client.query(querystring,function(err,result){
//             down();
//             if(err){
//                 console.log(err);
//                 res.status(400).send(err);
//             }
//             // return data in row
//             res.status(200).send(result.rows);
//         });
//     });
// });


// // get geomcolumn with various parameters in postgis
// geoJSON.get('/getGeoJSON/:schemaname/:tablename/:idcolumn/:geomcolumn',function(req,res){
//     pool.connect(function(err,client,down){
//         if(err){
//             console.log('not able to get connection '+err);
//             res.status(400).send(err);
//         }

//         // SQL language
//         var colnames = "";
//         var tablename = req.params.tablename;  //get tablename
//         var schema = req.params.schemaname;
//         var idcolumn = req.params.idcolumn;
//         var geomcolumn = req.params.geomcolumn;
//         // convert geomcolumn to json format
//         var geomcolumnJSON = JSON.stringify(geomcolumn);
//         var tablenameJSON = schema+'.'+tablename;

//         // qurety language
//         var querystring = "select string_agg(colname,',') from ( select column_name as colname ";
//         querystring = querystring + " FROM information_schema.columns as colname ";
//         querystring = querystring + " where table_name =$1";
//         querystring = querystring + " and column_name <> $2 and table_schema = $3 and data_type <> 'USER-DEFINED') as cols ";

//         // return query
//         client.query(querystring,[tablename,geomcolumn,schema],function(err,result){
//             if(err){
//                 console.log(err);
//                 res.status(400).send(err);
//             }
//             // return colnames
//             thecolnames = result.rows[0].string_agg;
//             colnames = thecolnames;
//             console.log('the colnames '+thecolnames);

//             // check id exists
//             if (thecolnames.toLowerCase().indexOf(idcolumn.toLowerCase())>-1){
//                 var cols =colnames.split(',');
//                 var colString='';
//                 for (var i=0;i<cols.length;i++){
//                     console.log(cols[i]);
//                     colString=colString+JSON.stringify(cols[i])+',';
//                 }
//                 console.log(colString);

//                 // remove extra comma 
//                 colString = colString.substring(0,colString.length -1);

//                 // geoJSON format query
//                 querystring = "SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM "; 
//                 querystring += "(select 'Feature' as type, x.properties,st_asgeojson(y.geometry)::json as geometry from "; 
//                 querystring +=" (select "+idcolumn+", row_to_json((SELECT l FROM (SELECT "+colString + ") As l )) as properties FROM "+schema+"."+JSON.stringify(tablename); 
//                 querystring += " ) x"; 
//                 querystring +=" inner join (SELECT "+idcolumn+", c.geom as geometry"; 
//                 querystring +=" FROM ( SELECT "+idcolumn+", (ST_Dump(st_transform("+geomcolumn+",4326))).geom AS geom "; 
//                 querystring +=" FROM "+schema+"."+JSON.stringify(tablename)+") c) y on y."+idcolumn+" = x."+idcolumn+") f";
//                 console.log(querystring);

//                 // return query
//                 client.query(querystring,function(err,result){
//                     if(err){
//                         console.log(err);
//                         res.status(400).send(err);
//                     }
//                     // remove extra[]
//                     var geoJSONData = JSON.stringify(result.rows);
//                     geoJSONData = geoJSONData.substring(1);
//                     geoJSONData = geoJSONData.substring(0,geoJSONData.length-1);
//                     console.log(geoJSONData);
//                     res.status(200).send(JSON.parse(geoJSONData));
//                 });
//             }
//             else{
//                 res.status(400).send('invalid id column name');
//             }
//         });
//     });
// });




// get assert location for specific user_id
geoJSON.get('/geoJSONUserId/:user_id',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }
           
        var colnames = "asset_id, asset_name, installation_date, latest_condition_report_date, condition_description";
        var user_id = req.params.user_id;
        // note that query needs to be a single string with no line breaks so built it up bit by bit
        var querystring = " SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features  FROM ";
        querystring += "(SELECT 'Feature' As type     , ST_AsGeoJSON(lg.location)::json As geometry, ";
        querystring += "row_to_json((SELECT l FROM (SELECT "+colnames + " ) As l      )) As properties ";
        querystring += "   FROM cege0043.asset_with_latest_condition As lg ";
        querystring += " where user_id = $1 limit 100  ) As f ";

        client.query(querystring,[user_id],function(err,result){
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


// advanced functionality 1
// condition report
geoJSON.get('/userConditionReports/:user_id',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }
           
        var user_id = req.params.user_id;
        // note that query needs to be a single string with no line breaks so built it up bit by bit
        var querystring = "select array_to_json (array_agg(c)) from ";
        querystring += "(SELECT COUNT(*) AS num_reports from cege0043.asset_condition_information where user_id = $1) c ";

        client.query(querystring,[user_id],function(err,result){
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

// rank of condition report
geoJSON.get('/userRanking/:user_id',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }
           
        var user_id = req.params.user_id;
        // note that query needs to be a single string with no line breaks so built it up bit by bit
        var querystring = "select array_to_json (array_agg(hh)) from ";
        querystring += "(select c.rank from (SELECT b.user_id, rank()over (order by num_reports desc) as rank ";
        querystring += "from (select COUNT(*) AS num_reports, user_id ";
        querystring += "from cege0043.asset_condition_information ";
        querystring += "group by user_id) b) c ";
        querystring += "where c.user_id = $1) hh ";

        client.query(querystring,[user_id],function(err,result){
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



// for Advanced Functionality 2
// Asset Location App
// list of all the assets with at least one report saying that they are in the best condition  (via a menu option) 
geoJSON.get('/assetsInGreatCondition',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }
           
        var querystring = "select array_to_json (array_agg(d)) from ";
        querystring += "(select c.* from cege0043.asset_information c inner join ";
        querystring += "(select count(*) as best_condition, asset_id from cege0043.asset_condition_information where ";
        querystring += "condition_id in (select id from cege0043.asset_condition_options where condition_description like '%very good%') ";
        querystring += "group by asset_id ";
        querystring += "order by best_condition desc) b ";
        querystring += "on b.asset_id = c.id) d " ;

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


// Asset App
geoJSON.get('/dailyParticipationRates',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }
           
        var querystring = "select  array_to_json (array_agg(c)) from ";
        querystring += "(select day, sum(reports_submitted) as reports_submitted, sum(not_working) as reports_not_working ";
        querystring += "from cege0043.report_summary ";
        querystring += "group by day) c ";

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

geoJSON.get('/assetsAddedWithinLastWeek',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }
           
        var querystring = "SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features  FROM ";
        querystring += "(SELECT 'Feature' As type , ST_AsGeoJSON(lg.location)::json As geometry, ";
        querystring += "row_to_json((SELECT l FROM (SELECT id, asset_name, installation_date) As l ";
        querystring += " )) As properties ";
        querystring += "FROM cege0043.asset_information  As lg ";
        querystring += "where timestamp > NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7  limit 100  ) As f ";

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


// 1111111111111111111111111111111111111111111111111
// problem
// Condition App
geoJSON.get('/fiveClosestAssets/:latitude/:longitude',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }
           
        var longitude = req.params.longitude;
        var latitude = req.params.latitude;

        var querystring = "SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM ";
        querystring += "(SELECT 'Feature' As type     , ST_AsGeoJSON(lg.location)::json As geometry, ";
        querystring += "row_to_json((SELECT l FROM (SELECT id, asset_name, installation_date) As l ";
        querystring += " )) As properties ";
        querystring += " FROM   (select c.* from cege0043.asset_information c ";
        querystring += "inner join (select id, st_distance(a.location, st_geomfromtext('POINT("+longitude+" "+latitude+")',4326)) as distance ";
        querystring += "from cege0043.asset_information a ";
        querystring += "order by distance asc ";
        querystring += "limit 5) b ";
        querystring += "on c.id = b.id ) as lg) As f ";

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

geoJSON.get('/lastFiveConditionReports/:user_id',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }
           
        var user_id = req.params.user_id;

        var querystring = "SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features  FROM ";
        querystring += "(SELECT 'Feature' As type , ST_AsGeoJSON(lg.location)::json As geometry, ";
        querystring += "row_to_json((SELECT l FROM (SELECT id,user_id, asset_name, condition_description) As l ";
        querystring += " )) As properties ";
        querystring += " FROM (select * from cege0043.condition_reports_with_text_descriptions ";
        querystring += "where user_id = $1 ";
        querystring += "order by timestamp desc ";
        querystring += "limit 5) as lg) As f ";

        client.query(querystring,[user_id],function(err,result){
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

// assets and calculates proximity alerts for assets that the user hasn’t already given a condition report for in the last 3 days
geoJSON.get('/conditionReportMissing/:user_id',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }
           
        var user_id = req.params.user_id;

        var querystring = "SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features  FROM ";
        querystring += "(SELECT 'Feature' As type, ST_AsGeoJSON(lg.location)::json As geometry,  ";
        querystring += "row_to_json((SELECT l FROM (SELECT asset_id, asset_name, installation_date, latest_condition_report_date, condition_description) As l  ";
        querystring += " )) As properties ";
        querystring += "FROM (select * from cege0043.asset_with_latest_condition ";
        querystring += "where asset_id not in ( ";
        querystring += "select asset_id from cege0043.asset_condition_information ";
        querystring += "where user_id = $1 and  ";
        querystring += "timestamp > NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-3) ) as lg) As f";

        client.query(querystring,[user_id],function(err,result){
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

// assets and calculates proximity alerts for assets that the user hasn’t already given a condition report for in the last 3 days
geoJSON.get('/topFiveScorers',function(req,res){
    pool.connect(function(err,client,done){
        if(err){
            console.log('not able to get connection '+err);
            res.status(400).send(err);
        }

        var querystring = "select array_to_json (array_agg(c)) from  ";
        querystring += "(select rank() over (order by num_reports desc) as rank , user_id ";
        querystring += "from (select COUNT(*) AS num_reports, user_id ";
        querystring += "from cege0043.asset_condition_information ";
        querystring += "group by user_id) b limit 5) c ";

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


