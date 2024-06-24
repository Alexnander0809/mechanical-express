<?php
include("conexion.php"); // Incluye tu archivo de conexión

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Recupera los datos del formulario
    $id = $_POST['id'];
    $nombre = $_POST['nombre'];
    $direccion = $_POST['direccion'];
    $email = $_POST['email'];
    $descripcion = $_POST['descripcion'];
    $precio = $_POST['precio'];
    $fecha_cita = $_POST['fecha_cita'];
    $hora_cita = $_POST['hora_cita'];
    $estado_reserva = $_POST['estado_reserva'];

    // Actualiza el registro en la base de datos
    $query = "UPDATE reserva SET nombre='$nombre', direccion='$direccion', email='$email', descripcion='$descripcion', precio='$precio', fecha_cita='$fecha_cita', hora_cita='$hora_cita', estado_reserva='$estado_reserva' WHERE id_reserva=$id";
    mysqli_query($conexion, $query);

    // Redirecciona a la página de lista de reservas después de la actualización
    header("Location: ../tablareserva.php");
    exit();
} else {
    // Si no se envió el formulario, muestra el formulario de actualización
    $id = $_GET['id'];
    $query = "SELECT id_reserva, nombre, direccion, email, descripcion, precio, fecha_cita, hora_cita , estado_reserva FROM reserva WHERE id_reserva=$id";
    $result = mysqli_query($conexion, $query);
    $row = mysqli_fetch_assoc($result);
    mysqli_close($conexion);
}
?>

