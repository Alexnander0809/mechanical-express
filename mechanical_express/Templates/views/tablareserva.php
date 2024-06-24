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
    <link rel="stylesheet" href="css/bootstrap.css">
    <link rel="stylesheet" href="css/fonts.css">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/misestilos.css">
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
      <div class="container contenedor-lista">
        <table class="table">
              <?php include("reservaphp/listareserva.php"); ?>
          </table>
    <div class="container-text-center cajaboton">
        <div class="row justify-content-end">
          <div class="btn-group dropup">
            <button type="button" class="btn dropdown-toggle boton rounded-circle" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bi bi-plus-lg icono"></i>
            </button>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item active" href="calendario/index.php">Calendario</a></li>
              <li><a class="dropdown-item" href="tablareserva.html">Tabla</a></li>
              <li><a class="dropdown-item" href="reserva.html">Lista</a></li>
              <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#datosreserva">Agregar</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="modal fade" id="datosreserva" tabindex="-1">
        <div class="modal-dialog  modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">Ingresa los datos de la reserva</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="container-fluid">
                <form action="reservaphp/insertarreserva.php" method="POST">
              <div class="row">
                <div class="col">
                    <input type="text" name="nombrereserva" class="form-control" id="floatingInput" placeholder="Nombre del usuario" required>
                </div>
                <div class="col">
                    <input type="email" name="correoreserva" class="form-control" id="floatingPassword" placeholder="Correo del usuario" required>
                </div>
                </div>
              <div class="row">
                <div class="col">
                <input type="text" name="direccionreserva" class="form-control" id="floatingInput" placeholder="Ingresa la direccion del lugar donde se hara la reparacion" required>
                </div>
                </div>
              <div class="row">
                <div class="col">
                <input type="int" name="precioreserva" class="form-control" id="floatingInput" placeholder="Añade el precio de la reserva" required>
                </div>
                <div class="col">
                  <input type="text" name="estadoreserva" list="datalistOptions" class="form-control" id="floatingInput" placeholder="estado,ej:pendiente,finalizada" required>
                  <datalist id="datalistOptions">
                    <option value="Activo">
                    <option value="Pendiente">
                    <option value="finalizada">                
                    </datalist>
                </div>
                </div>
              <div class="row">
                <div class="col">
                  <textarea class="form-control" name="descripcionreserva" placeholder="Añade una descripcion clara y concisa del problema o proceso que realizaras con el vehiculo" id="floatingTextarea2" style="height: 100px"></textarea>
                </div>
                </div>
              <div class="row">
                <div class="col">
                  <input type="date" name="fechareserva" class="form-control" id="floatingInput" placeholder="fecha de la reserva" required>
                </div>
                <div class="col">
                  <input type="time" name="horareserva" class="form-control" id="floatingInput" placeholder="hora de la reserva" required>
                </div>
              </div>
              <div class="row">
              <button type="submit" class="btn btn-dark">Agregar</button>
              </div>
            </form>
                </div>
              </div>
          </div>
        </div>
      </div>
    <script src="js/core.min.js"></script>
    <script src="js/script.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.min.js" integrity="sha384-Rx+T1VzGupg4BHQYs2gCW9It+akI2MM/mndMCy36UVfodzcJcF0GGLxZIzObiEfa" crossorigin="anonymous"></script>
  </body>
</html>