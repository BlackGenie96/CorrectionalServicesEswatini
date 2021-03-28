<?php

require_once dirname(__DIR__,1). '/db_config.php';

$response = array();
$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);

$json = json_decode(file_get_contents('php://input'),true);


if(!empty($json['offender_id'])){

    $offender_id = intval($json['offender_id']);

    if(offenderData($con)){

        if(residenceData($con)){

            $response['success'] = 1;
            $response['message'] = 'Successfully retrieved data';
        }else{
            $response['success'] = 0;
            $response['message'] = 'Error retrieving residence data from database.';
        }
    }else{
        $response['success'] = 0;
        $response['message'] = 'Error getting offender data from database.';
    }

}else{
    $response['success'] = 0;
    $response['message'] = "Required fields missing.";
}

echo json_encode($response);

#function to get offender data
function offenderData($con){
    global $response, $offender_id;

    $sql = "SELECT * FROM offender WHERE id = '$offender_id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();
        $response['full_names'] = $row['full_names']." ".$row['surname'];
        $response['sex'] = $row['sex'];
        $response['date_of_birth'] = $row['date_of_birth'];
        $response['age'] = $row['age'];
        $response['release_date'] = $row['actual_release_date'];

        return true;
    }else{
        $response['offender_error'] = $con->error;
        return false;
    }
}

#function to get residence information
function residenceData($con){
    global $response, $offender_id;

    $sql = "SELECT * FROM residence WHERE offender_id = '$offender_id' and flag = 'current'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();
        $response['region'] = $row['region'];
        $response['inkhundla'] = $row['inkhundla'];
        $response['umphakatsi'] = $row['umphakatsi'];
        $response['chief'] = $row['chief'];
        $response['indvuna'] = $row['indvuna'];

        return true;
    }else{
        $response['res_error'] = $con->error;
        return false;
    }
}