<!DOCTYPE html>
<html class="wide wow-animation" lang="en">
  <head>
    <title>Home</title>
    <meta name="format-detection" content="telephone=no">
    <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta charset="utf-8">
    <link rel="icon" href="" type="image/x-icon">
    <!-- Stylesheets-->
    <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Montserrat:400,500,600,700%7CPoppins:400%7CTeko:300,400">
    <link rel="stylesheet" href="../css/bootstrap.css">
    <link rel="stylesheet" href="../css/fonts.css">
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/misestilos.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
    <style>.ie-panel{display: none;background: #212121;padding: 10px 0;box-shadow: 3px 3px 5px 0 rgba(0,0,0,.3);clear: both;text-align:center;position: relative;z-index: 1;} html.ie-10 .ie-panel, html.lt-ie-10 .ie-panel {display: block;}</style>
  </head>
  <body>
    <div class="ie-panel"><a href="http://windows.microsoft.com/en-US/internet-explorer/"><img src="images/ie8-panel/warning_bar_0000_us.jpg" height="42" width="820" alt="You are using an outdated browser. For a faster, safer browsing experience, upgrade for free today."></a></div>
    <div class="preloader">
      <div class="preloader-body">
        <div class="cssload-container">
          <div class="cssload-speeding-wheel"></div>
        </div>
        <p>Loading...</p>
      </div>
    </div>
    <div class="page">

        <div class="rd-navbar-wrap">
          <nav class="rd-navbar rd-navbar-corporate" data-layout="rd-navbar-fixed" data-sm-layout="rd-navbar-fixed" data-md-layout="rd-navbar-fixed" data-md-device-layout="rd-navbar-fixed" data-lg-layout="rd-navbar-static" data-lg-device-layout="rd-navbar-fixed" data-xl-layout="rd-navbar-static" data-xl-device-layout="rd-navbar-static" data-xxl-layout="rd-navbar-static" data-xxl-device-layout="rd-navbar-static" data-lg-stick-up-offset="46px" data-xl-stick-up-offset="46px" data-xxl-stick-up-offset="106px" data-lg-stick-up="true" data-xl-stick-up="true" data-xxl-stick-up="true">
            <div class="rd-navbar-collapse-toggle rd-navbar-fixed-element-1" data-rd-navbar-toggle=".rd-navbar-collapse"><span></span></div>
            <div class="rd-navbar-aside-outer">
             
             </div>
            <div class="rd-navbar-main-outer">
              <div class="rd-navbar-main">
                <div class="rd-navbar-nav-wrap">
                  <ul class="list-inline list-inline-md rd-navbar-corporate-list-social">
                    <li><a class="icon fa fa-facebook" href="#"></a></li>
                    <li><a class="icon fa fa-twitter" href="#"></a></li>
                    <li><a class="icon fa fa-google-plus" href="#"></a></li>
                    <li><a class="icon fa fa-instagram" href="#"></a></li>
                  </ul>
                  <!-- RD Navbar Nav-->
                  <ul class="rd-navbar-nav">
                    <li class="rd-nav-item "><a class="rd-nav-link" href="index.html">Inicio</a>
                    </li>
                    <li class="rd-nav-item"><a class="rd-nav-link" href="">Solicitar domicilio</a>
                    </li>
                    </li>
                    <li class="rd-nav-item"><a class="rd-nav-link" href="typography.html">¿Quienes somos?</a>
                    </li>
                    <li class="rd-nav-item"><a class="rd-nav-link" href="contact-us.html">Contactos</a>
                    </li>
                    <li class="rd-nav-item active"><a class="rd-nav-link" href="reserva.html">Reserva</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </nav>
        </div>
      </header>
    <div class="container">
                <form action="actualizartabla.php" method="POST">
                <input type="hidden" name="id" value="<?php echo $row['id_reserva']; ?>">
              <div class="row">
                <div class="col">
                  <label for="nombre">Nombre:</label>
                    <input type="text" name="nombre" value="<?php echo $row['nombre']; ?>" class="form-control" id="floatingInput" placeholder="Nombre del usuario" required>
                </div>
                <div class="col">
                  <label for="correo">Correo:</label>
                    <input type="email" name="email" value="<?php echo $row['email']; ?>" class="form-control" id="floatingPassword" placeholder="Correo del usuario" required>
                </div>
                </div>
              <div class="row">
                <div class="col">
                  <label for="direccion">Direccion</label>
                <input type="text" name="direccion" value="<?php echo $row['direccion']; ?>" class="form-control" id="floatingInput" placeholder="Ingresa la direccion del lugar donde se hara la reparacion" required>
                </div>
                </div>
              <div class="row">
                <div class="col">
                  <label for="precio">Precio:</label>
                <input type="int" name="precio" value="<?php echo $row['precio']; ?>" class="form-control" id="floatingInput" placeholder="Añade el precio de la reserva" required>
                </div>
                <div class="col">
                  <label for="estado_reserva">Estado de reserva</label>
                  <input type="text" name="estado_reserva" value="<?php echo $row['estado_reserva']; ?>" list="datalistOptions" class="form-control" id="floatingInput" placeholder="estado,ej:pendiente,finalizada" required>
                  <datalist id="datalistOptions">
                    <option value="Activo">
                    <option value="Pendiente">
                    <option value="finalizada">                
                    </datalist>
                </div>
                </div>
              <div class="row">
                <div class="col">
                  <label for="descripcion">Descripcion</label>
                  <textarea role="input" class="form-control" name="descripcion" value="<?php echo $row['descripcion']; ?>" placeholder="Añade una descripcion clara y concisa del problema o proceso que realizaras con el vehiculo" id="floatingTextarea2" style="height: 100px"></textarea>
                </div>
                </div>
              <div class="row">
                <div class="col">
                  <label for="">Fecha</label>
                  <input type="date" name="fecha_cita" value="<?php echo $row['fecha_cita']; ?>" class="form-control" id="floatingInput" placeholder="fecha de la reserva" required>
                </div>
                <div class="col">
                  <label for="">Hora</label>
                  <input type="time" name="hora_cita" value="<?php echo $row['hora_cita']; ?>" class="form-control" id="floatingInput" placeholder="hora de la reserva" required>
                </div>
              </div>
              <div class="row">
              <button type="submit" class="btn btn-dark">Agregar</button>
            </form> 
      </div>
    <script src="../js/core.min.js"></script>
    <script src="../js/script.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.min.js" integrity="sha384-Rx+T1VzGupg4BHQYs2gCW9It+akI2MM/mndMCy36UVfodzcJcF0GGLxZIzObiEfa" crossorigin="anonymous"></script>
  </body>
</html>
</html>