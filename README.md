# Informe de Práctica: Validación del Software (Práctica 03)

## Autor 
* **Nombre:** Cristopher 
* **Tema:** Validación del software a través de pruebas automatizadas 

---

## 🔬 Descripción del Proyecto

Este proyecto se centra en la implementación y ejecución de **pruebas unitarias** usando la librería `unittest` de Python para garantizar la calidad y la coherencia de un módulo de análisis de datos (`Analizador`) que procesa información de ventas del SRI de 2024.

### 🛠️ Funcionalidades Base Implementadas (Paso 2-4)

La clase `Analizador` (`src/procesador.py`) implementa las siguientes funciones requeridas:
1.  **Cálculo de ventas totales por provincia** (`ventas_totales_por_provincia`).
2.  **Consulta de ventas** para una provincia específica (`ventas_por_provincia`).
3.  **Validaciones de pruebas unitarias** que cubren el retorno de tipo (diccionario), la coherencia del número de provincias, la verificación de valores no negativos, y la existencia de provincias consultadas.

### 🚀 Estadísticas de Extensión (Trabajo Autónomo)

Se implementaron **tres estadísticas adicionales** para el trabajo autónomo, asegurando la máxima cobertura funcional:

| No. | Estadística Implementada | Columna(s) de Datos |
| :---: | :--- | :--- |
| **1** | Exportaciones totales por mes | `EXPORTACIONES`, `MES` |
| **2** | Provincia con mayor volumen de importaciones | `IMPORTACIONES`, `PROVINCIA` |
| **3** | Porcentaje de ventas con Tarifa 0% | `VENTAS_NETAS_TARIFA_0`, `TOTAL_VENTAS` |

---

## 📊 Cobertura de Código (`coverage.py`)

Se utilizó la librería `coverage` de Python para medir la efectividad de las pruebas unitarias sobre el código de la aplicación. El proceso consistió en ejecutar las pruebas usando `coverage run -m unittest discover tests` y generar el informe final con `coverage report -m`.

## 📊 Cobertura de Código

| Name | Stmts | Miss | Cover | Missing |
| :--- | :---: | :---: | :---: | :---: |
| src\procesador.py | 26 | 0 | 100% | |
| tests\test_analizador.py | 26 | 1 | 96% | 40 |
| **TOTAL** | **52** | **1** | **98%** | |
---

## ✅ Conclusiones del Aprendizaje

1.  Se comprendió cómo utilizar el módulo `unittest` para validar funciones de forma estructurada y automática.

2.  Se aprendió a diseñar casos de prueba que permiten verificar tanto resultados correctos (Golden Path) como comportamientos erróneos (manejo de provincias inexistentes), fortaleciendo la confiabilidad del software.