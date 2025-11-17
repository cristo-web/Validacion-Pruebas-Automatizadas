from src.procesador import Analizador

def main():
    archivo = "datos/sri_ventas_2024.csv"
    analizador = Analizador(archivo)
    
    if not analizador.datos:
        print("No se pudo cargar el archivo CSV o está vacío. Terminando.")
        return

    # 1. VENTAS TOTALES POR PROVINCIA
    print("--- 1. Ventas Totales por Provincia ---")
    resumen = analizador.ventas_totales_por_provincia()
    for prov, total in resumen.items():
        print(f"\t{prov.ljust(15)}: ${total:,.2f}")
    
    # 2. CONSULTA INDIVIDUAL DE 3 PROVINCIAS
    print("\n--- 2. Consultar Ventas de Tres Provincias ---")
    
    for i in range(3):
        provincia = input(f"\tIngrese el nombre de la provincia #{i+1}: ")
        ventas = analizador.ventas_por_provincia(provincia)
        
        nombre_impresion = provincia.upper() if ventas > 0.0 else provincia
        print(f"\tVentas de {nombre_impresion.ljust(15)}: ${ventas:,.2f}")
        
        if ventas == 0.0:
            print("\t(Advertencia: Provincia no encontrada o con ventas de 0.0)")

    # 3. ESTADÍSTICA ADICIONAL 1: Exportaciones por mes
    print("\n--- 3. Exportaciones Totales por Mes ---")
    exportaciones_mes = analizador.exportaciones_por_mes()
    for mes, total_exp in exportaciones_mes.items():
        print(f"\tMes {str(mes).ljust(2)}: ${total_exp:,.2f}")

    # 4. ESTADÍSTICA ADICIONAL 2: Provincia con más Importaciones
    print("\n--- 4. Provincia con Mayor Volumen de Importaciones ---")
    provincia_max, valor_max = analizador.provincia_con_mas_importaciones()
    print(f"\tProvincia: {provincia_max}")
    print(f"\tTotal Importaciones: ${valor_max:,.2f}")

    # 5. ESTADÍSTICA ADICIONAL 3: Porcentaje de ventas con tarifa 0%
    print("\n--- 5. Porcentaje de Ventas Tarifa 0% por Provincia (Top 5) ---")
    porcentajes_cero = analizador.porcentaje_ventas_tarifa_0_por_provincia()
    top_5 = sorted(porcentajes_cero.items(), key=lambda item: item[1], reverse=True)[:5]
    
    if not top_5:
         print("\tN/A: No hay datos para calcular porcentajes.")
         return

    for prov, porcentaje in top_5:
        print(f"\t{prov.ljust(15)}: {porcentaje:.2f}%")


if __name__ == "__main__":
    main()