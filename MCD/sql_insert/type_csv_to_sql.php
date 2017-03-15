<?php
$strings = file_get_contents('./csv/type_poi.csv');
$rows = explode("\r\n", $strings);
array_shift($rows);
/*
id;general_type_id;name;name_fr;name_it;name_es;name_de;name_en
*/
if (($handle = fopen("./output/type_poi.sql", "a")) !== FALSE) {
  foreach ($rows as $value) {
    $row = explode(";", $value);
    /*INSERT INTO public.typespois(
	id, name, name_fr, name_en, name_es, name_de, name_it, generaltypes_id)
	VALUES (?, ?, ?, ?, ?, ?, ?, ?);*/
    $text = "INSERT INTO public.typespois(id, name, name_fr, name_en, name_es, name_de, name_it, generaltypes_id) VALUES ("
      . $row[0] .
      ", '" . strval($row[2]) .
      "', '" . strval($row[3]) .
      "', '" . strval($row[4]) .
      "', '". strval($row[5]) .
      "', '" . strval($row[6]) .
      "', '" . strval($row[7]) .
      "', '" . strval($row[1]) . "' );";

    fwrite($handle, $text);
  }
}
fclose($handle);

 ?>
