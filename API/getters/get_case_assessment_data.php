<?php 

require_once dirname(__DIR__,1).'/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);

$response = array();

$json = json_decode(file_get_contents('php://input'),true);

$json['offender_id'] = "1";

if(!empty($json['offender_id'])){

    $offender_id = intval($json['offender_id']);

    $sql = "SELECT * FROM case_assessment WHERE offender_id = '$offender_id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        $response['case_assess'] = array();
        while($row = $query->fetch_assoc()){
            $temp = array(
                'date_added' => $row['date_added'],
                'review'     => $row['review']
            );

            array_push($response['case_assess'], $temp);
        }

        $response['success'] = 1;
        $response['message'] = "Success.";
    }else if($query->num_rows == 0){
        $response['success'] = 0;
        $response['message'] = 'No case assessment or quaterly reviews found.';
    }else{
        $response['success'] = 0;
        $response['message'] = 'Error retrieving case assessment or quaterly reviews from relation.';
        $response['error']   = $con->error;
    }
}else{
    $response['success'] = 0;
    $response['message'] = "Required fields missing.";
}

echo json_encode($response);