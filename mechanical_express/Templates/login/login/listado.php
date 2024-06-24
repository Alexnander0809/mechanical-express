<?php
include("conexion.php");

$consulta = "SELECT * FROM usuario";
$resultado = $conexion->query($consulta);

echo "<center><table border='1'>
    <tr>
        <th>ID</th>
        <th>Rol</th>
        <th>Nombre</th>
        <th>Apellido</th>
        <th>Teléfono</th>
        <th>Email</th>
        <th>Edad</th>
        <th>Direccion</th>
        <th>Fecha de creacion</th>
        <th>Estado</th>
        <th>Acciones</th>
    </tr>";

if ($resultado->num_rows > 0) {
    while ($fila = $resultado->fetch_assoc()) {
        echo "<tr>";
        echo "<td>" . $fila['id_usuario'] . "</td>";
        echo "<td>" . $fila['rol'] . "</td>";
        echo "<td>" . $fila['nombre'] . "</td>";
        echo "<td>" . $fila['apellido'] . "</td>";
        echo "<td>" . $fila['telefono'] . "</td>";
        echo "<td>" . $fila['email'] . "</td>";
        echo "<td>" . $fila['edad'] . "</td>";
        echo "<td>" . $fila['direccion'] . "</td>";
        echo "<td>" . $fila['fecha_creacion'] . "</td>";
        // echo "<td>" . $fila['fecha_actualizacion'] . "</td>";
        echo "<td>" . $fila['estado'] . "</td>";
        echo "<td><a href='actualizar.php?id=" . $fila['id_usuario'] . "'>Actualizar</a></td>";

        // borrar
        echo "<td>
            <form action='borrar.php' method='post'>
                <input type='hidden' name='id' value='" . $fila['id_usuario'] . "'>
                <button type='submit'>Borrar</button>
            </form>
        </td>";

        echo "</tr>";
    }
} else {
    echo "<tr><td colspan='8'>No se encontraron usuarios.</td></tr>";
}

echo "</table></center>";

$conexion->close();
?>
