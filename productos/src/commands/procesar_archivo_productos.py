import pandas as pd
from src.commands.base_command import BaseCommand



columnas_requeridas = {'id_fabricante', 'nombre', 'valorUnitario', 'volumen'}

class ProcesarArchivoProductos(BaseCommand):
    def __init__(self, archivo, nombre_archivo: str):
        self.archivo = archivo
        self.nombre_archivo = nombre_archivo
    
    def validar_columnas(self, df):
        return columnas_requeridas.issubset(df.columns)

    def execute(self):
        try:
            if self.nombre_archivo.endswith(".csv"):
                df = pd.read_csv(self.archivo)
            elif self.nombre_archivo.endswith("xlsx"):
                df = pd.read_excel(self.archivo)
            elif self.nombre_archivo.endswith("json"):
                df = pd.read_json(self.archivo)
            else:
                return {
                    "response": {"msg": "Formato de archivo no soportado"},
                    "status_code": 400,
                }
            
            if not self.validar_columnas(df):
                return {
                    "response": {"msg": "El archivo no contiene las columnas requeridas"},
                    "status_code": 400,
                }
            
            productos = {"response": {'payload': df.to_dict(orient="records")}, 'status_code': 200}
            return productos
        
        except Exception as e:
            return {
                    "response": {"msg": f"Ha ocurrido un error al procesar el archivo: {e}"},
                    "status_code": 500,
                }