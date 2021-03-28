<?php

require_once __DIR__.'/db_config.php';

$con = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE) or die($con->error);
$response = array();

$json = json_decode(file_get_contents('php://input'),true);

/*$json = array(
    "offender_id" => "1",
    "date_of_release" => "2021-02-17T00:00:00", 
    "family_aware" => "YES", 
    "immediate_problems_post_release" => "lksjd lfkjas dfaslkd f\t lkj sldkf alskdj flaskj dflk\t lkasj dlkf jasldkf asldkfj aslkdf aslkd flaskd jflaks djflksa dflkasj dflkas dflk asdf\n",
    "clothing_availability" => "YES", 
    "offender_request" => " alks dlfkjas dfklasjd flaskjdflkas jdflkas dflkas jdlfk asjldfk asjldkf jasl dfkasj dlfkja sdlfkjasl;dkfj asl;kdfj alskd fjl;aks djflkas jdlfk jasl;dkf jal;sdkf jalskd fjlask dfjlas; dkfj asdfsdf\n", 
    "rehab_officer_actions" => "shkld faskd flasjkd flaksj dflkasj dlfkjas dlfkj aslkdfj als;kdjf ;askdj flaks jdflaks jdlfk ajsdlkf \n", 
    "comments" => " askdjfl kasjdlf kasjd lfajsd lfijasodifj asoeijfa lkwdjv poaiewufwuie fawsd\n", 
    "officer_name" => "SOme guy here", 
    "officer_date" => "2021-03-10T00:00:00", 
    "release_region" => "Some region", 
    "release_inkhundla" => "some inkhundla", 
    "release_umphakatsi" => "some umphakatsi", 
    "release_chief" => "some chief", 
    "release_indvuna" => "some indvuna", 
    "plans_for_employment_education" => "skl flksj dlfkas lkdj flaskdj flkasj dflkj sdfkj sdlkf jasdfkj asldkf\n", 
    "after_care_contact" => "2021-05-20T00:00:00", 
    "problems_referal_details" => "sadkj flaskd flask dflkas dflkas jdlfk asdjlfk asjd fkasj dlfkasj dl;fkasldkfj aowieu fwoiafu pwe gvuapwi4erf;asd f[aowpef [aipwaql z as dazsbdva;sd \n");*/

if(!empty($json['offender_id'])){

    $offender_id = intval($json['offender_id']);
    $release_date = $json['date_of_release'];
    $family_aware = $json['family_aware'];
    $immediate_problems = $json['immediate_problems_post_release'];
    $employment_plans = $json['plans_for_employment_education'];
    $clothing = $json['clothing_availability'];
    $offender_request = $json['offender_request'];
    $after_care_contact = $json['after_care_contact'];
    $problems_referal = $json['problems_referal_details'];
    $rehab_officer_actions = $json['rehab_officer_actions'];
    $comments = $json['comments'];
    $officer_name = $json['officer_name'];
    $officer_date = $json['officer_date'];

    $release_region = $json['release_region'];
    $release_inkhundla = $json['release_inkhundla'];
    $release_umphakatsi = $json['release_umphakatsi'];
    $release_chief = $json['release_chief'];
    $release_indvuna = $json['release_indvuna'];

    if(checkOffender($con, $offender_id)){
        
        if(updateDischargeData($con)){
            $response['success'] = 1;
            $response['message'] = "Successfully updated discharge interview data.";
        }else{
            $response['success'] = 0;
            $response['message'] = 'Error inserting into discharge interview relation';
        }
    }else{

        if(insertDischargeData($con)){
            $response['success'] = 1;
            $response['message'] = "Successfully inserted discharge interview data.";
        }else{
            $response['success'] = 0;
            $response['message'] = 'Error inserting into discharge interview relation';
        }
    }

    

    if(!empty($release_inkhundla) && !empty($release_region) && !empty($release_umphakatsi) && !empty($release_indvuna) && !empty($release_chief)){
        updateReleaseResidence($con);
    }

}else{
    $response['success'] = 0;
    $response['message'] = 'Required fields missing.';
}

echo json_encode($response);

function checkOffender($con, $offender_id){

    $sql = "SELECT * FROM discharge_interview WHERE offender_id = '$offender_id'";
    $query = $con->query($sql);

    if($query->num_rows > 0){
        return true;
    }else{
        return false;
    }
}

#function that updates into discharge interview relation
function updateDischargeData($con){

    global $response, $offender_id, $release_date, $family_aware, $immediate_problems, $employment_plans, $clothing, $offender_request, $after_care_contact, $problems_referal, $rehab_officer_actions, $comments,$officer_name, $officer_date;

    $sql = "UPDATE discharge_interview SET date_of_releasinserte='$release_date', family_aware_of_release='$family_aware', immediate_problems_post_release='$immediate_problems', plans_for_employment_education='$employment_plans', clothing_availability='$clothing', offender_request='$offender_request', after_care_contact='$after_care_contact', offender_problems_referal='$problems_referal',actions_by_rehabilitation_officer='$rehab_officer_actions',comments='$comments',officer_name='$officer_name', officer_date='$officer_date' WHERE offender_id ='$offender_id'";

    if($con->query($sql)){
        return true;
    }else{
        $response['discharge_error'] = $con->error;
        return false;
    }
}

#function that inserts into discharge interview relation
function insertDischargeData($con){

    global $response, $offender_id, $release_date, $family_aware, $immediate_problems, $employment_plans, $clothing, $offender_request, $after_care_contact, $problems_referal, $rehab_officer_actions, $comments,$officer_name, $officer_date;

    $sql = "INSERT INTO discharge_interview(offender_id, date_of_release, family_aware_of_release, immediate_problems_post_release, plans_for_employment_education, clothing_availability, offender_request, after_care_contact, offender_problems_referal,actions_by_rehabilitation_officer,comments,officer_name, officer_date) VALUE('$offender_id', '$release_date', '$family_aware', '$immediate_problems','$employment_plans', '$clothing', '$offender_request', '$after_care_contact', '$problems_referal', '$rehab_officer_actions', '$comments', '$officer_name', '$officer_date')";

    if($con->query($sql)){
        return true;
    }else{
        $response['discharge_error'] = $con->error;
        return false;
    }
}

#function to insert release information updates
function updateReleaseResidence($con){
    global $response, $offender_id, $release_region, $release_inkhundla, $release_umphakatsi, $release_chief, $release_indvuna;

    #update release residences for this offender
    $sql = "UPDATE residence SET flag = 'old' WHERE offender_id = '$offender_id' AND flag = 'release'";
    
    if($con->query($sql)){

        #insert new release residence information
        $sql = "INSERT INTO residence(offender_id, indvuna, umphakatsi, region, chief, inkhundla, flag) VALUES('$offender_id', '$release_indvuna', '$release_umphakatsi', '$release_region', '$release_chief', '$release_inkhundla', 'release')";

        if($con->query($sql)){
            return true;
        }else{
            $response['insert_error'] = $con->error;
            return false;
        }
    }else{
        $response['update_error'] = $con->error;
        return false;
    }
}