<?php

$u='" or 1=1--';
$p='asdf';
$query = "SELECT * from users where username=\"".$u."\" and password=\"".$p."\"";
echo $query;

?>
