<?php

require_once __DIR__ . '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$_POST = json_decode(file_get_contents('php://input'),true);

if(!empty($_POST)){

    $home_conditions = $_POST['home'];
    $community_standing = $_POST['community'];
    $education_list = $_POST['education_record'];
    $offender_id = intval($_POST['offender_id']);

    if(addHomeCommunity($con)){
        
        addEducationRecord($con);

        if(is_null($response['error_edu'])){
            $response['success'] = 1;
            $response['message'] = "Success.";
        }else{
            $response['success'] = 0;
            $response['message'] = "Server error";
        }

    }else{
        $response['success'] = 0;
        $response['message'] = 'Server error';
    }

}else{
    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);

#function to handle inserting home conditions and community standing into home relation
function addHomeCommunity($con){
    global $home_conditions, $community_standing, $response, $offender_id;

    changeFlag($con);
    $sql = "INSERT INTO home_environment(offender_id, community, material_conditions_home,flag) VALUES('$offender_id', '$community_standing', '$home_conditions', 'current')";

    if($con->query($sql)){
        return true;
    }else{
        $response['error_home'] = $con->error;
        return false;
    }
}

#function to change home environment current flag for offender
function changeFlag($con){
    global $response, $offender_id;

    $sql = "UPDATE home_environment SET flag = 'old' WHERE offender_id = '$offender_id'";
    $con->query($sql) or die($con->error);
}

#add education record to relation
function addEducationRecord($con){
    global $response, $education_list, $offender_id;

    if(is_array($education_list)){

        deleteEduData($con);
        for($i=0; $i < sizeof($education_list); $i++){
            $temp = $education_list[$i];

            $sql = "INSERT INTO educational_record(offender_id, school_name, date_from, date_to, qualification) VALUES('$offender_id','".$temp['school_name']."', '".$temp['date_from']."', '".$temp['date_to']."', '".$temp['qualification']."')";

            if($con->query($sql)){
                continue;
            }else{
                $response['error_edu'] .= "'$i'. ".$con->error.";";
            }
        }
    }
}

#delete current education data for updation
function deleteEduData($con){
    global $offender_id;

    $sql = "DELETE FROM educational_record WHERE offender_id = '$offender_id'";
    $con->query($sql);
}