<?php

require_once dirname(__DIR__,1). '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);

$json['offender_id'] = '1';

if(!empty($json['offender_id'])){

    $offender_id = intval($json['offender_id']);

    $sql = "SELECT * FROM record_of_contact WHERE offender_id = '$offender_id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $response['records'] = array();
        while($row = $query->fetch_assoc()){
            $temp = array(
                'date' => $row['date_of_interview'],
                'nature' => $row['nature_of_contact'],
                'problem' => $row['problem_identified'],
                'tentative' => $row['tentative_action'],
                'final' => $row['final_action']
            );

            array_push($response['records'], $temp);
        }
        
        $response['success'] = 1;
        $response['message'] = 'Successfully retrieved records';
    }else if($query->num_rows == 0){
        $response['success'] = 0;
        $response['message'] = "No records of contact found for this offender.";
    }else{
        $response['error'] = $con->error;
        $response['success'] = 0;
        $response['message'] = "Error retrieving records of contact data from relation.";
    }
}else{
    $response['success'] = 0;
    $response['message'] = "Required fields missing.";
}

echo json_encode($response);