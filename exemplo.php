<?php
  {
  $n = readline();
  $i = 1;
  $x = 1;
  $y = 4;
    $init  = "começou primeiro loop";
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
    $init = $init . " mas ja acabou";
    echo $init;
    $g = readline(); /* coloque 0 */
    $t = TrUe;
    $counter = 0;
    while (!$g and $t) {
        if ($g or $t)
          $counter = $counter + 1;
          
        if ($counter == 5){
          echo "acabou segundo loop";
          $g = TRue; 
          $t = faLse;  
        } 
    }
  echo $counter;
  echo $g;
  echo $t;
    if ($g and !$t){
      echo $x;
      echo $y;
      echo $i;
    }
    if ("A"=="A") echo readline();
    if ("B" == "A") echo "devia dar erro";
    
    $x = 1 + True; /* Ok */
    echo $x;
    $x = 1 and True; /* Ok */
    echo $x;
    $x = "a" . 1 . True; /* Ok */
    echo $x;
    $x = "a" == "b"; /* Ok, resultado bool: False */
    echo $x;
    if (tRuE==1) echo "fim do exemplo";
  }
?>