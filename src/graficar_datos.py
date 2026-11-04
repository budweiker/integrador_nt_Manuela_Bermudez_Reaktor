if __package__:
    from .reporte_datos import generar_reportes
else:
    from reporte_datos import generar_reportes


if __name__ == "__main__":
    from pathlib import Path

    generar_reportes(Path(__file__).resolve().parents[1])
