<?php

require_once __DIR__ . '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);

if(!empty($json['offender_id'])){

    $offender_id = $json['offender_id'];
    $review = $json['review'];

    $sql = "INSERT INTO case_assessment(offender_id, date_added, review) VALUES('$offender_id', CURRENT_TIMESTAMP, '$review')";
    if($con->query($sql)){

        $response['success'] = 1;
        $response['message'] = "Successfully inserted Quaterly Review into database relation";
    }else{
        $response['success'] = 0;
        $response['assess_error'] = $con->error;
        $response['message'] = "Error inserting Quaterly Review in relation";
    }
}else{
    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);