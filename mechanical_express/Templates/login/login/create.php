<?php
include("conexion.php");

// Ingreso de datos
$rol = $_POST['rol'];
$nombre = $_POST['nombre'];
$apellido = $_POST['apellido'];
$email = $_POST['email'];
$contrasena = $_POST['contrasena'];
$confirmar_contrasena = $_POST['Confirmar_contrasena'];
date_default_timezone_set('America/Bogota');
$fecha_actual = date(format: 'Y-m-d H:i:s');
$estado = 'Activo';

$check_query = "SELECT id_usuario FROM usuario WHERE email = '$email'";
$check_result = mysqli_query($conexion, $check_query);

$hashed_password = password_hash($contrasena, PASSWORD_DEFAULT);
$hashed_confirm_password = password_hash($confirmar_contrasena, PASSWORD_DEFAULT);

if (mysqli_num_rows($check_result) == 0) {
    // No existe registro con el mismo correo electrónico, inserte los datos
    $insertar = "INSERT INTO usuario (rol, nombre, apellido, email, contrasena, confirmar_contrasena, fecha_creacion, estado) 
    VALUES ('$rol', '$nombre', '$apellido', '$email', '$hashed_password', '$hashed_confirm_password', '$fecha_actual', '$estado')"; 

    $resultado = mysqli_query($conexion, $insertar);

    if ($resultado) {
        echo "<script>alert('Se agregó un nuevo registro');
        window.location='../../index.html'</script>";
    } else {
        echo "<script>alert('No se pudo agregar, inténtalo de nuevo');
        window.history.go(-1);</script>";
    }
} else {
    // Ya existe un registro con el mismo correo electrónico
    echo "<script>alert('El correo ya está registrado');
    window.history.go(-1);</script>";
}

mysqli_close($conexion);
?>
