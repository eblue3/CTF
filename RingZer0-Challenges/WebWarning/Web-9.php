<?php
$salt = 'vunp';
$hash = '0e612198634316944013585621061115'
for ($i=1; $i<100000000000; $i++) {
  if (md5($salt . $i) == $hash) {
    echo $i;
    break;
  }
}
 ?>
