// Load the AWS SDK for Node.js
var AWS = require('aws-sdk');

//update region
AWS.config.update({region:"us-east-2"});

// Create EC2 service object
var ec2 = new AWS.EC2({apiVersion: '2016-11-15'});

//Name of tag
var kubeClusterTag = "KubernetesCluster";
//Value of tag
var tagVal = "checkbox.ms.cluster.k8s.local";

var instanceArray = [];
getKubeInstances(instanceArray);
// printArr(instanceArray);

// function printArr(arr){
//   console.log("***Printing Array***");
//   for(var i = 0; i < arr.length; i++){
//     console.log(arr[i]);
//   }
// }

function getKubeInstances(instanceArray){
  var params = {
    Filters: [
       {
      Name: "tag:"+kubeClusterTag, 
      Values: [
         tagVal
      ]
     }
    ]
   };
   ec2.describeInstances(params, function(err, data) {
     if (err) console.log(err, err.stack); // an error occurred
     else{
       //console.log(data);
      for(var i = 0; i < data.Reservations.length; i++ ){
        for(var j = 0; j < data.Reservations[i].Instances.length; j++){
         // console.log(data.Reservations[i].Instances[j].InstanceId);
          instanceArray.push(data.Reservations[i].Instances[j].InstanceId);
          // printArr(instanceArray);
        }
        
      }
      terminateInstance(instanceArray);
     }
   });
}


function terminateInstance(instanceArray){
//Generate random number between 0-arr.length-1 both inclusive
var randomNum = Math.floor(Math.random() * instanceArray.length);
var params = {
  InstanceIds: [
     instanceArray[randomNum]
  ]
 };
 ec2.terminateInstances(params, function(err, data) {
   if (err) console.log(err, err.stack); // an error occurred
   else     console.log(data);           // successful response
 });
 }

