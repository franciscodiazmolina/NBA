#importar librerias
import pandas as pd
import pymssql
import pyodbc
from sqlalchemy import create_engine
import numpy as np
import zipfile
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
#READ

# 🔹 Montar Google Drive
kaggle_json_path = "/content/drive/My Drive/Proyecto Final/kaggle.json"



# Crear carpeta .kaggle en el directorio raíz del usuario
os.makedirs("/root/.kaggle", exist_ok=True)

# Mover kaggle.json a la carpeta
!mv kaggle.json /root/.kaggle/

# Cambiar permisos para evitar problemas de acceso
!chmod 600 /root/.kaggle/kaggle.json

!kaggle datasets download -d wyattowalsh/basketball


# Extraer los archivos en una carpeta llamada "basketball_data"
with zipfile.ZipFile("basketball.zip", "r") as zip_ref:
    zip_ref.extractall("basketball_data")

# Listar archivos en la carpeta
os.listdir("basketball_data")

#lecura de archivos a usar (conectar a la API, Seleccionar de un Bucket)
#df_team eliminar
df_game=pd.read_csv("basketball_data/csv/game.csv")
df_team_details=pd.read_csv('basketball_data/csv/team_details.csv')
df_other_stats=pd.read_csv('basketball_data/csv/other_stats.csv')
df_line=pd.read_csv('basketball_data/csv/line_score.csv')
df_common_player=pd.read_csv('basketball_data/csv/common_player_info.csv')
df_draft_history=pd.read_csv('basketball_data/csv/draft_history.csv')
df_game_info=pd.read_csv('basketball_data/csv/game_info.csv')
df_play_by_play=pd.read_csv('basketball_data/csv/play_by_play.csv')

#Scraping Instagram

#limpieza


dfs = {
    'df_game': df_game,
    'df_team_details': df_team_details,
    'df_other_stats': df_other_stats,
    'df_line': df_line,
    'df_common_player': df_common_player,
    'df_draft_history': df_draft_history,
    'df_game_info': df_game_info,
    'df_play_by_play': df_play_by_play
}

#eliminar columnas de dataframes
columns_to_drop = {
    'df_game': ['team_abbreviation_home',	'team_name_home', 'video_available_away', 'matchup_home',
                'matchup_away', 'team_abbreviation_away', 'team_name_away', 'video_available_home'], #, 'game_date'
    'df_team_details': [ 'dleagueaffiliation'], #'id'
    'df_other_stats': ['league_id','team_abbreviation_home',
                        'team_city_home','largest_lead_home', 'lead_changes', 'times_tied',
                        'team_turnovers_home','team_rebounds_home','team_abbreviation_away',
                        'team_city_away', 'largest_lead_away', 'team_turnovers_away',
                        'team_rebounds_away'],
    'df_line': ["pts_ot5_home","pts_ot6_home","pts_ot7_home","pts_ot8_home","pts_ot9_home","pts_ot10_home","pts_ot5_away","pts_ot6_away",
                      "pts_ot7_away","pts_ot8_away","pts_ot9_away","pts_ot10_away","game_sequence","team_abbreviation_home","team_city_name_home",
                      "team_nickname_home","team_abbreviation_away","team_city_name_away","team_nickname_away",
                      "team_wins_losses_home","team_wins_losses_away"],#"game_date_est"
    'df_common_player': ['display_first_last', 'display_last_comma_first', 'display_fi_last', 'player_slug', 'last_affiliation', 'team_name',
                         'team_code', 'dleague_flag', 'nba_flag', 'games_played_flag', 'greatest_75_flag',
                         'games_played_current_season_flag','school', 'team_abbreviation', 'team_city'],#'player_code'
    'df_draft_history': ['player_profile_flag', 'draft_type', 'player_name',	'round_number',	'round_pick', 'overall_pick',
                         'team_city', 'team_name', 'team_abbreviation', 'organization', 'organization_type'],#, 'season'
    'df_game_info': ['game_time'],
    'df_play_by_play': ['wctimestring', 'eventnum', 'neutraldescription', 'person1type', 'person2type', 'person3type',
                        'player1_team_city', 'player1_team_nickname', 'player2_team_city', 'player2_team_nickname', 'player3_team_city',
                        'player3_team_nickname', 'video_available_flag', 'player3_id', 'player3_name', 'player3_team_id',
                        'player3_team_abbreviation','period', 'pctimestring', 'scoremargin', 'player1_name',
                        'player1_team_id', 'player2_name','player2_team_id']

}

