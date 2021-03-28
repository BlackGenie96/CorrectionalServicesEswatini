<?php

require_once __DIR__ .'/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

/*$_POST = array(
    'c_f' => '250147', 
    'gaol_number' => '0112|02',
    'full_names' => 'Fanelesibonge Phiwokuhle',
    'surname' => 'Malaza', 
    'sex' => 'M', 
    'date_of_birth' => "1996-7-19", 
    'age' => '24', 
    'id_number' => '9607196100302',
    'region' => 'Manzini', 
    'inkhundla' => 'Ludzeludze Inkhundla', 
    'umphakatsi' => 'Zombodze Umphakatsi', 
    'chief' => 'Chief Manzanza', 
    'indvuna' => 'Mphatsakahle', 
    'next_of_kin_name' => 'Busisiwe Nkhosi', 
    'next_of_kin_phone' => '76159059', 
    'offences' => 'Theft;', 
    'court' => 'Manzini Court House', 
    'sentence' => '3 days in prison', 
    'criminal_case_num' => '55-88-21', 
    'admitting_center' => 'Manzini Correctional Services', 
    'rehabilitation_officer' => '1', 
    'post_sentence_assistance' => '1', 
    'e_d_r' => 'Something E.D.R', 
    'l_d_r' => 'Something L.D.R', 
    'transfer_center' => 'Something transfer center',
    'transfer_center_date' => "2021-2-14", 
    'officer_id' => '1', 
    'court_date' => "2021-2-13", 
    'date_of_reception' => "2021-2-14",
    'actual_release_date' => "2021-2-17", 
    'date_case_closed' => "2021-2-17", 
    'data_set' => '1');*/


if(!empty($_POST['data_set']) && $_POST['data_set'] == 1){

    $cf = $_POST['c_f'];
    $gaol_number = $_POST['gaol_number'];
    $fullnames = $_POST['full_names'];
    $surname = $_POST['surname'];
    $sex = $_POST['sex'];
    $date_of_birth = $_POST['date_of_birth'];
    $age = $_POST['age'];
    $id_number = $_POST['id_number'];
    $region = $_POST['region'];
    $inkhundla = $_POST['inkhundla'];
    $umphakatsi = $_POST['umphakatsi'];
    $chief = $_POST['chief'];
    $indvuna = $_POST['indvuna'];
    $next_of_kin_name = $_POST['next_of_kin_name'];
    $next_of_kin_phone = $_POST['next_of_kin_phone'];
    $offences = $_POST['offences'];
    $sentence = $_POST['sentence'];
    $criminal_case_num = $_POST['criminal_case_num'];
    $admitting_center = $_POST['admitting_center'];
    $rehabilitation_officer = $_POST['rehabilitation_officer'];
    $post_sentence_assistance = $_POST['post_sentence_assistance'];
    $court = $_POST['court'];
    $court_date = $_POST['court_date'];
    $date_of_reception = $_POST['date_of_reception'];
    $actual_release_date = $_POST['actual_release_date'];
    $date_case_closed = $_POST['date_case_closed'];
    $edr = $_POST['e_d_r'];
    $ldr = $_POST['l_d_r'];
    $transfer_center = $_POST['transfer_center'];
    $transfer_center_date = $_POST['transfer_center_date'];
    $officer_id = $_POST['officer_id'];

    $residenceId;
    $offender_id;
    $convictions_id;

    //first check if offender has been registered before
    $check = checkOffender($con);
    if($check == 1){
        //offender has been registered before. update offender details
        if(updateOffender($con)){
            //successfully updated offender profile
            if(setResidenceId($con)){
                //successfully updated residence information
                if(createOffenderFile($con, $offender_id)){
                    //successfully created offender file
                    if(insertIntoConvictionsRelation($con)){
                        //successfully added convictions
                        if(insertIntoOffences($con)){
                            $response['success'] = 1;
                            $response['message'] = 'Successfully created offender file and updated offender profile';
                        }else{
                            $response['success'] = 0;
                            $response['message'] = 'Error adding offences';
                        }
                    }else{
                        $response['success'] = 0;
                        $response['message'] = 'Error adding into convictions';
                    }
                }else{
                    $response['success'] = 0;
                    $response['message'] = 'Error creating new offender file';
                }
            }else{
                $response['success'] = 0;
                $response['message'] = 'Error updating offender residence';
            }
        }else{
            $response['success'] = 0;
            $response['message'] = "Error updating offender profile";
        }
    }else if($check == 2){
        //no offender was found register a new offender with a new offender file
        //start with creating offender profile
        if(createOffender($con)){
            //successfully created offender profile
            if(addResidenceInformation($con)){
                //successfully added residence information
                if(createOffenderFile($con, $offender_id)){
                    //successfully created offender file
                    if(insertIntoConvictionsRelation($con)){
                        //successfully added convictions
                        if(insertIntoOffences($con)){
                            $response['success'] = 1;
                            $response['message'] = "Successfully created offender profile";
                        }else{
                            $response['success'] = 0;
                            $response['message'] = "Error adding offences";
                        }
                    }else{
                        $response['success'] = 0;
                        $response['message'] = "Error adding to convictions.";
                    }
                }else{
                    $response['success'] = 0;
                    $response['message'] = "Error creating offender file.";
                }
            }else{
                $response['success'] = 0;
                $response['message'] = "Error adding residence information for offender.";
            }
        }else{
            $response['message'] = "Error creating offender profile.";
            $response['success'] = 0;
        }
    }else{
        $response['success'] = 0;
        $response['message'] = "Error checking for offender in database.";
    }

}else{

    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);

