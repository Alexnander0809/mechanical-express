<?php
include("conexion.php");

// Ingreso de datos
$nombre = $_POST['nombrereserva'];
$email = $_POST['correoreserva'];
$direccion = $_POST['direccionreserva'];
$descripcion = $_POST['descripcionreserva'];
$precio = $_POST['precioreserva'];
$fecha_cita = $_POST['fechareserva'];
$hora_cita = $_POST['horareserva'];
$estado_reserva = $_POST['estadoreserva'];


$insertar = "INSERT INTO reserva (nombre, email, direccion, descripcion, precio, fecha_cita, hora_cita,estado_reserva) 
VALUES ('$nombre', '$email', '$direccion', '$descripcion', '$precio', '$fecha_cita', '$hora_cita','$estado_reserva')";

// Ejecutar la consulta
if (mysqli_query($conexion, $insertar)) {
    echo "Reserva insertada exitosamente.";
    header("Location: ../reserva.html");
    exit; 
} else {
    echo "Error al insertar la reserva: " . mysqli_error($conexion);
}
?>

