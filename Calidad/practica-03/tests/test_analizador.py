import unittest
from src.procesador import Analizador

class TestAnalizador(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.analizador = Analizador("datos/sri_ventas_2024.csv")

    def test_ventas_totales_como_diccionario(self):
        resumen = self.analizador.ventas_totales_por_provincia()
        self.assertIsInstance(resumen, dict)

    def test_ventas_totales_todas_las_provincias(self):
        resumen = self.analizador.ventas_totales_por_provincia()
        total_provincias = len(resumen)
        self.assertGreaterEqual(total_provincias, 1)

    def test_ventas_totales_mayores_5k(self):
        resumen = self.analizador.ventas_totales_por_provincia()
        self.assertTrue(any(float(v) > 5000 for v in resumen.values()))

        #CÓDIGO SIN LAMDA 

        # bandera = true
        # for ventas in resumen.values():
        #     if float(ventas) < 5000:
        #     bandera = false
        #     break 
        # self.assertTrue(bandera)

    def test_ventas_por_provincia_inexistente(self):
        resultado = self.analizador.ventas_por_provincia("Narnia")
        self.assertEqual(resultado, 0)

    def test_ventas_por_provincia_existente(self):
        resumen = self.analizador.ventas_totales_por_provincia()
        provincia = next((p for p, v in resumen.items() if float(v) > 0), None)
        if provincia is None:
            self.skipTest("No hay provincias con ventas > 0 en el CSV")
        else:
            resultado = self.analizador.ventas_por_provincia(provincia)
            self.assertGreater(resultado, 0)

    # PRUEBA ADICIONAL 3: Porcentaje de ventas con tarifa 0%
    def test_porcentaje_ventas_tarifa_0_estructura_y_limites(self):
        porcentajes = self.analizador.porcentaje_ventas_tarifa_0_por_provincia()
        self.assertIsInstance(porcentajes, dict)
        
        for provincia, porcentaje in porcentajes.items():
            self.assertIsInstance(porcentaje, (float, int), 
                                  f"El porcentaje de {provincia} no es numérico.")
            
            self.assertGreaterEqual(porcentaje, 0, f"El porcentaje de {provincia} es negativo.")
            self.assertLessEqual(porcentaje, 100, f"El porcentaje de {provincia} excede el 100%.")
            
        if len(porcentajes) > 0:
            provincia_ejemplo = list(porcentajes.keys())[0]
            self.assertTrue(porcentajes[provincia_ejemplo] >= 0.0 and porcentajes[provincia_ejemplo] <= 100.0)