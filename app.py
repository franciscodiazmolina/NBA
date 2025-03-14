from flask import Flask, jsonify, request
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

app = Flask(__name__)

@app.route('/process', methods=['GET'])
def process_data():
    try:
        # Aquí va el código de procesamiento (de tu script)
        # El código para leer los datos y hacer la limpieza, etc.
        
        # Ejemplo de la limpieza y lectura de los datos:
        df_game = pd.read_csv("basketball_data/csv/game.csv")
        df_team_details = pd.read_csv('basketball_data/csv/team_details.csv')

        # Código de limpieza aquí (lo que ya tienes en tu script)
        
        # Simulando el proceso:
        return jsonify({"message": "Data processed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
