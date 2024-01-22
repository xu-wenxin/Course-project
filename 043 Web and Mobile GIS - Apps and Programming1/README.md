# cege0043-apis

Basic starter code for UCL module CEGE0043 api development - includes a basic HTTP server to provide data to app web page. 


## Question Setting Api
This is a technical guide to API.<br>
The api allows the user to get and post data to remote postgis database.<br>

### 1 System Requirements
<p>
    The implementation of this API requires no additional browser requirements.
</p>
<p>
    External libraries used by the api include express and pg packgae which can find in our package file.
</p>
<p>
    This api requires a connection to an Ubuntu server (virtual machine). You can use BitVise, Pycharm (version 2018.3.5 Professional) or other SSH software to connect to the Ubuntu server.
</p>
<p>
    If you intend to use this application off the UCL campus (without a connection to Eduroam), make sure you follow the instructions at https://www.ucl.ac.uk/isd/services/get-connected/remote-working-services/ucl- instructions on virtualprivate-network-vpn to connect to the UCL VPN.
</p>

### 2 Procedures to deploy this app

<p>
1. Clone the source code of the corresponding Node JS server from Github to CEGE server
at  home/studentuser/code by typing in the command line (terminal) window for Ubuntu:
<br><br>

cd /home/studentuser/code<br>
https://github.com/ucl-geospatial-21-22/cege0043-api-21-22-xu-wenxin.git
</p>
<p>
2. install npm package for api.<br><br>
npm init<br>
npm install express --save<br>
npm install pg --save
</p>
<p>
4. Go to the cege0043-api-21-22-xu-wenxin folder and start the Node JS server.
<br><br>
cd /home/studentuser/code/cege0043-api-21-22-xu-wenxin<br>
node dataAPI.js 
</p>

### 3 testing api
1. Make sure your device is connected to UCL Wifi or UCL VPN。
<br><br>
2. Make sure the Node JS server is active.
<br><br>
3. When testing the functionality of this mapping, check the API for errors in the server's Terminal interface。
<br><br>
4. test end points.
<br>
For get end point, you can type url into a browser to check the data you get.
<br>
For post end point, you can adapt the ajax.html file from the week7-ajax example of CEGE 0043 Web Mobile and GIS, you can also type a string of name/value parameters into a second box and then send that to the API using a POST request, or you can also use postman application to test post request.


### 4 File description
<p>
The files associated with this app are located in the /home/studentuser/code/cege0043-app-21-22-xu-wenxin folder and several subfolders.
</p>
<p>

**(1) ~/**<br>
dataAPI.js<br>
api main entry point.
<br><br>

**(2) ~/routes**<br>
1) crud.js <br>
Endpoint to get user_id and post data to database.
<br><br>

|  endpoint   | description  |
|  ----  | :-----  |
| crud.get(/getUserId)  | Get the user_id of the user currently logged into postGIS on the api side. |
| crud.post(/insertAssetPoint)  | Create new asset information in dataset. |
| crud.post(/insertConditionInformation)  | Create new asset condition report into dataset. |
| crud.post(/deleteAsset)  | Delete asset in dataset. |
| crud.post(/deleteConditionReport)  | Delete asset condition report in dataset. |
<br><br>

2) geoJSON.js<br>
Endpoint to get geoJSON formate asset information based on different requeirment.
<br><br>

|  endpoint   | description  |
|  ----  | :-----  |
| geoJSON.get(/geoJSONUserId/:user_id)  | get only the geoJSON asset locations for a specific user_id. |
| geoJSON.get(/userConditionReports/:user_id)  | the number of condition reports user have saved. |
| geoJSON.get(/userRanking/:user_id)  | Get user rank based on condition reports, in comparison to all other users. |
| geoJSON.get(/assetsInGreatCondition)  | Get information of assets with at least one report saying that they are in the best condition. |
| geoJSON.get(/dailyParticipationRates)  | daily reporting about how many reports have been submitted and how many of these had condition as one of the two 'not working' options for the past week. |
| geoJSON.get(/assetsAddedWithinLastWeek)  | all the asset locations added in the last week. |
| geoJSON.get(/fiveClosestAssets/:latitude/:longitude)  | the 5 assets closest to the the location. |
| geoJSON.get(/lastFiveConditionReports/:user_id)  | the last 5 reports that the user created. |
| geoJSON.get(/conditionReportMissing/:user_id)  | assets that the user hasn’t already given a condition report for in the last 3 days. |
| geoJSON.get(/topFiveScorers)  | top 5 scorers in terms of the number of reports created. |

</p>

### 5 Code reference
<p>
A large proportion of codes are adapted from the lab notes of CEGE 0043 Web Mobile and GIS by Calire Ellul, including Basic structures of bootStrap.html and functions related to events detector, data downloading, data uploading, user location tracking, displaying map layers, d3 bar graph, and the 3D Cesium view in dashboard.html.
</p>





