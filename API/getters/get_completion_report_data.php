<?php

require_once dirname(__DIR__, 1).'/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);



if(!empty($json['offender_id'])){
    $offender_id = intval($json['offender_id']);

    $sql = "SELECT * FROM completion_report WHERE offender_id = '$offender_id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();

        $response['to'] = $row['to_'];
        $response['num_years'] = $row['num_months_years'];
        $response['date_complete'] = $row['date_sentence_complete'];
        $response['comments'] = $row['comments'];
        $response['report_by'] = $row['report_by'];
        $response['date_created'] = $row['date_created'];
        $response['designation'] = $row['designation'];

        $response['success'] = 1;
        $response['message'] = 'Success.';
    }elseif($query->num_rows == 0){
        
        $response['success'] = 0;
        $response['message'] = 'No records for completion report found in database for this offender.';

    }else{
        $response['success'] = 0;
        $response['message'] = 'Error getting completion report data.';
        $response['error'] = $con->error;
    }
}else{
    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);