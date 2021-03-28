<?php

require_once __DIR__.'/db_config.php';
$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);

$response = array();

if(!empty($_POST['officer_no'])){

    $id = mysqli_real_escape_string($con, $_POST['officer_no']);

    $sql = "SELECT * FROM `correctional_db`.`officers` WHERE `officers`.`officer_no` = '{$id}'";
    $query = $con->query($sql) or die($con->error);

    if($query->num_rows > 0){
        #successfull login
        $row = $query->fetch_assoc();
        $response['success']     = 1;
        $response['message']     = "Login Successfull";
        $response['name']        = $row['officer_name'];
        $response['surname']     = $row['officer_surname'];
        $response['officer_id']  = $row['officer_no'];
    }else{
        #login not successful
        $response['success']     = 0;
        $response['message']     = "Login Unsuccessful. Incorrect Login details.";
    }

}else{

    $response["success"] = 0;
    $response["message"] = "Required fields missing.";
}

echo json_encode($response);