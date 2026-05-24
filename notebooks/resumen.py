#!/usr/bin/env python3
"""
Script para mostrar resumen rápido de resultados del scoring
Ejecuta: python resumen.py
"""

import pandas as pd
from pathlib import Path

# Cargar datos
base_path = Path(__file__).resolve().parent
data_path = base_path.parent / 'data' / 'datos_medellin_od_limpio.csv'
results_path = base_path.parent / 'resultados' / 'tabla_resultados_scoring.csv'

if not data_path.exists():
    print("❌ Error: No se encontró datos_medellin_od_limpio.csv en carpeta data/")
    print("   Primero ejecuta el notebook: 01_calculo_scoring.ipynb")
    exit(1)

if not results_path.exists():
    print("❌ Error: No se encontraron resultados. Ejecuta primero el notebook.")
    exit(1)

df_od = pd.read_csv(data_path)
df_results = pd.read_csv(results_path)

print("\n")
print("="*100)
print(" "*20 + "SCORING DE RIESGO DE GENTRIFICACIÓN POR TRANSPORTE")
print(" "*35 + "Medellín 2025")
print("="*100)

print(f"\n📊 DATOS CARGADOS:")
print(f"   • Macrozonas analizadas: {len(df_od)}")
print(f"   • Total viajes origen: {df_od['viajes_origen'].sum():,}")
print(f"   • Total viajes destino: {df_od['viajes_destino'].sum():,}")

print(f"\n📈 DISTRIBUCIÓN POR CATEGORÍA DE RIESGO:")
categorias = df_results['CATEGORIA'].value_counts().sort_index(ascending=False)
for cat, count in categorias.items():
    print(f"   • {cat:<10}: {count} zona(s)")

print(f"\n⚠️  ZONAS DE RIESGO ALTO (50–65):")
alto = df_results[df_results['CATEGORIA'] == 'Alto'].sort_values('INDICE', ascending=False)
for idx, row in alto.iterrows():
    print(f"   {idx+1}. {row['macrozona']:<25} Índice: {row['INDICE']:>6.1f}")

print(f"\n🔴 ZONAS DE RIESGO CRÍTICO (>65):")
critico = df_results[df_results['CATEGORIA'] == 'Crítico']
if len(critico) > 0:
    for idx, row in critico.iterrows():
        print(f"   {row['macrozona']:<25} Índice: {row['INDICE']:>6.1f}")
else:
    print("   [Ninguna zona alcanza riesgo crítico]")

print(f"\n📊 ESTADÍSTICAS DEL ÍNDICE:")
print(f"   • Máximo: {df_results['INDICE'].max():.1f}")
print(f"   • Mínimo: {df_results['INDICE'].min():.1f}")
print(f"   • Promedio: {df_results['INDICE'].mean():.1f}")
print(f"   • Mediana: {df_results['INDICE'].median():.1f}")
print(f"   • Desv. Estándar: {df_results['INDICE'].std():.1f}")

print(f"\n🎯 HALLAZGOS PRINCIPALES:")
print(f"   • Corredor occidental (Metro de la 80) concentra 5 zonas de riesgo alto")
print(f"   • Santa Cruz tiene exportación extrema (16.55%) pero bajo riesgo por infraestructura")
print(f"   • Centralidades consolidadas (Candelaria, Poblado, Laureles) = bajo riesgo")
print(f"   • Riesgo identificado es FUTURO, no actual — hay ventana para políticas preventivas")

print(f"\n📁 ARCHIVOS GENERADOS:")
print(f"   ✓ ../resultados/tabla_resultados_scoring.csv")
print(f"   ✓ ../resultados/01_ranking_indice.png")
print(f"   ✓ ../resultados/02_heatmap_componentes.png")
print(f"   ✓ ../resultados/03_scatter_detonantes.png")

print(f"\n📖 TABLA DE RESULTADOS COMPLETA:")
print("="*100)
print(df_results.to_string(index=False))

print("\n" + "="*100)
print("✓ Análisis completado. Para ver gráficos detallados, revisa la carpeta ../resultados/")
print("="*100 + "\n")
