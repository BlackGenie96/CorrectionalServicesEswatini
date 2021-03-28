<?php

require_once __DIR__ . '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);

if(!empty($json['offender_id'])){

    $offender_id = $json['offender_id'];
    $date = $json['date'];
    $nature = $json['nature'];
    $problems = $json['problem'];
    $tentative = $json['tentative'];
    $action = $json['final_action'];

    $sql = "INSERT INTO record_of_contact(offender_id, date_of_interview, nature_of_contact, problem_identified, tentative_action, final_action) VALUES('$offender_id', '$date', '$nature', '$problems', '$tentative', '$action')";

    if($con->query($sql)){
        $response['success'] = 1;
        $response['message'] = "Successfully added record of contact to relation.";
    }else{
        $response['success'] = 0;
        $response['message'] = "Error adding record of contact in relation.";
    }
}else{
    $response['success'] = 0;
    $response['message'] = "Required fields missing.";
}

echo json_encode($response);