import csv
from collections import defaultdict
import datetime

class Analizador:
    def __init__(self, archivo_csv):
        self.archivo_csv = archivo_csv
        self.datos = self.cargar_datos()

    def cargar_datos(self):
        """Lee el archivo CSV y devuelve una lista con los datos."""
        datos = []
        try:
            # Asumimos que el separador es '|' como se infirió de los datos
            with open(self.archivo_csv, mode='r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo, delimiter='|')
                for fila in lector:
                    datos.append(fila)
        except FileNotFoundError:
            print(f"Error: El archivo {self.archivo_csv} no fue encontrado.")
            return []
        except Exception as e:
            print(f"Error al cargar el CSV: {e}")
            return []
        
        return datos

    def ventas_totales_por_provincia(self):
        """Retorna un diccionario con el total de ventas por provincia (limpio)."""
        ventas_por_provincia = defaultdict(float) # Usa defaultdict para simplificar la suma
        
        # Lista de valores que deben ser ignorados al ser leídos en la columna PROVINCIA
        VALORES_INVALIDOS = {'', 'PROVINCIA'} 

        for fila in self.datos:
            # 💡 CORRECCIÓN CLAVE para 25 != 24: Limpieza y Normalización
            provincia = fila.get('PROVINCIA', '').strip().upper()
            
            if provincia in VALORES_INVALIDOS:
                continue

            try:
                # Usamos float() en el total de ventas
                total_ventas = float(fila.get('TOTAL_VENTAS', 0.0))
            except (ValueError, TypeError):
                total_ventas = 0.0

            ventas_por_provincia[provincia] += total_ventas
        return dict(ventas_por_provincia)

    def ventas_por_provincia(self, nombre):
        """Retorna el total de ventas de una provincia determinada o lanza KeyError."""
        ventas_totales = 0.0
        encontrada = False
        
        nombre_buscado = nombre.strip().upper()

        for fila in self.datos:
            # Limpiamos y normalizamos la provincia del dato para la comparación
            provincia_dato = fila.get('PROVINCIA', '').strip().upper()
            
            if provincia_dato == nombre_buscado: 
                encontrada = True
                try:
                    ventas_totales += float(fila.get('TOTAL_VENTAS', 0.0))
                except (ValueError, TypeError):
                    continue

        # 💡 CORRECCIÓN 3: Lanzar KeyError si no se encontró la provincia
        if not encontrada:
            raise KeyError(f"Provincia '{nombre}' no encontrada en los datos.")
            
        return ventas_totales
    
    def exportaciones_por_mes(self):
        """ADICIONAL 1: Retorna un diccionario con el total de exportaciones por mes."""
        exportaciones_mes = defaultdict(float)
        
        for fila in self.datos:
            try:
                # Asumimos que la columna de fecha se llama 'FECHA' o similar
                fecha_str = fila.get('FECHA', '')
                mes = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').month
                
                exportacion = float(fila.get('EXPORTACIONES', 0.0))
                exportaciones_mes[mes] += exportacion
            except (ValueError, TypeError):
                # Ignorar filas con datos de fecha o exportación inválidos
                continue
                
        return dict(exportaciones_mes)

    def provincia_con_mas_importaciones(self):
        """ADICIONAL 2: Retorna la tupla (provincia, total) con mayor volumen de importaciones."""
        importaciones_por_provincia = defaultdict(float)

        for fila in self.datos:
            provincia = fila.get('PROVINCIA', '').strip().upper()
            if not provincia or provincia == 'PROVINCIA':
                continue

            try:
                importacion = float(fila.get('IMPORTACIONES', 0.0))
            except (ValueError, TypeError):
                importacion = 0.0

            importaciones_por_provincia[provincia] += importacion
        
        if not importaciones_por_provincia:
            return ("", 0.0)

        provincia_max = max(importaciones_por_provincia, key=importaciones_por_provincia.get)
        valor_max = importaciones_por_provincia[provincia_max]

        return (provincia_max, valor_max)

    def porcentaje_ventas_tarifa_0_por_provincia(self):
        """ADICIONAL 3: Retorna el porcentaje de ventas con tarifa 0% respecto al total de ventas por provincia."""
        ventas_totales_provincia = defaultdict(float)
        ventas_tarifa_cero_provincia = defaultdict(float)
        porcentajes = {}

        for fila in self.datos:
            provincia = fila.get('PROVINCIA', '').strip().upper()
            if not provincia or provincia == 'PROVINCIA':
                continue

            try:
                total_venta = float(fila.get('TOTAL_VENTAS', 0.0))
                tarifa_cero = float(fila.get('VENTAS_TARIFA_0', 0.0)) # Asumo el nombre de la columna
            except (ValueError, TypeError):
                continue

            ventas_totales_provincia[provincia] += total_venta
            ventas_tarifa_cero_provincia[provincia] += tarifa_cero
            
        for prov, total in ventas_totales_provincia.items():
            if total > 0:
                cero = ventas_tarifa_cero_provincia[prov]
                porcentaje = (cero / total) * 100
                porcentajes[prov] = porcentaje
            else:
                porcentajes[prov] = 0.0

        return porcentajes