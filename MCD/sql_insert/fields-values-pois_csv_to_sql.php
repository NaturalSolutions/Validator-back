<?php
$strings = file_get_contents('./csv/poi_parc-jardin-vsm.csv');
$rows = explode("\r\n", $strings);
$headers = array_shift($rows);
$header = explode(";", $headers);
/*
id;longitude;latitude;name;name_en;name_fr;name_es;name_de;name_it;visit_time_min;visit_time_max;price_min;price_max;type_id;street;postal_code;phone;mail;website;resa_link;url_img1;url_img2;desc;desc_en;desc_fr;desc_es;desc_de;desc_it;withchild
*/


if (($handleFields = fopen("./output/fields_csv_to_sql.sql", "a")) !== FALSE) {
  $required = 'FALSE';

  /*INSERT INTO public.fields(id, pos, name, required, types_id)
     VALUES (?, ?, ?, ?, ?);*/
  foreach ($header as $key => $value) {
    if($value == 'name'){
      $required = 'TRUE';
    }
    if($value == 'id' || $value == 'type_id'){
      continue;
    }
    $insertFields = "INSERT INTO public.fields(id, pos, name, required, types_id) VALUES ("
      . $key .
      ", " . $key .
      ", '" . strval($value) .
      "', '" . $required .
      "', ". switchType($value) .");\n";
    fwrite($handleFields, $insertFields);
  }
}

$pas = 1;
if (($handlePois = fopen("./output/pois_csv_to_sql.sql", "a")) !== FALSE) {

  foreach ($rows as $key => $value) {
    if($key == 110 ) break;
    $row = explode(";", $value);
    /*INSERT INTO public.pois(id, tour_id, typespois_id)
       VALUES (?, ?, ?);*/
    $insertPois = "INSERT INTO public.pois(id, tour_id, typespois_id) VALUES ("
      . $row[0] .
      ", '" . strval($row[0]) .
      "', '" . strval($row[13]) . "' );\n";
    fwrite($handlePois, $insertPois);

    /*INSERT INTO public."values"(id, value, createddate, iduser)
     VALUES (?, ?, ?, ?);*/

    for($i= 1; $i < count($row) ; $i++){
      if($i == 13 || $row[$i] == '' || $row[$i] == -1){
        continue;
      }
      if (($handleValues = fopen("./output/values_csv_to_sql.sql", "a")) !== FALSE) {

        $insertValues = "INSERT INTO public.values(id, value, createddate, users_id) VALUES ("
          . $pas .
          ", '" . $row[$i] .
          "',  '01/01/2014' , 1 );\n";
        fwrite($handleValues, $insertValues);
      }
      if (($handleContrib = fopen("./output/contributions_csv_to_sql.sql", "a")) !== FALSE) {

        /*INSERT INTO public.contributions(version, status, idfield, idvalue, idpoi)
           VALUES (?, ?, ?, ?, ?);*/
         $insertContributions = "INSERT INTO public.contributions(version, status, idfield, idvalue, idpoi) VALUES (1,'in progress', "
           . $i .
           ", " . $pas .
           ", " .  addslashes($row[0]) . ");\n";
         fwrite($handleContrib, $insertContributions);
      }
      $pas++;
    }
  }
}

$updateSequence = "SELECT setval('values_id_seq', (SELECT max(id) FROM public.values));SELECT setval('pois_id_seq', (SELECT max(id) FROM public.pois));SELECT setval('fields_id_seq', (SELECT max(id) FROM public.fields));";
fwrite($handleContrib, $updateSequence);

fclose($handleFields);
fclose($handlePois);
fclose($handleValues);
fclose($handleContrib);

function valueToJson($header, $value){
  if(gettype($value) != 'array'){
    $value = array($header => $value);
  }
  return json_encode($value, JSON_HEX_APOS);
}

function switchType($value){
  /*
  id;longitude;latitude;name;name_en;name_fr;name_es;name_de;name_it;visit_time_min;visit_time_max;price_min;price_max;
  type_id;street;postal_code;phone;mail;website;resa_link;url_img1;url_img2;desc;desc_en;desc_fr;desc_es;desc_de;desc_it;withchild

  */
  $type;
  switch ($value) {
    case 'longitude':
    case 'latitude':
    case 'price_min':
    case 'price_max':
        $type = 7;
        break;
    case 'name':
    case 'name_en':
    case 'name_fr':
    case 'name_es':
    case 'name_de':
    case 'name_it':
    case 'street':
    case 'mail':
    case 'website':
    case 'resa_link':
        $type = 1;
        break;
    case 'visit_time_min':
    case 'visit_time_max':
        $type = 2;
        break;
    case 'postal_code':
    case 'phone':
        $type = 8;
        break;
    case 'url_img1':
    case 'url_img2':
      $type = 6;
      break;
    case 'desc':
    case 'desc_en':
    case 'desc_fr':
    case 'desc_es':
    case 'desc_de':
    case 'desc_it':
      $type = 9;
      break;
    case 'withchild':
      $type = 5;
      break;
  }
  return $type;
}

?>
