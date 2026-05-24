# Movilidad Urbana y Riesgo de Gentrificación en Medellín

**Propuesta de índice exploratorio para la detección temprana de zonas vulnerables**

## Descripción del proyecto

Este proyecto desarrolla una **metodología de scoring** para identificar territorios de Medellín que podrían experimentar presión gentrificadora futura como consecuencia de mejoras en accesibilidad y conectividad urbana, con énfasis especial en el **Metro de la 80**.

A diferencia de estudios que buscan demostrar que la gentrificación ya ocurrió, este análisis busca **detectar zonas en la antesala del cambio**, antes de que el mercado inmobiliario reaccione y las políticas preventivas lleguen tarde.

## Hipótesis central

**El transporte masivo es un detonante poderoso de valorización urbana.** Cuando una zona pasa de estar desconectada a conectada mediante nueva infraestructura:

1. El tiempo de viaje se reduce dramáticamente
2. Esa accesibilidad se capitaliza en el precio del suelo
3. La zona se vuelve atractiva para poblaciones de mayor ingreso
4. Los residentes actuales (típicamente de menor ingreso) enfrentan presión de desplazamiento

## Datos utilizados

### Origen: Encuesta Origen-Destino AMVA 2025

- **Total de viajes:** 6.490.299 viajes en un día hábil
- **Ámbito:** Área Metropolitana del Valle de Aburrá
- **Desagregación:** 16 macrozonas de Medellín (datos urbanos)
- **Variables disponibles:** Origen, destino, modo de transporte, hora, estrato socioeconómico

**Fuente:** Área Metropolitana del Valle de Aburrá (AMVA), mayo de 2026

### Datos complementarios utilizados

- **Trazado oficial del Metro de la 80:** metrodela80.gov.co, Plan de Reasentimiento del Metro de Medellín (abril 2024), Plan de Desarrollo del Concejo de Medellín (2024)
- **Indicadores socioeconómicos por macrozona:** Alcaldía de Medellín (fichas comunales 2021), Metropol (indicadores de vivienda), Siciudadanía (ficha El Poblado 2022)

## Metodología del scoring

### Componentes del índice

El índice combina **5 componentes**, cada uno normalizado en escala 0–100:

| Componente | Descripción | Peso | Fuente |
|-----------|-------------|------|--------|
| **C1** | Exportación neta de viajes | 25% | EOD AMVA 2025 |
| **C2** | Exposición al Metro de la 80 | 25% | Trazado oficial |
| **C3** | Dependencia de transporte público | 20% | Alcaldía Medellín + Metropol |
| **C4** | Masa crítica de movilidad | 15% | EOD AMVA 2025 |
| **C5** | Potencial de atracción futura | 15% | EOD AMVA 2025 |

### Fórmulas

**C1 — Exportación neta de viajes:**
```
C1_raw = (Viajes_Origen - Viajes_Destino) / Viajes_Origen
C1 = MinMax(clip(C1_raw, 0)) [0, 100]
```
Mide la dependencia funcional externa. Zonas importadoras reciben C1=0 (son centralidades).

**C2 — Exposición al Metro de la 80:**
```
C2 = Score experto [0, 100]
  100 = Zonas en corredor directo del trazado (Castilla, Robledo, Laureles, La América, San Javier, Belén, Guayabal)
   50 = Zonas adyacentes con trasbordo potencial (La Candelaria)
   40 = Zonas adyacentes cercanas (Doce de Octubre)
  10-20 = Zonas fuera del corredor
```

**C3 — Dependencia de transporte público:**
```
C3 = Score basado en nivel socioeconómico [0, 100]
  100 = Extremo (Popular)
   85 = Muy Alto (Santa Cruz, Doce de Octubre, Villa Hermosa, Manrique, San Javier)
   65 = Alto (Robledo, Castilla, Aranjuez, Buenos Aires, Guayabal, La Candelaria)
   50 = Medio-Alto (Belén)
   35 = Medio (La América)
   20 = Bajo-Medio (Laureles-Estadio)
   10 = Bajo (El Poblado)
```

**C4 — Masa crítica de movilidad:**
```
C4 = MinMax(% viajes origen) [0, 100]
```
La Candelaria (8.64%, máximo) obtiene C4=100.

**C5 — Potencial de atracción futura:**
```
C5_raw = (1 - pct_destino_normalizado) × (C2 / 100)
C5 = MinMax(C5_raw) [0, 100]
```
Identifica zonas hoy periféricas que quedarán conectadas por infraestructura futura.

### Agregación

```
ÍNDICE = 0.25·C1 + 0.25·C2 + 0.20·C3 + 0.15·C4 + 0.15·C5
```

**Justificación de pesos:**
- C1 + C2 = 50%: Capturan el **detonante principal** (exportación + infraestructura)
- C3 = 20%: Determina **QUIÉN** es vulnerable al desplazamiento
- C4 + C5 = 30%: Condiciones **moduladoras** (masa crítica + potencial futuro)

### Categorización

| Categoría | Rango | Interpretación |
|-----------|-------|----------------|
| Crítico | > 65 | Múltiples factores de vulnerabilidad convergen con alta exposición a infraestructura |
| Alto | 50–65 | Combinación significativa de al menos dos factores de riesgo |
| Medio | 35–50 | Factores presentes pero sin convergencia crítica |
| Bajo | < 35 | Centralidad consolidada o baja exposición a infraestructura |

## Resultados principales

### Zonas de riesgo alto

5 macrozonas alcanzan categoría de **riesgo alto** (50–65):

