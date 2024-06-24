<?php

include("conexion.php");

$rol = $_POST['rol'];
$email = $_POST['email'];
$contrasena = $_POST['contrasena'];

$sql = "SELECT * FROM usuario WHERE rol = '$rol' and email = '$email' AND contrasena = '$contrasena'";

$result = $conexion->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $rol = $row['rol'];
    
    if ($rol == 'administrador') {
        header('Location: listado.php');
        exit();
    } else {
        header('Location: ../../index.html');
    }
} else {
    echo "Error: Credenciales incorrectas. Por favor, verifica tu email y contraseña.";
}

// Cerrar la conexión a la base de datos
$conexion->close();
?>
