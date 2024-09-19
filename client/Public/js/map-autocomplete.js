$(document).ready(function() {
    // Inicializar el mapa
    var map = L.map('map').setView([6.2518, -75.5636], 12);

    // Agregar capa de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Variable para almacenar el marcador actual
    var currentMarker = null;

    // Función para agregar o actualizar el marcador en el mapa
    function updateMarker(lat, lng, name) {
        // Eliminar el marcador anterior si existe
        if (currentMarker) {
            map.removeLayer(currentMarker);
        }
        // Crear un nuevo marcador y agregarlo al mapa
        currentMarker = L.marker([lat, lng]).addTo(map);
        // Agregar un popup con el nombre del barrio
        currentMarker.bindPopup(name).openPopup();
    }

    // Lista de barrios con coordenadas
    var barrios = [
        {name: "Campo Valdés", coords: [6.242, -75.564]},
        {name: "La Loma", coords: [6.242, -75.565]},
        {name: "Popular", coords: [6.240, -75.566]},

        {name: "Santa Cruz", coords: [6.239, -75.572]},
        {name: "La Esmeralda", coords: [6.240, -75.572]},
        {name: "La Candelaria", coords: [6.238, -75.570]},

        {name: "Manrique Central", coords: [6.263, -75.572]},
        {name: "Manrique Norte", coords: [6.265, -75.570]},
        {name: "Manrique Sur", coords: [6.261, -75.569]},

        {name: "Aranjuez", coords: [6.258, -75.567]},
        {name: "El Trapiche", coords: [6.259, -75.568]},

        {name: "Castilla", coords: [6.249, -75.568]},
        {name: "La Pradera", coords: [6.248, -75.567]},
        {name: "Los Colores", coords: [6.247, -75.569]},

        {name: "Doce de Octubre", coords: [6.251, -75.580]},
        {name: "Fátima", coords: [6.252, -75.581]},

        {name: "Robledo", coords: [6.259, -75.564]},
        {name: "La Campiña", coords: [6.258, -75.565]},
        {name: "Belén", coords: [6.262, -75.562]},

        {name: "Villa Hermosa", coords: [6.237, -75.580]},
        {name: "Los Mangos", coords: [6.236, -75.579]},

        {name: "Buenos Aires", coords: [6.248, -75.577]},
        {name: "La Candelaria", coords: [6.249, -75.575]},

        {name: "La Candelaria", coords: [6.243, -75.570]},
        {name: "El Centro", coords: [6.242, -75.571]},

        {name: "Laureles", coords: [6.236, -75.586]},
        {name: "Estadio", coords: [6.237, -75.585]},

        {name: "San Javier", coords: [6.229, -75.582]},
        {name: "La Loma de los Bernal", coords: [6.230, -75.580]},

        {name: "San Cristóbal", coords: [6.231, -75.579]},
        {name: "La Palma", coords: [6.230, -75.578]},

        {name: "El Poblado", coords: [6.207, -75.567]},
        {name: "Las Palmas", coords: [6.206, -75.569]},

        {name: "Envigado", coords: [6.168, -75.583]},
        {name: "La Magnolia", coords: [6.169, -75.582]},

        {name: "Itagüí", coords: [6.169, -75.611]},
        {name: "San Pío", coords: [6.168, -75.610]},

        {name: "Bello", coords: [6.335, -75.543]},
        {name: "Niquía", coords: [6.336, -75.540]},

        {name: "Sabaneta", coords: [6.176, -75.596]},
        {name: "El Trapiche", coords: [6.175, -75.594]},

        {name: "La Estrella", coords: [6.162, -75.582]},
        {name: "El Trapiche", coords: [6.161, -75.580]},

        {name: "Caldas", coords: [6.069, -75.630]},
        {name: "El Trapiche", coords: [6.068, -75.628]}
    ];

    // Agregar los barrios al mapa inicialmente (opcional)
    barrios.forEach(function(bar) {
        L.marker(bar.coords)
            .bindPopup(bar.name)
            .addTo(map);
    });

    // Autocompletar para la ubicación
    $('#ubicacion').autocomplete({
        source: barrios.map(bar => bar.name),
        select: function(event, ui) {
            var selectedBar = barrios.find(bar => bar.name === ui.item.value);
            if (selectedBar) {
                // Mover el mapa a la ubicación seleccionada y actualizar el marcador
                map.setView(selectedBar.coords, 14);
                updateMarker(selectedBar.coords[0], selectedBar.coords[1], selectedBar.name);
            }
        }
    });

    // Actualizar vista del mapa según la ubicación inicial
    var initialLocation = $('#ubicacion').val();
    var initialBar = barrios.find(bar => bar.name === initialLocation);
    if (initialBar) {
        map.setView(initialBar.coords, 14);
        updateMarker(initialBar.coords[0], initialBar.coords[1], initialBar.name);
    }
});