1. **San Javier** (59.8) — Corredor directo + muy alta dependencia TP + estrato bajo
2. **Guayabal** (56.0) — Máximo potencial de atracción futura + baja densidad hoy
3. **Robledo** (54.5) — Máxima exposición infraestructura + sector universitario
4. **Castilla** (54.0) — Punto de inicio del corredor + dependencia TP alta
5. **Belén** (52.0) — Corredor suroccidental + masa crítica significativa

**Patrón territorial:** Todas coinciden con el trazado oficial del Metro de la 80.

### Caso especial: Santa Cruz

- **Índice:** 46.2 (riesgo medio)
- **Razón:** Mayor exportador neto de viajes (16.55% de ratio de exportación) pero **fuera del corredor del Metro de la 80**
- **Implicación:** Su riesgo es real pero opera por desbordamiento desde el norte, no por infraestructura propia

### Centralidades consolidadas

La Candelaria, El Poblado y Laureles-Estadio obtienen bajo riesgo porque ya son destinos de viajes consolidados. Su condición de centralidad establece un mecanismo de amortiguación: el precio del suelo ya refleja su accesibilidad.

## Estructura del repositorio

```
gentrificacion-medellin/
│
├── README.md                              # Este archivo
├── requirements.txt                       # Dependencias del proyecto
├── gitignore                              # Archivos ignorados por Git
│
├── data/
│   └── datos_medellin_od_limpio.csv      # Datos de origen-destino limpios
│
├── notebooks/
│   ├── 01_calculo_scoring.ipynb          # Notebook con cálculos completos
│   └── resumen.py                        # Script de resumen rápido de resultados
│
├── resultados/
│   ├── tabla_resultados_scoring.csv      # Tabla final de resultados
│   ├── 01_ranking_indice.png             # Gráfico de ranking
│   ├── 02_heatmap_componentes.png        # Heatmap de componentes
│   └── 03_scatter_detonantes.png         # Scatter C1 vs C2
│
└── src/                                   # Carpeta reservada para scripts adicionales
```

## Cómo reproducir los cálculos

### Requisitos

```bash
python >= 3.8 , <= 3.14
pandas >= 1.2
numpy >= 1.20
matplotlib >= 3.3
seaborn >= 0.11
jupyter >= 1.0
```

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/usuario/gentrificacion-medellin.git
cd gentrificacion-medellin

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar el análisis

```bash
# Iniciar Jupyter
jupyter notebook notebooks/01_calculo_scoring.ipynb
```

El notebook ejecuta todos los cálculos paso a paso y genera:
- Tabla de resultados en CSV
- 3 visualizaciones en PNG
- Análisis de sensibilidad
- Validaciones de integridad

## Limitaciones y trabajo futuro

### Limitaciones actuales

1. **Escala de agregación:** El análisis opera a nivel de macrozona, que agrupa barrios heterogéneos. Fase 2 descenderá a nivel de barrio.

2. **Componentes C2 y C3 basados en juicio experto:** Sin datos georreferenciados precisos de distancia a estaciones y sin datos de modo de transporte desagregados por zona de la EOD.

3. **Ausencia de variables de resultado:** El índice predice riesgo relativo pero no valida contra precios de vivienda reales ni cambio socioeconómico documentado.

4. **Ponderación no validada empíricamente:** Los pesos reflejan razonamiento teórico. Análisis de sensibilidad incluido en el notebook muestra robustez del ranking.

5. **Corte transversal:** La EOD 2025 es un corte en el tiempo. Se requieren encuestas posteriores para validar dinámicamente.

### Agenda de trabajo futuro

**Fase 2:** Integración de variables complementarias
- Precios de vivienda por m² (datos catastrales, Lonja de Propiedad Raíz, portales inmobiliarios)
- Densidad de comercio formal (DIAN, Cámara de Comercio de Medellín)
- Tasa de permanencia residencial (DANE, SISBEN)
- Desagregación a escala de barrio (UGEL)

**Fase 3:** Validación post-apertura del Metro de la 80
- Contrastación del índice con precios reales observados
- Identificación de escenarios de riesgo 2025–2032
- Análisis de ventanas de oportunidad para políticas preventivas

## Referencias

### Gentrificación y transporte

- Sabatini, F., Cáceres, G., & Cerda, J. (2001). Segregación residencial en las principales ciudades chilenas. *EURE*, 27(82), 21–42.
- Delmelle, E. C., & Casas, I. (2012). Evaluating spatial equity of bus rapid transit accessibility. *Transport Policy*, 20, 36–46.
- Contreras, Y. (2011). La recuperación urbana y residencial del centro de Santiago. *EURE*, 37(112), 89–113.
- Smith, N. (1987). Gentrification and the rent gap. *Annals of the Association of American Geographers*, 77(3), 462–465.
- Lees, L., Slater, T., & Wyly, E. (2008). *Gentrification*. Routledge.

### Datos y contexto local

- AMVA. (2026). *Encuesta Origen-Destino 2025*. Medellín: AMVA.
- Alcaldía de Medellín. (2021). Fichas informativas de comunas. Recuperado de https://www.medellin.gov.co
- Metro de Medellín. (2024). Plan de reasentamiento general Metro de la 80. Recuperado de https://www.metrodemedellin.gov.co
- Metro de la 80. (2024). Sobre el proyecto. Recuperado de https://metrodela80.gov.co

## Autores

Propuesta investigativa de pregrado — Universidad [Tu Universidad]
Elaborado en 2025

## Licencia

[Especificar licencia: MIT, CC-BY-4.0, etc.]

## Contacto

Para preguntas o sugerencias sobre la metodología, contactar a: [email]

---

**Nota importante:** Este proyecto busca generar una **alerta temprana** para que las políticas preventivas puedan anticiparse al fenómeno, no reaccionar después de que ocurra. La gentrificación inducida por transporte no es inevitable: ocurre cuando la inversión en infraestructura llega sin mecanismos de protección del suelo.
