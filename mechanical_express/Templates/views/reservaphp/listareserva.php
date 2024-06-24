<style>
    .hidden {
        display: none;
    }
</style>

<?php
include("conexion.php"); // Incluye tu archivo de conexión
// Query para obtener los datos de la base de datos (ajusta esto según tu estructura)
$query = "SELECT  id_reserva,nombre, direccion, email , descripcion, precio, fecha_cita, hora_cita, estado_reserva FROM reserva";
$result = mysqli_query($conexion, $query);
// Comienza la tabla HTML

echo '<table class="table">
        <h2>Reservas</h2>
        <thead>
          <tr>
            <th scope="col" class="hidden">ID</th>
            <th scope="col">Nombre</th>
            <th scope="col">Direccion</th>
            <th scope="col">Email</th>
            <th scope="col">Descripcion</th>
            <th scope="col">Precio</th>
            <th scope="col">Fecha</th>
            <th scope="col">Hora</th>
            <th scope="col">Estado</th>
            <th scope="col">Acciones</th>
          </tr>
        </thead>
        <tbody>';

// Itera sobre los resultados y genera las filas de la tabla
while ($row = mysqli_fetch_assoc($result)) {
    echo '<tr>';
    echo '<th scope="row" class="hidden">' . $row['id_reserva'] . '</th>';
    echo '<th scope="row">' . $row['nombre'] . '</th>';
    echo '<td>' . $row['direccion'] . '</td>';
    echo '<td>' . $row['email'] . '</td>';
    echo '<td>' . $row['descripcion'] . '</td>';
    echo '<td>' . $row['precio'] . '</td>';
    echo '<td>' . $row['fecha_cita'] . '</td>';
    echo '<td>' . $row['hora_cita'] . '</td>';
    echo '<td>' . $row['estado_reserva'] . '</td>';
    echo '<td>';
    echo '<a href="reservaphp/actualizartabla.php?id=' . $row['id_reserva'] . '" class="btn btn-primary">Actualizar</a>';
    echo '<a href="reservaphp/borrar.php?id=' . $row['id_reserva'] . '" class="btn btn-danger">Borrar</a>';
    echo '</td>';
    echo '</tr>';
}

// Cierra la tabla HTML
echo '</tbody></table>';

// Cierra la conexión
mysqli_close($conexion);
?>