#function to check if the offender has been registered before
function checkOffender($con){
    global $id_number, $offender_id,$response;

    $sql = "SELECT * FROM offender WHERE id_number = '$id_number'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        #offender has been registered before
        $row = $query->fetch_assoc();
        $offender_id = $row['id'];
        return 1;
    }else if($query->num_rows == 0){
        #no offender was found with this id number. this is a new offender
        return 2;
    }else{
        #error was encountered while checking for offender
        $response['offender_id_error'] = $con->error;
        return 0;
    }
}

#function to create offender file
function createOffenderFile($con, $offenderId){
    global $cf, $gaol_number, $criminal_case_num, $officer_id;
    global $response;

    $sql = "INSERT INTO offender_file(gaol_number, offender_id, officers_id, c_f, criminal_case_number,date_created, date_updated) VALUES('$gaol_number', '$offenderId', '$officer_id', '$cf', '$criminal_case_num', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)";

    if($con->query($sql)){
        return true;
    }else{
        $response['offender_file_error'] = $con->error;
        return false;
    }
}

#function to get offender residence id
function setResidenceId($con){
    global $response, $residenceId, $offender_id, $region, $inkhundla, $umphakatsi, $chief, $indvuna;

    $sql = "SELECT * FROM residence WHERE offender_id = '$offender_id'";
    $query = $con->query($sql) or die($con->error);

    $found = false;

    if($query->num_rows > 0){
        while($row = $query->fetch_assoc()){

            //set all the residences to for this offender to old
            $sql = "UPDATE residence SET flag = 'old' WHERE id = '".$row['id']."'";
            $con->query($sql);

            if(($region == $row['region']) && ($inkhundla == $row['inkhundla']) && ($umphakatsi == $row['umphakatsi']) && ($chief == $row['chief']) && ($indvuna == $row['indvuna'])){

                $found = true;
                //update the current residence information to being the current residence
                $sql = "UPDATE residence SET flag = 'current' WHERE id = '".$row['id']."'";
                $con->query($sql);
                $residenceId = $row['id'];
            }
        }

        if($found){
            //found is true
            return true;
        }else{
            if(addResidenceInformation($con)){
                return true;
            }else{
                return false;
            }
        }
    }else{
        //not residence found for this offender
        return false;
    }

}

