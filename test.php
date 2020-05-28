<?php
function soma($x, $y) {
  function echoes($b) {
    if($b<10){
      $b = $b + 1;
      echoes($b);
    }else{
      echo "nise";
    }
  }
      $a = $x + $y;
      return $a;
    }
?>