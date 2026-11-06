import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

pd.set_option("display.max_columns", 40)
pd.set_option("display.width", 200)
pd.set_option("display.precision", 2)
pd.set_option("display.max_colwidth", 200)

ICCS_ES = {
    "ICCS0101": "Homicidio intencionado",
    "ICCS0102": "Tentativa de homicidio",
    "ICCS020111": "Agresión grave",
    "ICCS020221": "Secuestro",
    "ICCS0301": "Violencia sexual",
    "ICCS03011": "Violación",
    "ICCS03012": "Agresión sexual",
    "ICCS0302": "Explotación sexual",
    "ICCS030221": "Pornografía infantil",
    "ICCS0401": "Robo con violencia o intimidación",
    "ICCS0501": "Robo con fuerza (todo tipo de inmueble)",
    "ICCS05012": "Robo en vivienda",
    "ICCS0502": "Hurto",
    "ICCS05021": "Robo de vehículo a motor",
    "ICCS0601": "Delitos de drogas",
    "ICCS0701": "Fraude",
    "ICCS0703": "Corrupción",
    "ICCS07031": "Soborno",
    "ICCS07041": "Blanqueo de capitales",
    "ICCS0903": "Ataques a sistemas informáticos",
    "ICCS09051": "Pertenencia a organización criminal",
    "ICCS1001": "Contaminación o degradación ambiental",
    "ICCS1002": "Traslado o vertido ilegal de residuos",
    "ICCS1003": "Tráfico de especies protegidas",
    "ICCS1004": "Agotamiento de recursos naturales",
}

# hija -> madre (para no sumar dos veces)
JERARQUIA = {"ICCS03011": "ICCS0301", "ICCS03012": "ICCS0301", "ICCS030221": "ICCS0302",
             "ICCS05012": "ICCS0501", "ICCS05021": "ICCS0502", "ICCS07031": "ICCS0703"}

PAISES = {
    "AL": "Albania", "AT": "Austria", "BA": "Bosnia y Herzegovina", "BE": "Bélgica", "BG": "Bulgaria",
    "CH": "Suiza", "CY": "Chipre", "CZ": "Chequia", "DE": "Alemania", "DK": "Dinamarca", "EE": "Estonia",
    "EL": "Grecia", "ES": "España", "FI": "Finlandia", "FR": "Francia", "HR": "Croacia", "HU": "Hungría",
    "IE": "Irlanda", "IS": "Islandia", "IT": "Italia", "LI": "Liechtenstein", "LT": "Lituania",
    "LU": "Luxemburgo", "LV": "Letonia", "ME": "Montenegro", "MK": "Macedonia del Norte", "MT": "Malta",
    "NL": "Países Bajos", "NO": "Noruega", "PL": "Polonia", "PT": "Portugal", "RO": "Rumanía",
    "RS": "Serbia", "SE": "Suecia", "SI": "Eslovenia", "SK": "Eslovaquia", "TR": "Turquía",
    "UKC-L": "Inglaterra y Gales", "UKM": "Escocia", "UKN": "Irlanda del Norte", "XK": "Kosovo",
}
UE27 = {"AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR", "HU", "IE", "IT",
        "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK"}
AELC = {"CH", "IS", "LI", "NO"}

RAMOS = {
    "Hogar":                       {"ICCS05012": 2, "ICCS0502": 1},
    "Automóvil":                   {"ICCS05021": 1},
    "Comercios y pymes":           {"ICCS0501": 2, "ICCS0401": 1, "ICCS0701": 1},
    "Vida y accidentes":           {"ICCS0101": 2, "ICCS0102": 1, "ICCS020111": 2, "ICCS020221": 1},
    "Ciberriesgo":                 {"ICCS0903": 2, "ICCS0701": 1},
    "Crimen financiero (D&O)":     {"ICCS0703": 1, "ICCS07041": 1, "ICCS09051": 1},
    "RC medioambiental":           {"ICCS1001": 1, "ICCS1002": 1, "ICCS1003": 1, "ICCS1004": 1},
}

def grupo_pais(geo):
    if geo in UE27:
        return "UE-27"
    if geo in AELC:
        return "AELC"
    if geo.startswith("UK"):
        return "Reino Unido"
    return "Candidatos y otros"

# Paleta: un color por serie, gris para el contexto,
# rampa azul para magnitudes y azul <-> rojo (centro gris) para "por debajo / por encima de la mediana"
AZUL, NARANJA, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
GRIS_CONTEXTO = "#c3c2b7"
TINTA, TINTA_2, TINTA_SUAVE = "#0b0b0b", "#52514e", "#898781"
SUPERFICIE, REJILLA = "#fcfcfb", "#e1e0d9"

SECUENCIAL = LinearSegmentedColormap.from_list(
    "azul", ["#f0efec", "#b7d3f6", "#6da7ec", "#2a78d6", "#1c5cab", "#0d366b"])
DIVERGENTE = LinearSegmentedColormap.from_list(
    "azul_rojo", ["#104281", "#3987e5", "#b7d3f6", "#f0efec", "#f4b9b8", "#e34948", "#9e2b2b"])

mpl.rcParams.update({
    "figure.facecolor": SUPERFICIE, "axes.facecolor": SUPERFICIE, "savefig.facecolor": SUPERFICIE,
    "axes.edgecolor": GRIS_CONTEXTO, "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": REJILLA, "grid.linewidth": 0.6, "grid.linestyle": "-",
    "axes.axisbelow": True,
    "text.color": TINTA, "axes.labelcolor": TINTA_2, "axes.titlecolor": TINTA,
    "xtick.color": TINTA_SUAVE, "ytick.color": TINTA_SUAVE,
    "xtick.labelcolor": TINTA_2, "ytick.labelcolor": TINTA_2,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.frameon": False, "legend.fontsize": 9,
    "lines.linewidth": 2,
    "figure.dpi": 100,
})