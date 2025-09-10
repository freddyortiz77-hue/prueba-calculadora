# SimToolkit – Calculadora de Pruebas Estadísticas

**Autor:** freddy ortiz   
**Curso:** decimo semestre  
**Fecha:** 2025/09/09

## Resumen
Aplicación en Python 3.10+ que implementa generadores (Cuadrados Medios, Multiplicador Constante) y pruebas estadísticas (Media, Varianza, Chi²). GUI en Tkinter.

## Requisitos
- Python 3.10+
- numpy
- matplotlib

Instalación:
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

SimToolkit_Pruebas_Calculadora/
├── README.md
├── requirements.txt
└── src/
    ├── main.py
    ├── gui.py
    ├── generators.py
    ├── tests.py
    └── utils.py
| Fecha      | Clase # | Actividad principal                 | Archivos añadidos / modificados | Observaciones            |
| ---------- | ------- | ----------------------------------- | ------------------------------- | ------------------------ |
| 2025-09-01 | Clase 1 | Implementación LCG y middle-square  | `generators.py`, `README.md`    | PRIMERA ENT.             |
| 2025-09-05 | Clase 2 | Pruebas de media y varianza         | `tests.py`                      | Añadir p-valores después |
| 2025-09-08 | Clase 3 | GUI básica y exportación de CSV/PNG | `gui.py`, `utils.py`            | Interfaz lista           |
