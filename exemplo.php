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
    echo $x;
    echo $y;
    echo $i;
    echo readline();
}