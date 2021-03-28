<?php

require_once dirname(__DIR__,1) . '/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);


$json['id_number'] = '9607196100302';

#check for offender id 
if(!empty($json['id_number'])){

    $id_number = $json['id_number'];

    #retrieve offender data from offender relation{
    if(getOffenderData($con, $id_number)){

        if(getResidenceData($con)){

            if(getOffenderFileData($con)){

                if(getConvictionsData($con)){

                    if(getRehabOfficer($con)){

                        $response['success'] = 1;
                        $response['message'] = "Successfully retrieved case record data.";
                    }else{
                        $response['success'] = 0;
                        $response['message'] = "Error getting rehab officer data from relation.";
                    }
                }else{
                    $response['success'] = 0;
                    $response['message'] = "Error getting convictions data from relation.";
                }
            }else{
                $response['success'] = 0;
                $response['message'] = "Error getting offender file data from relation.";
            }
        }else{
            $response['success'] = 0;
            $response['message'] = "Error getting residence data from relation.";
        }
    }else{
        $response['success'] = 0;
        $response['message'] = "Error getting offender data from relation.";
    }
}else{
    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);

#function to handle retrieving data from offender relation
function getOffenderData($con, $id_number){
    global $response;

    $sql = "SELECT * FROM offender WHERE id_number = '$id_number'";
    $query = $con->query($sql) or die($con->error);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();

        $response['id'] = $row['id'];
        $response['full_names'] = $row['full_names'];
        $response['surname'] = $row['surname'];
        $response['sex'] = $row['sex'];
        $response['id_number'] = $row['id_number'];
        $response['date_of_birth'] = $row['date_of_birth'];
        $response['age'] = $row['age'];
        $response['next_of_kin_name'] = $row['next_of_kin_name'];
        $response['next_of_kin_phone'] = $row['next_of_kin_phone'];
        $response['admitting_center'] = $row['admitting_center'];
        $response['date_of_reception'] = $row['date_of_reception'];
        $response['e_d_r'] = $row['e_d_r'];
        $response['l_d_r'] = $row['l_d_r'];
        $response['transfer_centre'] = $row['transfer_centre'];
        $response['transfer_centre_date'] = $row['transfer_centre_date'];
        $response['actual_release_date'] = $row['actual_release_date'];
        $response['after_case_sentence_assistance'] = $row['after_care_sentence_assistance'];
        $response['date_case_closed'] = $row['date_case_closed'];
        $response['rehabilitation_officer_id'] = $row['rehabilitation_officers_id'];
        
        return true;
    }else{
        return false;
    }
}

#function to retrieve residence data from residence relation
function getResidenceData($con){
    global $response;

    $id = $response['id'];

    $sql = "SELECT * FROM residence WHERE offender_id = '$id' AND flag = 'current'";
    $query = $con->query($sql) or die($con->error);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();

        $response['indvuna'] = $row['indvuna'];
        $response['umphakatsi'] = $row['umphakatsi'];
        $response['region'] = $row['region'];
        $response['chief'] = $row['chief'];
        $response['inkhundla'] = $row['inkhundla'];
        
        return true;
    }else{
        return false;
    }
}

#function to get offender file data
function getOffenderFileData($con){
    global $response;

    $id = $response['id'];

    $sql = "SELECT * FROM offender_file WHERE offender_id = '$id'";
    $query = $con->query($sql) or die($con->error);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();

        $response['gaol_number'] = $row['gaol_number'];
        $response['c_f'] = $row['c_f'];
        $response['criminal_case_number'] = $row['criminal_case_number'];
        
        return true;
    }else{
        return false;
    }
}

#function to retrieve conviction and offence data 
function getConvictionsData($con){
    global $response;

    $id = $response['id'];

    $sql = "SELECT * FROM convictions WHERE offender_id = '$id' AND flag = 'current'";
    $query = $con->query($sql) or die($con->error);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();

        $response['court_date'] = $row['conviction_date'];
        $response['court_name'] = $row['court'];
        $response['sentence'] = $row['sentence'];
        $response['offences'] = getOffencesData($con,$row['id']);

        return true;
    }else{
        return false;
    }
}

#function to retrieve offences from offence relation
function getOffencesData($con, $conviction_id){
    
    $sql = "SELECT * FROM offences WHERE convictions_id = '$conviction_id'";
    $query = $con->query($sql) or die($con->error);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();

        return $row['description'];
    }else{
        return null;
    }
}

#function to get rehabilitation officer
function getRehabOfficer($con){
    global $response;

    $id = $response['rehabilitation_officer_id'];

    $sql = "SELECT * FROM rehabilitation_officers WHERE id = '$id'";
    $query = $con->query($sql) or die($con->error);

    if($query->num_rows > 0){
        $row = $query->fetch_assoc();

        $response['rehabilitation_officer_name'] = $row['rehab_name'];
        $response['rehabilitation_officer_surname'] = $row['rehab_surname'];
        $response['rehabilitation_officer_number'] = $row['officer_no'];

        return true;
    }else{
        return false;
    }
}