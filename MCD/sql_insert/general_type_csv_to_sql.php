<?php
$strings = file_get_contents('./csv/general_type.csv');
$rows = explode("\r\n", $strings);
array_shift($rows);
/*
id;name;name_fr;name_it;name_es;name_de;name_en
*/
if (($handle = fopen("./output/general_type.sql", "a")) !== FALSE) {
  foreach ($rows as $value) {
    $row = explode(";", $value);
    /*
    INSERT INTO public.generaltypes(
    	id, name, name_fr, name_en, name_es, name_de, name_it)
    	VALUES (?, ?, ?, ?, ?, ?, ?);
    */
    $text = "INSERT INTO public.generaltypes(id, name, name_fr, name_en, name_es, name_de, name_it) VALUES ("
      . $row[0] .
      ", '" . strval($row[1]) .
      "', '" . strval($row[2]) .
      "', '" . strval($row[3]) .
      "', '". strval($row[4]) .
      "', '" . strval($row[5]) .
      "', '" . strval($row[6]) . "' );";

    fwrite($handle, $text);
  }
}
fclose($handle);

 ?>
