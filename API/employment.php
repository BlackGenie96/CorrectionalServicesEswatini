<?php

require_once __DIR__ . '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$_POST = json_decode(file_get_contents('php://input'),true);


if(!empty($_POST['offender_id']) && !empty($_POST['records'])){

    $records = $_POST['records'];
    $offender_id = $_POST['offender_id'];

    if(is_array($records)){

        deleteRecords($con);
        
        for($i=0; $i < sizeof($records); $i++){
            $temp = $records[$i];

            $sql = "INSERT INTO employment_record(offender_id,employer_name, position_held, date_from, date_to, reason_for_leaving) VALUES('$offender_id', '".$temp['employer']."', '".$temp['position']."', '".$temp['date_from']."', '".$temp['date_to']."', '".$temp['reason']."')";

            if($con->query($sql)){
                continue;
            }else{
                $response['error'] .= "'$i'. ".$con->error.";"; 
            }
        }
    }

    if(is_null($response['error'])){
        $response['success'] = 1;
        $response['message'] = "Success";
    }else{
        $response['success'] = 0;
        $response['message'] = "Server error";
    }
}else{
    $response['success'] = 0;
    $response['message'] = "Required fields missing";
}

echo json_encode($response);

#function to delete offender employment options for updation
function deleteRecords($con){

    global $offender_id;

    $sql = "DELETE FROM employment_record WHERE offender_id = '$offender_id'";
    $con->query($sql);
}