for df_name, columns in columns_to_drop.items():
    df = globals().get(df_name)
    if df is not None:
        df.drop(columns=columns, axis=1, inplace=True)


# cambio de datos game y game info ******
df_line = df_line.rename(columns={'game_date_est': 'game_date'})

#Pasar date a fecha

df_game_info['game_date'] = pd.to_datetime(df_game_info['game_date'])
df_game['game_date'] = pd.to_datetime(df_game['game_date'])
df_line['game_date'] = pd.to_datetime(df_line['game_date'])


#2018 en adelante ******
df_game = df_game[df_game['game_date'] >  '2018-10-01']
df_game_info = df_game_info[df_game_info['game_date'] >  '2018-10-01']
df_line = df_line[(df_line["game_date"] > "2018-10-16")]
df_common_player=df_common_player[(df_common_player['from_year'] >= 2001)]
df_draft_history = df_draft_history[(df_draft_history["season"] >= 2001)]


#Columnas  rellenar
df_game.loc[:, 'ft_pct_home'] = df_game['ft_pct_home'].fillna(0)

#completar de forma especifica los nulos team_details
nuevos_registros = [
    {
        'team_id': '1610612738',
        'abbreviation': 'BOS',
        'nickname': 'Celtics',
        'yearfounded': '1946',
        'city': 'Boston',
        'arena': 'TD Garden',
        'arenacapacity': '18624',
        'owner': 'Wyc Grousbeck',
        'generalmanager': 'Brad Stevens',
        'headcoach': 'Joe Mazzulla',
        'dleagueaffiliation': 'Maine Celtics',
        'facebook': 'https://web.facebook.com/bostonceltics/',
        'instagram': 'https://www.instagram.com/celtics/',
        'twitter': 'https://x.com/celtics'
    },
    {
        'team_id': '1610612739',
        'abbreviation': 'CLE',
        'nickname': 'Cavaliers',
        'yearfounded': '1970',
        'city': 'cleveland',
        'arena': 'Rocket Arena',
        'arenacapacity': '19432',
        'owner': 'Dan Gilbert',
        'generalmanager': 'Mike Gansey',
        'headcoach': 'Kenny Atkinson',
        'dleagueaffiliation': 'The Cleveland Charge',
        'facebook': 'https://web.facebook.com/Cavs/',
        'instagram': 'https://www.instagram.com/cavs/',
        'twitter': 'https://x.com/cavs'
    },
    {
        'team_id': '1610612740',
        'abbreviation': 'NOP',
        'nickname': 'Pelicans',
        'yearfounded': '2002',
        'city': 'New Orleans',
        'arena': 'New Orleans Arena',
        'arenacapacity': '17791',
        'owner': 'Gayle Benson',
        'generalmanager': 'Bryson Graham',
        'headcoach': 'Willie Green',
        'dleagueaffiliation': 'Birmingham Squadron',
        'facebook': 'https://web.facebook.com/PelicansNBA/',
        'instagram': 'https://www.instagram.com/pelicansnba/',
        'twitter': 'https://x.com/PelicansNBA'
    },
    {
        'team_id': '1610612752',
        'abbreviation': 'NYK',
        'nickname': 'Knicks',
        'yearfounded': '1946',
        'city': 'New York',
        'arena': 'Madison Square Garden',
        'arenacapacity': '19500',
        'owner': 'James L. Dolan',
        'generalmanager': 'Gersson Rosas',
        'headcoach': 'Tom Thibodeau',
        'dleagueaffiliation': 'Westchester Knicks',
        'facebook': 'https://web.facebook.com/NYKnicks',
        'instagram': 'https://www.instagram.com/nyknicks',
        'twitter': 'https://x.com/nyknicks'
    },
    {
        'team_id': '1610612753',
        'abbreviation': 'ORL',
        'nickname': 'Magic',
        'yearfounded': '1989',
        'city': 'Orlando',
        'arena': 'Kia Center',
        'arenacapacity': '20000',
        'owner': 'RDV Sports, Inc.',
        'generalmanager': 'Anthony Parker',
        'headcoach': 'Jamahl Mosley',
        'dleagueaffiliation': 'Osceola Magic y Lakeland Magic',
        'facebook': 'https://web.facebook.com/OrlandoMagic/',
        'instagram': 'https://www.instagram.com/orlandomagic/',
        'twitter': 'https://x.com/OrlandoMagic'
    }
]
df_team_details = pd.concat([df_team_details, pd.DataFrame(nuevos_registros)], ignore_index=True)

