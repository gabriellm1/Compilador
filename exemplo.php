{
$n = readline();
$i = 1;
$x = 1;
$y = 4;
  while (($i < $n) or ($i == $n)) {
    if ($x > $y)
      $y = $y + 1;
    else if ($x < $y) 
      $x = $x + 1;
    else {
            $x = $x + 1;
        }   
        $i = $i + 1;
    }

  $g = 0;
  $t = 1;
  $counter = 0;
  while (!$g and $t) {
      if ($g or $t)
        $counter = $counter + 1;
        
      if ($counter == 5){
        $g = 1; 
        $t = 0;  
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
  echo readline();
}