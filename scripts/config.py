"""Parámetros de la ciudad de estudio (Montería, Córdoba), compartidos por todos los scripts."""
CIUDAD = "monteria"
NOMBRE = "Montería"
CENTRO = (8.7479, -75.8814)            # centro urbano (lat, lon)
ESTACION = "0013035501"                # IDEAM, Aeropuerto Los Garzones
ESTACION_ARCHIVO = "los_garzones"
LAT, LON = 8.826, -75.825              # coordenadas de la estación
ESTACION_ANTIGUA = "0013055040"        # IDEAM, INCODER-AUT (2005-2017), contraste con una serie más larga
BBOX = (-75.95, 8.68, -75.80, 8.85)    # oeste, sur, este, norte: casco urbano y aeropuerto
# Ventana 3x3 de celdas de NEX-GDDP-CMIP6 (0,25 grados) centrada en la celda de la estación (8,875 N; 75,875 O);
# la celda del sur (8,625 N) contiene al centro urbano. Longitudes en 0-360.
NEX_LATS = [8.625, 8.875, 9.125]
NEX_LONS = [283.875, 284.125, 284.375]
USER_AGENT = "crc001-monteria-cuaderno/1.0 (cuaderno reproducible de la UNGRD)"
