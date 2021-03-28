<?php

require_once __DIR__ . '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$_POST = array(
    'name' => 'Mlindi',
    'surname' => 'Dlamini',
    'officer_number' => '0000'
);

if(!empty($_POST['name']) && !empty($_POST['surname']) && !empty($_POST['officer_number'])){

    $name = $_POST['name'];
    $surname = $_POST['surname'];
    $officer_no = $_POST['officer_number'];

    //check if officer is registered
    $sql = "SELECT * FROM officers WHERE officer_no = '$officer_no'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        //an officer was found
        $response['success'] = 0;
        $response['message'] = "Officer already registered";
    }else{
        //insert new officer
        $sql = "INSERT INTO officers(officer_name, officer_surname, officer_no) VALUES('$name', '$surname', '$officer_no')";

        if($con->query($sql)){
            $response['success'] = 1;
            $response['message'] = 'Successfully registered officer.';
        }else{
            $response['error'] = $con->error;
            $response['success'] = 0;
            $response['message'] = 'Error registering officer.';
        }
    }
}else{
    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);