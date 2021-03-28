<?php

require_once __DIR__ . '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);


if(!empty($json['gaol_number'])){

    $gaol = $json['gaol_number'];
    getOffenderInfoWithGaol($con, $gaol);

}else if(!empty($json['id_number'])){

    $id_number = $json['id_number'];
    getOffenderInfoWithId($con, $id_number);
}else{
    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);

#function to retrieve data using offender id
function getOffenderInfoWithId($con, $id_number){

    global $response;
    
    $sql = "SELECT * FROM offender WHERE id_number = '$id_number'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();

        $response['offender_id'] = $row['id'];
        $response['name'] = $row['full_names'];
        $response['surname'] = $row['surname'];
        $response['id_number'] = $row['id_number'];

        //get gaol number using offender id
        $sql = "SELECT * FROM offender_file WHERE offender_id = '".$row['id']."'";
        $query = $con->query($sql);

        if($query->num_rows > 0){
            $row = $query->fetch_assoc();
            $response['gaol_number'] = $row['gaol_number'];
            $response['success'] = 1;
        }else{
            $response['success'] = 0;
            $response['message'] = 'Offender file for '.$response['name'].' '.$response['surname'].'not found';
        }
    }else{
        $response['success'] = 0;
        $response['message'] = "Offender with ID number ".$id_number." not found. Does not exist in database.";
    }
}

#function to retrieve data using gaol number
function getOffenderInfoWithGaol($con, $gaol_number){

    global $response;

    $sql = "SELECT * FROM offender_file WHERE gaol_number = '$gaol_number'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();
        $response['gaol_number'] = $row['gaol_number'];
        $response['offender_id'] = $row['offender_id'];

        $sql = "SELECT * FROM offender WHERE id = '".$row['offender_id']."'";
        $query = $con->query($sql);

        if($query->num_rows > 0){
            $row = $query->fetch_assoc();
            $response['name'] = $row['full_names'];
            $response['surname'] = $row['surname'];
            $response['id_number'] = $row['id_number'];
            $response['success'] = 1;
        }
    }else{
        $response['success'] = 0;
        $response['message'] = 'Offender file with GAOL number '.$gaol_number.' not found'; 
    }
}