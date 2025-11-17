import csv
from collections import defaultdict

class Analizador:
    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv
        self.datos = self.leer_csv()

    def leer_csv(self):
        """Lee el archivo CSV y devuelve una lista de filas."""
        datos = []
        try:
            with open(self.ruta_csv, "r", encoding="utf-8") as archivo:
                lector = csv.DictReader(archivo, delimiter='|')
                for fila in lector:
                    datos.append(fila)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en la ruta: {self.ruta_csv}")
            return []
        except Exception as e:
            print(f"Error al leer el CSV: {e}")
            return []
        return datos

    def ventas_totales_por_provincia(self):
        """Devuelve un diccionario con el total de ventas por provincia."""
        totales = defaultdict(float)

        for fila in self.datos:
            try:
                provincia = fila["PROVINCIA"]
                total_venta = float(fila["TOTAL_VENTAS"])
                totales[provincia] += total_venta
            except (ValueError, KeyError):
                # Ignorar filas con datos inválidos o columnas faltantes
                continue

        return dict(totales)

    def ventas_por_provincia(self, nombre):
        """Devuelve el total de ventas de una provincia específica."""
        totales = self.ventas_totales_por_provincia()

        nombre_estandarizado = nombre.upper() 

        return totales.get(nombre_estandarizado, 0.0)

    def exportaciones_por_mes(self):
        """Devuelve un diccionario con el total de exportaciones por mes (1 a 12)."""
        exportaciones = defaultdict(float)

        for fila in self.datos:
            try:
                mes = int(fila["MES"])
                exportacion = float(fila["EXPORTACIONES"])
                
                # Validamos que el mes sea coherente
                if 1 <= mes <= 12:
                    exportaciones[mes] += exportacion
            except (ValueError, KeyError):
                # Ignorar filas con datos inválidos o columnas faltantes
                continue

        # Ordenamos el diccionario por la clave del mes
        return dict(sorted(exportaciones.items()))

    def provincia_con_mas_importaciones(self):
        """Identifica la provincia con el mayor volumen total de importaciones."""
        importaciones_por_provincia = defaultdict(float)

        for fila in self.datos:
            try:
                provincia = fila["PROVINCIA"]
                importacion = float(fila["IMPORTACIONES"])
                importaciones_por_provincia[provincia] += importacion
            except (ValueError, KeyError):
                # Ignorar filas con datos inválidos o columnas faltantes
                continue
        
        if not importaciones_por_provincia:
            return "N/A", 0.0 
        provincia_max = max(importaciones_por_provincia, key=importaciones_por_provincia.get)
        valor_max = importaciones_por_provincia[provincia_max]
        
        return provincia_max, valor_max
    
    def porcentaje_ventas_tarifa_0_por_provincia(self):
        """
        Calcula el promedio de (VENTAS_NETAS_TARIFA_0 / TOTAL_VENTAS) * 100 por provincia.
        Retorna un diccionario {PROVINCIA: PORCENTAJE}.
        """
        datos_por_provincia = defaultdict(lambda: {'total_cero': 0.0, 'total_ventas': 0.0})

        for fila in self.datos:
            try:
                provincia = fila["PROVINCIA"]
                # Cuidado: convertir las columnas relevantes a float
                ventas_tarifa_cero = float(fila["VENTAS_NETAS_TARIFA_0"])
                total_ventas = float(fila["TOTAL_VENTAS"])

                datos_por_provincia[provincia]['total_cero'] += ventas_tarifa_cero
                datos_por_provincia[provincia]['total_ventas'] += total_ventas
            except (ValueError, KeyError):
                continue
        
        porcentajes = {}
        for prov, datos in datos_por_provincia.items():
            total_cero = datos['total_cero']
            total_ventas = datos['total_ventas']
            
            # Evitar división por cero
            if total_ventas > 0:
                porcentaje = (total_cero / total_ventas) * 100
            else:
                # Si las ventas totales son 0, el porcentaje también es 0.
                porcentaje = 0.0
            
            porcentajes[prov] = porcentaje

        return porcentajes