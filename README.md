# 🏛️ XV Legislatura — Salario de los Diputados y Gobierno de España

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)
![Dataset](https://img.shields.io/badge/Dataset-Elaboración%20propia-blue?style=for-the-badge)

## 📌 Descripción

Dashboard interactivo sobre las retribuciones de todos los diputados (activos y bajas) de la **XV Legislatura del Congreso de los Diputados de España**, incluyendo también los miembros del Gobierno.

El proyecto responde a una pregunta central:

> **¿Cuántos diputados cobran más que el Presidente del Gobierno?**

Y va más allá, analizando la estructura salarial completa: salario base, dietas y suplementos, desglosados por grupo parlamentario, partido político y circunscripción.

---

## 📊 Hallazgos principales

| Indicador | Valor |
|---|---|
| Total diputados en la legislatura | 350 |
| Diputados que superan el salario del Presidente | 44 (11,92%) |
| Salario bruto anual mínimo | 61.591 € |
| Salario bruto anual máximo | 230.912 € (Presidenta del Congreso) |
| Salario del Presidente del Gobierno | 110.397 € |
| Salario medio mensual | 7.036 € |
| Media de dietas | 1.938 € |
| Media de suplementos | 1.481 € |
| Composición por género | 55,01% hombres · 44,99% mujeres |

---

## 🗂️ Estructura del repositorio

```
📦 xv-legislatura-salarios
 ┣ 📂 data
 ┃ ┗ 📄 diputados_transpatentia.xlsx     # Dataset completo (activos + bajas)
 ┃ ┗ 📄salario_congreso.py               # Web Scrapping de Transparentia de Newtral para recoger los salarios
 ┣ 📂 powerbi
 ┃ ┗ 📄 dashboard_diputados.pbix          # Dashboard Power BI
 ┗ 📄 README.md
```

---

## 📋 Dataset

El dataset ha sido compilado manualmente a partir de fuentes oficiales e incluye **todos los diputados** de la XV Legislatura, tanto activos como bajas por sustitución.

### Columnas principales

| Campo | Descripción |
|---|---|
| `ID_DIPUTADO` | Identificador único |
| `DIPUTADO` | Nombre completo |
| `CARGO` | Cargo en el Congreso |
| `CIRCUNSCRIPCIÓN` | Provincia de elección |
| `LEGISLATURA` | XV Legislatura |
| `GRUPO_PARLAMENTARIO_INICIAL` | Grupo al inicio de la legislatura |
| `GRUPO_PARLAMENTARIO_ACTUAL` | Grupo en el momento del registro |
| `PARTIDO_POLITICO_ACTUAL` | Partido político |
| `FECHA_INICIO_LEGISLATURA` | Fecha de incorporación |
| `FECHA_FIN_LEGISLATURA` | Fecha de baja (si aplica) |
| `SUSTITUYE_A` | Diputado al que sustituye |
| `SUSTITUIDO_POR` | Diputado que lo sustituye |
| `ACTIVO` | Estado actual (Sí/No) |
| `SALARIO_BRUTO_ANUAL` | Retribución bruta anual (€) |
| `SALARIO_BRUTO_MENSUAL` | Retribución bruta mensual (€) |
| `SALARIO_BASE` | Salario base (€) |
| `DIETAS` | Dietas (€) |
| `SUPLEMENTOS` | Suplementos (€) |
| `COORD_X` | Longitud (para mapas) |
| `COORD_Y` | Latitud (para mapas) |

### Fuentes
- [Congreso de los Diputados](https://www.congreso.es)
- [BOE — Retribuciones de altos cargos](https://www.boe.es)
- [Transparentia Buscador - Newtral](https://transparentia.newtral.es/buscador)

---

## 📈 Dashboard Power BI

### Visualizaciones incluidas

- **KPIs principales** — total diputados, superan umbral presidencial, salario mín/máx/medio
- **Desglose salarial** — salario base, dietas y suplementos en tarjetas separadas
- **Histograma** — distribución salarial con línea de referencia presidencial
- **Tabla por grupo parlamentario** — media salarial ordenada de mayor a menor
- **Hemiciclo** — composición del Congreso por grupo parlamentario
- **Tabla detallada** — todos los diputados con formato condicional
- **Filtros interactivos** — por órgano, activo/inactivo y partido político

### Medidas DAX principales

```dax
-- Diputados que superan el salario de la Presidenta
Diputados > Presidente = 
CALCULATE(
    COUNTROWS('Tabla1'),
    FILTER(
        'Tabla1',
        'Tabla1'[SALARIO_BRUTO_ANUAL] > [Salario Presidente]
    )
)

-- Porcentaje sobre el total
% Diputados con mayor SBA = 
CALCULATE(
    DIVIDE(Tabla1[Diputados > Presidente],COUNTROWS(Tabla1),0)*100)
```

---

### Resultado final
<img width="1279" height="722" alt="image" src="https://github.com/user-attachments/assets/d8d80ae2-f983-41dd-89f9-bed75304c7ea" />


## 🛠️ Requisitos

- Microsoft Power BI Desktop (gratuito) — [Descargar aquí](https://powerbi.microsoft.com/es-es/desktop/)
- Microsoft Excel (para explorar el dataset)

---

## 👤 Autor

**Vini** — Analista de datos con formación en Ciencia Política, Sociología y Big Data.

Portfolio orientado a roles de **Data Analyst** y **Data Scientist**, con proyectos aplicados a datos públicos y político-institucionales.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Conectar-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/marco-vinicio-ayala-sierra/)
[![GitHub](https://img.shields.io/badge/GitHub-Portfolio-181717?style=flat&logo=github)](https://github.com/marco24aya)

---

## 📄 Licencia

Los datos son de elaboración propia a partir de fuentes públicas oficiales.
El código y el dashboard son de libre uso con atribución al autor.
