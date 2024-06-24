<?php

$servername = "localhost";
$username = "root";
$password = "";
$database = "mechanical_express";

$conexion = mysqli_connect($servername, $username, $password, $database);

if (!$conexion) {
    die("Conexión fallo: " . mysqli_connect_error());
}

?>