import unittest
import os
from src.procesador import Analizador

# Configuración: Usa la ruta real de tu carpeta de datos
RUTA_ARCHIVO_DATOS = "datos/sri_ventas_2024.csv"

# Número esperado de provincias en Ecuador (24 después de la limpieza)
NUM_PROVINCIAS_ECUADOR = 24 

class TestAnalizador(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configura el objeto Analizador una sola vez antes de todas las pruebas."""
        
        # 💡 CORRECCIÓN 1: Verificar la ruta correcta (datos/ en plural)
        if not os.path.exists(RUTA_ARCHIVO_DATOS):
            raise unittest.SkipTest(f"El archivo de datos no se encontró en la ruta: {RUTA_ARCHIVO_DATOS}. Saltando pruebas.")
        
        cls.analizador = Analizador(RUTA_ARCHIVO_DATOS)
        
        if not cls.analizador.datos:
            raise unittest.SkipTest("El archivo CSV se cargó vacío. Saltando todas las pruebas.")


    def test_ventas_totales_como_diccionario(self):
        """Verifica que ventas_totales_por_provincia retorne un diccionario."""
        resumen = self.analizador.ventas_totales_por_provincia()
        self.assertIsInstance(resumen, dict)

    # REQUISITO 2: Verificar que los valores calculados sean numéricos y no negativos. 
    def test_valores_son_numericos_y_no_negativos(self):
        """Verifica que todos los totales de ventas sean números (float/int) y no sean negativos."""
        resumen = self.analizador.ventas_totales_por_provincia()
        
        for provincia, total_venta in resumen.items():
            self.assertIsInstance(total_venta, (float, int), 
                                  f"El valor de {provincia} no es numérico.")
            # Esta prueba fallaba si tenías provincias con ventas totales calculadas como 0
            self.assertGreaterEqual(total_venta, 0, 
                                    f"El total de ventas para {provincia} es negativo: {total_venta}.")

   
    def test_ventas_por_provincia_inexistente(self):
        """Verifica que al consultar una provincia inexistente LANCE un KeyError."""
        # 💡 CORRECCIÓN 2: Si implementamos un `raise KeyError` en procesador.py, debemos ESPERARLO aquí.
        with self.assertRaises(KeyError):
            self.analizador.ventas_por_provincia("NARNIA")
        
    # REQUISITO 4: Manejo de provincias existentes.
    def test_ventas_por_provincia_existente(self):
        """Verifica que al consultar una provincia existente (con ventas > 0) retorne un valor positivo."""
        # Busca la provincia con ventas más altas (PICHINCHA es un buen candidato)
        resultado = self.analizador.ventas_por_provincia("PICHINCHA") 
        self.assertGreater(resultado, 0.0, f"Las ventas de PICHINCHA deben ser positivas.")

    def test_exportaciones_por_mes_estructura(self):
        """Verifica la estructura y validez de los valores retornados por exportaciones_por_mes()."""
        exportaciones = self.analizador.exportaciones_por_mes()
        self.assertIsInstance(exportaciones, dict)
        
        for mes, valor in exportaciones.items():
            self.assertIsInstance(mes, int)
            self.assertIn(mes, range(1, 13), f"Clave de mes inválida: {mes}")
            self.assertGreaterEqual(valor, 0, f"Valor de exportación negativo en mes {mes}.")
            self.assertIsInstance(valor, (float, int), f"Valor de exportación no numérico en mes {mes}.")

    # ADICIONAL 2: Provincia con mayor volumen de importaciones
    def test_provincia_con_mas_importaciones_formato_y_tipo(self):
        """Verifica que provincia_con_mas_importaciones() retorne una tupla (str, float) no negativa."""
        prov, valor = self.analizador.provincia_con_mas_importaciones()
        self.assertIsInstance(prov, str)
        self.assertIsInstance(valor, (float, int))
        self.assertGreaterEqual(valor, 0.0)
        
        if valor > 0.0:
            self.assertGreater(valor, 0.0)

    # ADICIONAL 3: Porcentaje de ventas con tarifa 0%
    def test_porcentaje_ventas_tarifa_0_estructura_y_limites(self):
        """Verifica que los porcentajes estén entre 0 y 100 y sean numéricos."""
        porcentajes = self.analizador.porcentaje_ventas_tarifa_0_por_provincia()
        self.assertIsInstance(porcentajes, dict)
        
        for provincia, porcentaje in porcentajes.items():
            self.assertIsInstance(porcentaje, (float, int), 
                                  f"El porcentaje de {provincia} no es numérico.")
            
            # El porcentaje debe estar entre 0% y 100%
            self.assertGreaterEqual(porcentaje, 0, f"El porcentaje de {provincia} es negativo.")
            self.assertLessEqual(porcentaje, 100.01, f"El porcentaje de {provincia} excede el 100%.")

if __name__ == '__main__':
    unittest.main()