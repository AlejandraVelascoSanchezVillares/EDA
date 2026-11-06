# Criminalidad en Europa y riesgo asegurador

Análisis exploratorio (EDA) de los delitos registrados por la policía en Europa, con datos de Eurostat, para una aseguradora que quiere ajustar sus primas según la criminalidad de cada país y el tipo de delito.

El resultado es un **factor orientativo de prima por país y ramo de seguro** (hogar, automóvil, comercios, vida y accidentes, ciberriesgo, crimen financiero y RC medioambiental) y una agrupación de países en **tres zonas de riesgo**.

## Preguntas que responde

- ¿Qué tipos de delito son más frecuentes y cuáles son residuales?
- ¿Las tasas siguen una distribución normal?
- ¿Qué países están por encima o por debajo de la mediana europea en los delitos que afectan a cada ramo?
- ¿Qué delitos se mueven juntos?
- ¿Cómo han evolucionado desde 2008 y qué países empeoran?
- ¿Qué ajuste de prima orientativo sale para cada combinación país × ramo?

## Datos

- **Fuente:** Eurostat, conjunto [`crim_off_cat`](https://ec.europa.eu/eurostat/web/crime/information-data): delitos registrados por la policía por categoría.
- **Cobertura:** 41 territorios europeos, 25 categorías de la clasificación internacional ICCS, años 2008–2024.
- **Unidades:** número de delitos (`NR`) y tasa por 100.000 habitantes (`P_HTHAB`).

> **Aviso:** Eurostat advierte que comparar niveles de delincuencia entre países puede llevar a conclusiones erróneas, porque cambian las definiciones legales, las reglas de recuento y la propensión a denunciar, y recomienda centrarse en tendencias. El método de este proyecto amortigua las diferencias de nivel y da peso a la tendencia.

## Estructura del repositorio

```
├── data/
│   └── estat_crim_off_cat.tsv                 # datos de Eurostat (TSV original)
├── eda_criminalidad_aseguradora.ipynb         # notebook con todo el análisis
├── factores_riesgo_pais_ramo.csv              # resultado: factor por país y ramo
├── presentacion_criminalidad_aseguradora.pptx # presentación de resultados
├── utils.py                                   # diccionario ICCS en español
└── README.md
```

## Cómo ejecutarlo

1. Instala las dependencias:

```bash
   pip install "pandas>=2.2" numpy matplotlib "seaborn>=0.13" scipy scikit-learn
```

2. Coloca el fichero de Eurostat en `data/estat_crim_off_cat.tsv` (o cambia `RUTA_DATOS` en el notebook).
3. Ejecuta el notebook de principio a fin. Al terminar genera `factores_riesgo_pais_ramo.csv`.

## Contenido del notebook

1. **Carga y limpieza:** del formato TSV "ancho" de Eurostat a formato largo; separación de unidades y tratamiento de valores no disponibles (`:`).
2. **Calidad y cobertura:** qué años, países y delitos tienen dato.
3. **Frecuencia y distribuciones:** tasas por delito, test de normalidad (Shapiro-Wilk) y escala logarítmica.
4. **Comparación entre países:** relatividad frente a la mediana europea y ranking en delitos clave.
5. **Correlaciones:** qué delitos se mueven juntos (Spearman).
6. **Volatilidad y tamaño del país:** por qué los países pequeños necesitan credibilidad.
7. **Tendencias:** evolución 2008–2024 (índice 2016 = 100) y cambio anual por país (pendiente de Theil–Sen).
8. **Índice de riesgo y factor de prima** por país y ramo.
9. **Zonas de riesgo:** agrupación de países con K-means.
10. **Conclusiones, limitaciones y próximos pasos.**

## Metodología del factor de prima

Para cada país y delito:

1. **Nivel:** tasa del país ÷ mediana europea (relatividad), recortada entre ¼ y 4.
2. **Credibilidad:** con pocos casos, el país se acerca a la mediana. `Z = min(1, √(n / 1.082))`, con `n` = delitos registrados en 2021–2024 (criterio clásico de credibilidad de fluctuación limitada).
3. **Tendencia:** cambio anual 2016–2024 estimado con la pendiente de Theil–Sen sobre el logaritmo de la tasa, robusta a años atípicos como 2020.

Para cada ramo:

4. **Agregación:** media geométrica ponderada de los delitos del ramo (solo si hay datos de al menos el 50 % del peso).
5. **Factor final:** `índice_nivel ^ elasticidad × factor_tendencia`, acotado entre 0,75 y 1,35.

### Ramos y pesos

| Ramo | Delitos (peso) |
|---|---|
| Hogar | Robo en vivienda (2), hurto (1) |
| Automóvil | Robo de vehículo a motor (1) |
| Comercios y pymes | Robo con fuerza (2), robo con violencia (1), fraude (1) |
| Vida y accidentes | Homicidio (2), agresión grave (2), tentativa de homicidio (1), secuestro (1) |
| Ciberriesgo | Ataques a sistemas informáticos (2), fraude (1) |
| Crimen financiero (D&O) | Corrupción (1), blanqueo de capitales (1), organización criminal (1) |
| RC medioambiental | Contaminación, residuos, especies protegidas, recursos naturales (1 cada uno) |

### Parámetros

| Parámetro | Valor | Significado |
|---|---|---|
| `VENTANA` | 2021–2024 | Años usados para comparar niveles |
| `PERIODO_TEND` | 2016–2024 | Años usados para estimar tendencias |
| `N_PLENA_CREDIBILIDAD` | 1.082 | Casos necesarios para credibilidad plena |
| `TOPE_RELATIVIDAD` | 4 | Recorte de la relatividad (entre ¼ y 4) |
| `ELASTICIDAD` | 0,25 | Cuánto se traslada el nivel de criminalidad a la prima |
| `HORIZONTE` | 2 años | Proyección de la tendencia hasta la vigencia de la póliza |
| `TOPE_TENDENCIA` | ±10 % | Límite del factor de tendencia |
| `FACTOR_MIN`, `FACTOR_MAX` | 0,75 – 1,35 | Límites del factor final |

> Los pesos, la elasticidad, el horizonte y los topes son **supuestos de negocio**, no estimaciones. Deben calibrarse con la siniestralidad de la aseguradora. Todos están en una misma celda del notebook para poder cambiarlos.

## Resultados principales

- **Los robos caen:** en el país mediano, el robo en vivienda está un 46 % por debajo de 2016 y el robo de vehículos un 30 %.
- **El fraude y los ciberataques suben:** +71 % y +58 % desde 2016, en más del 80 % de los países.
- **Solo el homicidio es comparable entre países:** el país más alto multiplica por menos de 5 al más bajo; en agresión grave la distancia es de unas 550 veces y en corrupción de unas 1.800, lo que refleja diferencias de definición y registro.
- **Infradenuncia:** el homicidio se correlaciona negativamente con los delitos contra la propiedad. Hipótesis: parte de la criminalidad patrimonial registrada refleja la penetración del seguro, porque sin denuncia no se cobra el siniestro.
- **Factor por ramo (país mediano):** Hogar −9 %, Automóvil −3 %, Ciberriesgo +9 %, Crimen financiero +13 %.
- **España:** Comercios y pymes (1,33) y Ciberriesgo (1,23) son los ramos con mayor recargo; Hogar (1,04) y Automóvil (0,97) quedan casi neutros porque la bajada de los robos compensa su nivel alto.
- **Tres zonas de riesgo:**
  - **Bajo:** Europa central y del este, Bálticos y Balcanes.
  - **Medio:** sur de Europa, España, Austria, Suiza, Países Bajos, Dinamarca, Finlandia, Islandia y Malta.
  - **Alto:** Alemania, Bélgica, Francia, Luxemburgo y Suecia.

## Limitaciones

- Son delitos **registrados por la policía**, no delitos ocurridos ni siniestros: falta lo que no se denuncia.
- La tasa es por habitante, no por póliza ni por bien asegurado.
- El fichero no incluye las banderas de Eurostat, así que no se ven las rupturas de serie (por ejemplo, Luxemburgo en robo de vehículos salta de ≈50 a ≈260 por 100.000 habitantes en 2019).
- Reino Unido (datos hasta 2018), Bosnia y Herzegovina (2012) y Kosovo (2021) quedan fuera de la comparación reciente.

## Próximos pasos

- Calibrar pesos y elasticidad con la siniestralidad de la aseguradora, por ejemplo incluyendo el índice como variable en un GLM de frecuencia de siniestros.
- Bajar a nivel regional con los datos NUTS 3 de Eurostat.
- Corregir la infradenuncia con encuestas de victimización y variables de contexto (PIB per cápita, penetración del seguro, urbanización).
- Volver a descargar los datos con banderas para detectar rupturas de serie.

## Autora

Alejandra Velasco Sánchez-Villares
