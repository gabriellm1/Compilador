<?php
  
  $n = 8;
  $i = 1;
  $x = 1;
  $y = 4;
  echo $n;
  echo $i;
  echo $x;
  echo $y;
    while (($i < $n) or ($i == $n)) {
      if ($x > $y){
        $y = $y + 1;
      }
      else if ($x < $y) 
        $x = $x + 1;
      else {
              $x = $x + 1;
          }   
          $i = $i + 1;
      }
    echo $n;
    echo $i;
    echo $x;
    echo $y;
    $g = false;
    $t = TrUe;
    $counter = 0;
    while (!$g and $t) {
        if ($g or $t)
          $counter = $counter + 1;
          
        if ($counter == 5){
          $g = TRue; 
          $t = faLse;  
        } 
    }
  echo $counter;
  echo $g;
  echo $t;
  
?>