import mysql.connector
from mysql.connector import pooling

class ConexionMySql:
    _config = {
        "host": "localhost",
        "database": "gestiontareas",
        "user": "root",
        "password": "230902trph",
    }

    _pool = None

    @classmethod
    def iniciar_pool(cls, pool_size=10):
        if cls._pool is None:
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=pool_size,
                    **cls._config
                )
                print("Conexión al pool de MySQL establecida correctamente.")
            except mysql.connector.Error as e:
                print(f"Error al conectar a la base de datos: {e}")
                cls._pool = None

    @classmethod
    def get_conexion(cls):
        if cls._pool is None:
            cls.iniciar_pool()
        try:
            return cls._pool.get_connection()
        except mysql.connector.Error as e:
            print(f"Error al obtener conexión del pool: {e}")
            return None
