<?php

require_once dirname(__DIR__,1).'/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);

#$json['offender_id'] = "1";

if(!empty($json['offender_id'])){

	$offender_id = intval($json['offender_id']);
	$response['message'] = '';

	$health = getHealthData($con);
	$devel = getDevelHistoryData($con);

	if($health == true){
		$response['success'] = 1;
		$response['message'] .= ' Success from health record.';
	}else{
		$response['success'] = 0;
	}

	if($devel == true){
		$response['success'] = 1;
		$response['message'] .= ' Success from developmental history.';
	}else{
		$response['success'] = 0;
	}

}else{

	$response['success'] = 0;
	$response['message'] = 'Required fields missing.';
}

echo json_encode($response);

#function to retrieve health data from relation
#some error in this line
function getHealthData($con){

	global $offender_id, $response;

	$sql = "SELECT * FROM health_record WHERE offender_id = '$offender_id'";
	$query = $con->query($sql);

	if($query->num_rows == 0){

		$response['message'] .= "Health record is empty for offender.";
		return false; 
	}else if($query->num_rows > 0){
		$row = $query->fetch_assoc();

		$response['health'] = $row['description'];
		return true;
	}else{
		$response['health_error'] = $con->error;
	}
}

#function to get developmental history data from relation
function getDevelHistoryData($con){
	global $response ,$offender_id;

	$sql = "SELECT * FROM developmental_history WHERE offender_id = '$offender_id'";
	$query = $con->query($sql);

	if($query->num_rows == 0){
		$response['message'] .= " Developmental history record is empty for this offender.";
		return false;
	}else if($query->num_rows > 0){
		$row = $query->fetch_assoc();

		$response['developmental'] = $row['description'];
		return true;
	}else{
		$response['devel_error'] = $con->error;
		return false;
	}
}
