<?php

require_once dirname(__DIR__, 1).'/db_config.php';

$response = array();
$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);

$json = json_decode(file_get_contents('php://input'),true);

#$json['offender_id'] = '1';

if(!empty($json['offender_id'])){
    
    $offender_id = $json['offender_id'];

    $sql = "SELECT * FROM discharge_interview WHERE offender_id = '$offender_id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();

        $response['date_of_release'] = $row['date_of_release'];
        $response['family_aware'] = $row['family_aware_of_release'];
        $response['immediate_problems'] = $row['immediate_problems_post_release'];
        $response['plans_for_employment'] = $row['plans_for_employment_education'];
        $response['clothing'] = $row['clothing_availability']; 
        $response['offender_request'] = $row['offender_request'];
        $response['after_care_contact'] = $row['after_care_contact'];
        $response['problems_referal'] = $row['offender_problems_referal'];
        $response['rehab_officer_actions'] = $row['actions_by_rehabilitation_officer'];
        $response['comments'] = $row['comments'];
        $response['officer_name'] = $row['officer_name'];
        $response['officer_date'] = $row['officer_date'];

        getReleaseResidence($con);

        $response['success'] = 1;
        $response['message'] = "Successfully retrieved discharge interview data.";
    }else{
        $response['success'] = 0;
        $response['message'] = "Discharge Interview Record not found.";
    }
}else{
    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);

function getReleaseResidence($con){
    global $response,$offender_id;

    $sql = "SELECT * FROM residence WHERE offender_id = '$offender_id' AND flag = 'release'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();

        $response['region'] = $row['region'];
        $response['inkhundla'] = $row['inkhundla'];
        $response['umphakatsi'] = $row['umphakatsi'];
        $response['chief'] = $row['chief'];
        $response['indvuna'] = $row['indvuna'];
    }
}