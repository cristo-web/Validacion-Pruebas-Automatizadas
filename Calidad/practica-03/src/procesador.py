import csv

class Analizador:
    def __init__(self, archivo_csv):
        self.archivo_csv = archivo_csv
        self.datos = self.cargar_datos()

    def cargar_datos(self):
        """Lee el archivo CSV y devuelve una lista con los datos."""
        datos = []
        with open(self.archivo_csv, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo, delimiter='|')
            for fila in lector:
                datos.append(fila)
        return datos

    def ventas_totales_por_provincia(self):
        """Retorna un diccionario con el total de ventas por provincia."""
        ventas_por_provincia = {}

        for fila in self.datos:
            provincia = fila['PROVINCIA']
            try:
                total_ventas = float(fila['TOTAL_VENTAS'])
            except ValueError:
                total_ventas = 0.0  # Si no se puede convertir, ponemos 0.0

            if provincia in ventas_por_provincia:
                ventas_por_provincia[provincia] += total_ventas
            else:
                ventas_por_provincia[provincia] = total_ventas

        return ventas_por_provincia

    def ventas_por_provincia(self, nombre):
        """Retorna el total de ventas de una provincia determinada."""
        ventas_totales = 0.0
        for fila in self.datos:
            if fila['PROVINCIA'] == nombre:
                try:
                    ventas_totales += float(fila['TOTAL_VENTAS'])
                except ValueError:
                    continue  # Si hay un error, simplemente lo ignoramos
        return ventas_totales
