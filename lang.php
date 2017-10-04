<?php
$id = $_GET['id'];

$con =  mysqli_connect('localhost', 'user', 'pass', "database")
	    or die('Could not connect: ' . mysql_error());
$sql = 'SELECT language from user where id="'.$id.'"';
$query = mysqli_query($con, $sql);

while($result = mysqli_fetch_array($query))
{
	  echo $result["language"];
}

?>
