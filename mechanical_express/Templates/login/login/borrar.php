<?php
include("conexion.php");

if ($_SERVER["REQUEST_METHOD"] == "GET" && isset($_GET['id'])) {
    $id = $_GET['id'];

    var_dump($_SERVER["REQUEST_METHOD"]);

    $consulta = "SELECT * FROM usuario WHERE id_usuario = '$id'";
    $resultado = $conexion->query($consulta);

    echo "Antes de verificar la existencia del usuario";

    if ($resultado->num_rows == 1) {
        $consulta_delete = "DELETE FROM usuario WHERE id_usuario = '$id'";

        echo "Antes de eliminar el registro";

        if ($conexion->query($consulta_delete) === TRUE) {
            echo "Registro eliminado correctamente. <a href='listado.php'>Volver al listado</a>";
        } else {
            echo "Error al eliminar el registro: " . $conexion->error;
        }


        echo "Después de eliminar el registro";
    } else {
        echo "Usuario no encontrado.";
    }
    
    $conexion->close();
} else {
    echo "Solicitud no válida.";
}
?>