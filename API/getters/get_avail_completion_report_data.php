<?php

require_once dirname(__DIR__, 1).'/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE)or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);

if(!empty($json['offender_id'])){

    $offender_id = intval($json['offender_id']);

    if(getCriminalCaseNum($con)){

        if(getOffenderData($con)){

            if(getResidenceData($con)){
                
                if(getConvictionsData($con)){

                    $response['success'] = 1;
                    $response['message'] = "Successfully retrieved data.";
                }else{
                    $response['success'] = 0;
                    $response['message'] = 'Error getting convictions from database.';
                }
            }else{
                $response['success'] = 0;
                $response['message'] = 'Error getting residence data from database';
            }
        }else{
            $response['success'] = 0;
            $response['message'] = 'Error getting offender information from database.';
        }
    }else{
        $response['success'] = 0;
        $response['message'] = 'Error getting criminal case number.';
    }
}else{
    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);

function getCriminalCaseNum($con){
    global $offender_id, $response;

    $sql = "SELECT criminal_case_number FROM offender_file WHERE offender_id = '$offender_id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();
        $response['criminal_case_number'] = $row['criminal_case_number'];
        return true;
    }else{
        $response['criminal_error'] = $con->error;
        return false;
    }
}

function getOffenderData($con){
    global $response, $offender_id;

    $sql = "SELECT full_names, surname, date_of_birth FROM offender WHERE id = '$offender_id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();
        $response['full_names'] = $row['full_names']." ".$row['surname'];
        $response['date_of_birth'] = $row['date_of_birth'];

        return true;
    }else{
        $response['offender_error'] = $con->error;
        return false;
    }
}

function getResidenceData($con){
    global $response, $offender_id;

    $sql = "SELECT region, indvuna, umphakatsi, chief, inkhundla FROM residence WHERE offender_id = '$offender_id' and flag = 'current'";
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
        $response['residence_error'] = $con->error;
        return false;
    }
}

function getConvictionsData($con){
    global $response, $offender_id;

    $sql = "SELECT * FROM convictions WHERE offender_id = '$offender_id' AND flag = 'current'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();
        $response['court_date'] = $row['conviction_date'];
        $response['court'] = $row['court'];
        $response['sentence'] = $row['sentence'];
        
        $sql = "SELECT * FROM offences WHERE convictions_id = '".$row['id']."'";
        $query = $con->query($sql);

        if($query->num_rows > 0){
            $row = $query->fetch_assoc();
            $response['offences'] = $row['description'];

            return true;
        }else{
            $response['offences_error'] = $con->error;
            return false;
        }
    }else{
        $response['convictions_error'] = $con->error;
        return false;
    }
}