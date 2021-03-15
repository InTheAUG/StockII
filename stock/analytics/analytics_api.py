from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
import psycopg2
import toml
from pathlib import Path

DB_CONFIG = toml.load(Path(__file__).parent.parent.absolute() / "dbconfig.toml")[
    "postgresql"
]
SETUP_DB_NAME = DB_CONFIG["db_setup_name"]
DB_USER = DB_CONFIG["db_user"]
DB_USER_PW = DB_CONFIG["db_pw"]
DB_HOST = DB_CONFIG["db_host"]
DB_PORT = DB_CONFIG["db_port"]
DB_NAME = DB_CONFIG["db_name"]
db_connect = psycopg2.connect(
    database=SETUP_DB_NAME,
    user=DB_USER,
    password=DB_USER_PW,
    host=DB_HOST,
    port=DB_PORT,
)
