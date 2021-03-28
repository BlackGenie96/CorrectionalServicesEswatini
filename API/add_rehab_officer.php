<?php

require_once __DIR__ . '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);

$response = array();

/*$_POST = array(
    "name" => "Sebenzile",
    "surname" => "Mazibuko",
    "officer_no" => "1234"
);*/

if(!empty($_POST['name']) && !empty($_POST['surname']) && !empty($_POST['officer_no'])){

    $name = $_POST['name'];
    $surname = $_POST['surname'];
    $officer_no = $_POST['officer_no'];

    if(checkOfficer($con)){
        $response['success'] = 0;
        $response['message'] = 'Officer already registered';
    }else{
        $sql = "INSERT INTO rehabilitation_officers(rehab_name, rehab_surname, officer_no) VALUES('$name', '$surname', '$officer_no')";
    
        if($con->query($sql)){
            $response["success"] = 1;
            $response["message"] = "Successfully inserted officer as a rehabilitation officer";
        }else{ 
            $respose['error'] = $con->error;
            $response['success'] = 0;
            $response['message'] = 'Error inserting officer into rehabilitation officers relation.';
        }    
    }
}else{
    $response["success"] = 0;
    $response["message"] = "Required fields missing.";
}

echo json_encode($response);

//function to check if officer has been registered before
function checkOfficer($con){
    global $officer_no,$response;

    $sql = "SELECT * FROM rehabilitation_officers WHERE officer_no = '$officer_no'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        return true;
    }else{
        $response['officer_error'] = $con->error;
        return false;
    }
}