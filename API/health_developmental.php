<?php

require_once __DIR__ . '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);

if(!empty($json['offender_id'])){
    $offender_id = $json['offender_id'];
    $health = $json['health'];
    $develop = $json['developmental'];

    if(addHealthData($con)){
        if(addDevelopmentalData($con)){
            $response['success'] = 1;
            $response['message'] = 'Successfully added all information to relations.';
        }else{
            $response['success'] = 0;
            $response['message'] = "Error adding developmental history data.";
        }
    }else{
        #sdff

        $response['success'] = 0;
        $response['message'] = "Error adding health data.";
    }

}else{
    $response['success'] = 0;
    $response['message'] = "Required fields missing.";
}

echo json_encode($response);




#function to add health description
function addHealthData($con){
    global $response, $offender_id, $health;

    $sql = "INSERT INTO health_record(offender_id,description, date_added) VALUES('$offender_id', '$health', CURRENT_TIMESTAMP)";
    
    if($con->query($sql)){
        $response['success'] = 1;
        $response['health_message'] = "Successfully added to relation.";
        return true;
    }else{
        $response['success'] = 0;
        $response['health_error'] = $con->error;
        return false;
    }
}

#function to add to developmental relation
function addDevelopmentalData($con){
    global $response, $offender_id, $develop;

    $sql = "INSERT INTO developmental_history(offender_id, description, date_added) VALUES('$offender_id','$develop',CURRENT_TIMESTAMP)";

    if($con->query($sql)){
        $response['success'] = 1;
        $response['develop_message'] = "Successfully added history into relation.";
        return true;
    }else{
        $response['success'] = 0;
        $response['develop_error'] = $con->error;
        return false;
    }
}