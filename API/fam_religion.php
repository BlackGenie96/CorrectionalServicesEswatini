<?php

require_once __DIR__ . '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$_POST = json_decode(file_get_contents('php://input'),true);

//echo json_encode($_POST);

if(!empty($_POST["religion"]) && !empty($_POST["marital_status"]) && !empty($_POST["offender_id"])){

    $religion = $_POST['religion'];
    $marital_status = $_POST['marital_status'];
    $marriage_type = $_POST['marriage_type'];
    if(empty($marriage_type)){
        $marriage_type = NULL;
    }
    $offender_id = $_POST['offender_id'];
    $family = $_POST['family'];
    
    updateOffender($con);
    insertMembers($con);

}else{
    $response['success'] = 0;
    $response['message'] = "Required fields missing.";
}

echo json_encode($response);

//function to update info in offender relation  
function updateOffender($con){
    global $religion, $marital_status, $marriage_type, $offender_id, $response;

    $sql = "UPDATE offender SET religion = '$religion', marital_status = '$marital_status', marriage_type = '$marriage_type' WHERE id = '$offender_id'";

    if($con->query($sql)){
        $response['success'] = 1;
        $response['offender_message'] = "Successful update"; 
    }else{
        $response['success'] = 0;
        $response['error_offender'] = $con->error;
    }   
}

//function to insert family members to family relation
function insertMembers($con){
    global $response, $family, $offender_id;
       
    //$response['fam'] = $family;

    if(is_array($family)){

        if(deleteFamily($con)){
            for($i=0; $i < sizeof($family); $i++){
                $item = $family[$i];
    
                $sql = "INSERT INTO family(offender_id, member_name, member_age, member_relationship) VALUES('$offender_id','".$item['name']."', '".$item['age']."', '".$item['relationship']."')";
    
                if($con->query($sql)){
                    $response['success'] = 1;
                }else{
                    $response['success'] = 0;
                }
            }
    
            if($response['success'] == 0){
                $response['family_error'] = 'Error inserting family members';
            }else{
                $response['message'] = 'Successful insertion of family members';
            }
        }else{
            return;
        }
        
    }else{
        $response['family_error'] = 'Not array';
    }
}

//function to delete offender family members before update 
function deleteFamily($con){
    global $offender_id, $response;

    $sql = "DELETE FROM family where offender_id = '$offender_id'";

    if($con->query($sql)){
        return true;
    }else{
        $response['delete_error'] = $con->error;
        return false;
    }
}