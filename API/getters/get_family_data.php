<?php

require_once dirname(__DIR__, 1).'/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'), true);

if(!empty($json['offender_id'])){

    $id = intval($json['offender_id']);

    if(getOffenderData($con)){
        if(getFamilyData($con)){

            $response['success'] = 1;
            $response['message'] = "Successfully retrieved all data.";
        }else{
            if($response['success'] == 1){
                
            }else{
                $response['success'] = 0;
                $response['message'] = "Error getting family data from relation.";
            }
        }
    }else{
        $response['success'] = 0;
        $response['message'] = "Error getting offender data.";
    }

}else{
    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);

#function to get religion and marriage information from offender relation
function getOffenderData($con){
    global $response, $id;

    $sql = "SELECT religion, marital_status, marriage_type FROM offender WHERE id = '$id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();
        $response['religion'] = $row['religion'];
        $response['marriage_type'] = $row['marriage_type'];
        $response['marital_status'] = $row['marital_status'];

        return true;
    }else{
        $response['offender_error'] = $con->error;
        return false;
    }
}


#function to family data from family relation
function getFamilyData($con){
    global $response, $id;

    $sql = "SELECT * FROM family WHERE offender_id = '$id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $response['family'] = array();
        while($row = $query->fetch_assoc()){
            $temp = array(
                'name' => $row['member_name'],
                'age' => $row['member_age'],
                'relationship' => $row['member_relationship']
            );

            array_push($response['family'], $temp);
        }

        return true;
    }else if($query->num_rows == 0){
        $response['success'] = 1;
        $response['message'] = "No Family data found.";
        return;
    }else{
        $response['family_error'] = $con->error;
        return false;
    }
}