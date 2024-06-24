<?php
include("conexion.php"); // Incluye tu archivo de conexión

if (isset($_GET['id'])) {
    $id = $_GET['id'];

    // Realiza la eliminación del registro en la base de datos
    $query = "DELETE FROM reserva WHERE id_reserva=$id";
    mysqli_query($conexion, $query);

    // Redirecciona a la página de lista de reservas después de la eliminación
    header("Location: ../tablareserva.php");
    exit();
} else {
    // Si no se proporcionó un ID válido, maneja el error o redirecciona a la página de lista de reservas
    header("Location: ../tablareserva.php");
    exit();
}
?>


