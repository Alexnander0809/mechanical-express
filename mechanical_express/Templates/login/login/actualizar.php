<?php
// include("listado.php");
include("conexion.php");

$rol = "";
$nombre = "";
$apellido = "";
$telefono = "";
$email = "";
$edad = "";
$id = "";

// var_dump($id);
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_GET['id_usuario'])) {
    $id = $_GET['id_usuario'];
    var_dump($id);
    $consulta = "SELECT rol, nombre, apellido , telefono, email, edad FROM usuario WHERE id_usuario = ?";
    $stmt = $conexion->prepare($consulta);
    $stmt->bind_param("id_usuario", $id);

    if ($stmt->execute()) {
        $result = $stmt->get_result();

        if ($result->num_rows == 1) {
            $row = $result->fetch_assoc();
            $rol = $row['rol'];
            $nombre = $row['nombre'];
            $apellido = $row['apellido'];
            $telefono = $row['telefono'];
            $email = $row['email'];
            $edad = $row['edad'];
        } else {
            echo "Usuario no encontrado.";
            exit();
        }
    } else {
        echo "Error en la consulta: " . $stmt->error;
        exit();
    }
}

if (isset($_POST['Actualizar'])) {
    $id = $_POST['id'];
    $rol = $_POST['rol'];
    $nombre = $_POST['nombre'];
    $apellido = $_POST['apellido'];
    $telefono = $_POST['telefono'];
    $email = $_POST['email'];
    $edad = $_POST['edad'];

    $consulta = "UPDATE usuario SET rol=?, nombre=?, apellido=?, telefono=?, email=?, edad=? WHERE id_usuario=?";
    $stmt = $conexion->prepare($consulta);
    $stmt->bind_param("ssssssi", $rol, $nombre, $apellido, $telefono, $email, $edad, $id);

    if ($stmt->execute()) {
        echo "Actualización exitosa. <a href='listado.php'>Volver al listado</a>";
    } else {
        echo "Error al actualizar el registro: " . $stmt->error;
    }
}

// $conexion->close();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Actualizar Usuario</title>
</head>
<body>
    <center>
        <h2>Actualizar Usuario</h2>
        <form method="post">
            <input type="hidden" name="id" value="<?php echo $id; ?>">
            <label for="rol">Rol:</label>
            <select name="rol">
                <option value="domiciliario" <?php if ($rol == 'domiciliario') echo 'selected'; ?>>Domiciliario</option>
                <option value="usuario" <?php if ($rol == 'usuario') echo 'selected'; ?>>Usuario</option>
                <option value="taller" <?php if ($rol == 'taller') echo 'selected'; ?>>Taller</option>
            </select><br>
            <label for="nombre">Nombre:</label>
            <input type="text" name="nombre" value="<?php echo $nombre; ?>"><br>
            <label for="apellido">Apellido:</label>
            <input type="text" name="apellido" value="<?php echo $apellido; ?>"><br>
            <label for="telefono">Teléfono:</label>
            <input type="text" name="telefono" value="<?php echo $telefono; ?>"><br>
            <label for="email">Email:</label>
            <input type="email" name="email" value="<?php echo $email; ?>"><br>
            <label for="edad">Edad:</label>
            <input type="text" name="edad" value="<?php echo $edad; ?>"><br>
            <input type="submit" value="Actualizar" name="Actualizar">
        </form>
    </center>
</body>
</html>
