<?php

require_once __DIR__ . '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);

if(!empty($json['offender_id'])){

    $offender_id = intval($json['offender_id']);
    $to          = $json['to'];
    $num_years   = $json['num_years'];
    $sentence_complete = $json['sentence_complete'];
    $comments    = $json['comments'];
    $report_by   = $json['report_by'];
    $date_created = $json['date_created'];
    $designation = $json['designation'];

    if(checkReport($con)){
        if(updateCompletionData($con)){
            $response['success'] = 1;
            $response['message'] = 'Successfully updated completion report.';
        }else{
            $response['success'] = 0;
            $response['message'] = "Error updating completion report.";
        }
    }else{
        if(insertCompletionData($con)){
            
            $response['success'] = 1;
            $response['message'] = "Successfully inserted completion report.";
        }else{
            $response['success'] = 0;
            $response['message'] = "Error creating completion report.";
        }
    }

}else{
    $response['success'] = 0;
    $response['message'] = "Required fields missing.";
}

echo json_encode($response);

function checkReport($con){
    global $offender_id;

    $sql = "SELECT * FROM completion_report WHERE offender_id = '$offender_id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        return true;
    }else{
        $response['check_error'] = $con->error;
        return false;
    }
}

function insertCompletionData($con){
    global $response, $offender_id, $to, $num_years, $sentence_complete, $comments, $report_by, $date_created, $designation;

    $sql = "INSERT INTO completion_report(offender_id, to_, num_months_years, date_sentence_complete, comments, report_by, date_created, designation) VALUES('$offender_id', '$to', '$num_years', '$sentence_complete', '$comments', '$report_by', '$date_created', '$designation')";

    if($con->query($sql)){
        return true;
    }else{
        $response['insert_error'] = $con->error;
        return false;
    }
}

function updateCompletionData($con){
    global $response, $offender_id, $to, $num_years, $sentence_complete, $comments, $report_by, $date_created, $designation;

    $sql = "UPDATE completion_report SET to_ = '$to', num_months_years = '$num_years', date_sentence_complete = '$sentence_complete', comments = '$comments', report_by = '$report_by', date_created = '$date_created', designation = '$designation' WHERE offender_id = '$offender_id'";

    if($con->query($sql)){
        return true;
    }else{
        $response['update_error'] = $con->error;
        return false;
    }
}