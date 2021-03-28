<?php

require_once dirname(__DIR__, 1).'/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);

if(!empty($json['offender_id'])){

    $offender_id = intval($json['offender_id']);

    $home = getHomeCommunityData($con);
    $edu = getEducationData($con);
    if($home == true && $edu == true){
        
        $response['success'] = 1;
        $response['message'] = "Successfully retrieved all data.";
    }

    if($home == false && $edu == true){
        $response['success'] = 1;
        $response['message'] = 'Error getting home and community data from relation.';
    }

    if($home == 0 && $edu == true){
        $response['success'] = 1;
        $response['message'] = "No records found for home and community standing data.";
    }

    if($home == true && $edu == false){
        $response['success'] = 1;
        $response['message'] = "Error getting education records from relation.";
    }

    if($home == true && $edu == 0){
        $response['success'] = 1;
        $response['message'] = "No records about education found in relation.";
    }

    if($home == false && $edu == false){
        $response['success'] = 0;
        $response['message'] = "Error getting home and education records from relation.";
    }

    if($home == 0 && $edu == 0){
        $response['success'] = 0;
        $response['message'] = "Home and education records are empty for this offender.";
    }
    
}else{
    $response['success'] = 0;
    $response['message'] = "Required fields missing.";
}

echo json_encode($response);

#function to get home and community conditions data
function getHomeCommunityData($con){
    global $response, $offender_id;

    $sql = "SELECT * FROM home_environment WHERE offender_id = '$offender_id' AND flag = 'current'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();

        $response['home'] = $row['material_conditions_home'];
        $response['community'] = $row['community'];

        return true;
    }else if($query->num_rows == 0){
        return 0;
    }else{
        $response['conditions_error'] = $con->error;
        return false;
    }
}

#function to get education record from relation
function getEducationData($con){
    global $response, $offender_id;

    $sql = "SELECT * FROM educational_record WHERE offender_id = '$offender_id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $response['edu_list'] = array();
        while($row = $query->fetch_assoc()){
            $temp = array(
                'school_name'   => $row['school_name'],
                'date_from'     => $row['date_from'],
                'date_to'       => $row['date_to'],
                'qualification' => $row['qualification']
            );

            array_push($response['edu_list'], $temp);
        }

        return true;
    }else if($query->num_rows == 0){
        return 0;
    }else{
        $response['edu_error'] = $con->error;
        return false;
    }
}