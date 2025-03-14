import pandas as pd
import pymssql
import os
import zipfile
from sqlalchemy import create_engine

# Configurar conexión a SQL Server
server = 'server-sql-grupo1.database.windows.net'
database = 'NBA'
username = 'Admon'
password = 'Password.Server1'

# Crear el engine usando pymssql
connection_string = f"mssql+pymssql://{username}:{password}@{server}/{database}"
engine = create_engine(connection_string)

# Función para procesar datos
def process_data():
    # Montar Google Drive (si es necesario, omitir en Docker)
    # kaggle_json_path = "/content/drive/My Drive/Proyecto Final/kaggle.json"
    # os.makedirs("/root/.kaggle", exist_ok=True)
    # !mv kaggle.json /root/.kaggle/
    # !chmod 600 /root/.kaggle/kaggle.json

    # Descargar el dataset de Kaggle
    os.system('kaggle datasets download -d wyattowalsh/basketball')

    # Extraer los archivos en una carpeta llamada "basketball_data"
    with zipfile.ZipFile("basketball.zip", "r") as zip_ref:
        zip_ref.extractall("basketball_data")

    # Leer los archivos CSV
    df_game = pd.read_csv("basketball_data/csv/game.csv")
    df_team_details = pd.read_csv('basketball_data/csv/team_details.csv')
    df_other_stats = pd.read_csv('basketball_data/csv/other_stats.csv')
    df_line = pd.read_csv('basketball_data/csv/line_score.csv')
    df_common_player = pd.read_csv('basketball_data/csv/common_player_info.csv')
    df_draft_history = pd.read_csv('basketball_data/csv/draft_history.csv')
    df_game_info = pd.read_csv('basketball_data/csv/game_info.csv')
    df_play_by_play = pd.read_csv('basketball_data/csv/play_by_play.csv')

    # Aquí va el resto del procesamiento de datos que proporcionaste
    # (eliminar columnas, renombrar, filtrar, etc.)

    # Guardar los DataFrames procesados en CSV
    df_game.to_csv('df_game.csv', index=False)
    df_team_details.to_csv('df_team_details.csv', index=False)
    df_other_stats.to_csv('df_other_stats.csv', index=False)
    df_line.to_csv('df_line.csv', index=False)
    df_common_player.to_csv('df_common_player.csv', index=False)
    df_draft_history.to_csv('df_draft_history.csv', index=False)
    df_game_info.to_csv('df_game_info.csv', index=False)

    # Cargar los DataFrames en la base de datos
    dfs_to_load = {
        'df_team_details': df_team_details,
        # Agregar otros DataFrames si es necesario
    }

    for table_name, df in dfs_to_load.items():
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Tabla '{table_name}' cargada correctamente.")

if __name__ == "__main__":
    process_data()