df_team_details.loc[df_team_details["nickname"] == "Nuggets", "arenacapacity"] = 21000
df_team_details.loc[df_team_details["nickname"] == "Warriors", "arenacapacity"] = 18064
df_team_details.loc[df_team_details["nickname"] == "Nets", "arenacapacity"] = 19000
df_team_details.loc[df_team_details["nickname"] == "76ers", "arenacapacity"] = 21000
df_team_details.loc[df_team_details["nickname"] == "Suns", "arenacapacity"] = 18422
df_team_details.loc[df_team_details["nickname"] == "Thunder", "arenacapacity"] = 18203
df_team_details.loc[df_team_details["nickname"] == "Raptors", "arenacapacity"] = 19800
df_team_details.loc[df_team_details["nickname"] == "Jazz", "arenacapacity"] = 20000
df_team_details.loc[df_team_details["nickname"] == "Pistons", "arenacapacity"] = 20491
df_team_details.loc[df_team_details["nickname"] == "Raptors", "headcoach"] = 'Darko Rajaković'

#df_team_details= df_team_details.sort_values(by='team_id').reset_index()

#crear una nueva columna en team_details
equipos_este = ["BOS", "BKN", "NYK", "PHI", "TOR", "ATL", "CHA", "MIA", "ORL", "WAS", "CHI", "CLE", "DET", "IND", "MIL"]

df_team_details["Conferencia"] = df_team_details["abbreviation"].apply(lambda x: "East" if x in equipos_este else "West")

df_team_details['full_name'] = df_team_details['city'] + ' ' + df_team_details['nickname']


# filtrar los datos de 'All Stars' y 'pretemporada' game

df_game = df_game[~df_game['season_type'].isin(['All-Star', 'All Star', 'Pre Season'])]

# filtro de publico por maximo game_info
df_game_info = df_game_info[df_game_info['attendance'] <= 21711]


# Limpieza other_stats
df_game_id = df_game['game_id'].unique().tolist()
df_other_stats = df_other_stats[df_other_stats['game_id'].isin(df_game_id)]
# Limpieza play_by_play
df_play_by_play = df_play_by_play[df_play_by_play['game_id'].isin(df_game_id)]
eventos_analisis= [1, 2, 3, 4, 5, 6]
df_play_by_play = df_play_by_play[df_play_by_play['eventmsgtype'].isin(eventos_analisis)]


#Scraping team_details=Instagram




#limpios
df_game.to_csv('/df_game.csv', index=False)
df_team_details.to_csv('/df_team_details.csv', index=False)
df_other_stats.to_csv('/df_other_stats.csv', index=False)
df_line.to_csv('/df_line.csv', index=False)
df_common_player.to_csv('/df_common_player.csv', index=False)
df_draft_history.to_csv('/df_draft_history.csv', index=False)
df_game_info.to_csv('/df_game_info.csv', index=False)



#CARGA
# Configurar conexión a SQL Server
server = 'server-sql-grupo1.database.windows.net'
database = 'NBA'
username = 'Admon'
password = 'Password.Server1'

# Crear el engine usando pymssql
connection_string = f"mssql+pymssql://{username}:{password}@{server}/{database}"
engine = create_engine(connection_string)

# Diccionario de DataFrames (asegúrate de definirlos previamente)
dfs_to_load = {
    #'df_game': df_game,
    'df_team_details': df_team_details,
    #'df_other_stats': df_other_stats,
    #'df_line': df_line,
    #'df_common_player': df_common_player,
    #'df_draft_history': df_draft_history,
    #'df_game_info': df_game_info,
    #'df_play_by_play': df_play_by_play
}

# Cargar los DataFrames en la base de datos
for table_name, df in dfs_to_load.items():
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Tabla '{table_name}' cargada correctamente.")