#function to handle residence creation for the offender
function addResidenceInformation($con){
    global $region, $umphakatsi, $indvuna, $residenceId, $chief, $inkhundla, $offender_id;
    global $response;

    $sql = "INSERT INTO residence(offender_id, inkhundla, umphakatsi, region, chief, indvuna, flag) VALUES('$offender_id','$inkhundla', '$umphakatsi', '$region', '$chief', '$indvuna', 'current')";

    if($con->query($sql)){
        $residenceId = $con->insert_id;
        return true;
    }else{
        $response['residence_error'] = $con->error;
        return false;
    }
}

#function to create offender data in offender relation
function createOffender($con){
    global $fullnames, $surname, $sex, $date_of_birth, $age, $id_number, $next_of_kin_name, $next_of_kin_phone, $admitting_center, $date_of_reception, $edr, $ldr, $transfer_center, $transfer_center_date, $actual_release_date, $post_sentence_assistance, $date_case_closed, $offender_id, $rehabilitation_officer;

    global $response;

    $sql = "INSERT INTO offender(full_names, surname, sex, date_of_birth, age, id_number, next_of_kin_name, next_of_kin_phone, admitting_center, date_of_reception, e_d_r, l_d_r, transfer_centre, transfer_centre_date, actual_release_date, after_care_sentence_assistance, date_case_closed, religion, marital_status, rehabilitation_officers_id) VALUES('$fullnames', '$surname', '$sex', '$date_of_birth', '$age', '$id_number', '$next_of_kin_name', '$next_of_kin_phone', '$admitting_center', '$date_of_reception', '$edr', '$ldr', '$transfer_center', '$transfer_center_date', '$actual_release_date', '$post_sentence_assistance', '$date_case_closed', NULL, NULL, '$rehabilitation_officer')";

    if($con->query($sql)){
        $response["offender_id"] = $con->insert_id;
        $offender_id = $con->insert_id;
        return true;
    }else{
        $response['offender_error'] = $con->error;
        return false;
    }
}

#function to add offence information into convictions relation
function insertIntoConvictionsRelation($con){

    global $offender_id, $court, $court_date, $sentence;
    global $response, $convictions_id;

    $sql = "INSERT INTO convictions(offender_id, conviction_date, court, sentence) VALUES('$offender_id', '$court_date', '$court', '$sentence')";

    if($con->query($sql)){
        $convictions_id = $con->insert_id;
        return true;
    }else{
        $response["convictions_error"] = $con->error;
        return false;
    }
}

#funtion to add offences offender has been convicted of
function insertIntoOffences($con){
    global $convictions_id, $offences, $response;

    $sql = "INSERT INTO offences(convictions_id, description) VALUES('$convictions_id', '$offences')";

    if($con->query($sql)){
        
        return true;
    }else{
        $response['offences_error'] = $con->error;
        return false;
    }
}

#function to update offender information in offender relation
function updateOffender($con){
    global $response, $offender_id, $fullnames, $surname, $sex, $date_of_birth, $age, $next_of_kin_name, $next_of_kin_phone, $admitting_center, $date_of_reception, $edr, $ldr, $transfer_center, $transfer_center_date, $actual_release_date, $post_sentence_assistance, $date_case_closed, $rehabilitation_officer;

    $sql = "UPDATE offender SET full_names = '$fullnames', surname = '$surname', sex = '$sex', date_of_birth = '$date_of_birth', age = '$age', next_of_kin_name = '$next_of_kin_name', next_of_kin_phone = '$next_of_kin_phone', admitting_center = '$admitting_center', date_of_reception = '$date_of_reception', e_d_r = '$edr', l_d_r = '$ldr', transfer_centre = '$transfer_center', transfer_centre_date = '$transfer_center_date', actual_release_date = '$actual_release_date', after_care_sentence_assistance = '$post_sentence_assistance', date_case_closed = '$date_case_closed', rehabilitation_officers_id = '$rehabilitation_officer' WHERE id = '$offender_id'";

    if($con->query($sql)){
        //update successful.
        return true;
    }else{
        $response['update_error'] = $con->error;
        return false;
    }
}