<?php

require_once dirname(__DIR__,1). '/db_config.php'; 

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);

$json['offender_id']= "1";

if(!empty($json['offender_id'])){

    $offender_id = intval($json['offender_id']);

    $sql = "SELECT * FROM employment_record WHERE offender_id = '$offender_id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $response['employment_records'] = array();

        while($row = $query->fetch_assoc()){
            $temp = array(
                'employer' => $row['employer_name'],
                'position'      => $row['position_held'],
                'date_from'     => $row['date_from'],
                'date_to'       => $row['date_to'],
                'reason'        => $row['reason_for_leaving']
            );

            array_push($response['employment_records'], $temp);
        }

        $response['success'] = 1;
        $response['message'] = 'Successfully retrieved employment records.';
    }else if($query->num_rows == 0){
        $response['success'] = 0;
        $response['message'] = 'No employment records found for this offender.';
    }else{
        $response['success'] = 0;
        $response['message'] = 'Error getting employment records from relation.';
    }

}else{
    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);