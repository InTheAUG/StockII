import sys
import os
import toml
import subprocess
from pathlib import Path
from stock import paths
import psycopg2

DB_CONFIG = toml.load(Path(__file__).parent.absolute() / "dbconfig.toml")["postgresql"]
SETUP_DB_NAME = DB_CONFIG["db_setup_name"]
DB_USER = DB_CONFIG["db_user"]
DB_USER_PW = DB_CONFIG["db_pw"]
DB_HOST = DB_CONFIG["db_host"]
DB_PORT = DB_CONFIG["db_port"]
DB_NAME = DB_CONFIG["db_name"]


def printPostgresVersion(cursor):
    print("PostgreSQL database version:")
    cursor.execute("SELECT version()")
    db_version = cursor.fetchone()
    print(db_version)


def createPostgresDB():
    create_db_statement = f"CREATE database {DB_NAME}"

    conn = psycopg2.connect(
        database=SETUP_DB_NAME,
        user=DB_USER,
        password=DB_USER_PW,
        host=DB_HOST,
        port=DB_PORT,
    )
    conn.autocommit = True
    cursor = conn.cursor()
    printPostgresVersion(cursor)
    cursor.execute(create_db_statement)
    return


if __name__ == "__main__":
    assert "linux" in sys.platform

    os.mkdir(paths.DATA_BASEPATH)
    os.mkdir(paths.STOCKFILES)
    os.mkdir(paths.MODELS)

    subprocess.run(["cd", Path(__file__).absolute().parent])
    subprocess.run(["python3", "-m", "pip", "install", "poetry"])
    subprocess.run(["poetry", "install"])


    subprocess.run(
        [
            "docker-compose",
            Path(__file__).parent.absolute() / "docker-compose.yml",
            "up",
        ]
    )
    createPostgresDB()
    subprocess.run(
        [
            "docker-compose",
            Path(__file__).parent.absolute() / "docker-compose.yml",
            "down",
        ]
    )
