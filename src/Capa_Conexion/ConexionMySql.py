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
    _conexion_sesion = None  # Mantiene la sesión activa

    @classmethod
    def iniciar_pool(cls, pool_size=10):
        """Inicia el pool de conexiones a MySQL."""
        if cls._pool is None:
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=pool_size,
                    pool_reset_session=True,  # Restablecer sesión al reutilizar conexiones
                    connection_timeout=300,   # Aumentar el tiempo de espera para conexiones inactivas
                    **cls._config
                )
                print("✅ Conexión al pool de MySQL establecida correctamente.")
            except mysql.connector.Error as e:
                print(f"❌ Error al conectar a la base de datos: {e}")
                cls._pool = None

    @classmethod
    def get_conexion(cls):
        """Obtiene una nueva conexión del pool."""
        if cls._pool is None:
            cls.iniciar_pool()
        try:
            conexion = cls._pool.get_connection()
            if conexion.is_connected():
                print("🔗 Conexión obtenida del pool.")
            return conexion
        except mysql.connector.Error as e:
            print(f"❌ Error al obtener conexión del pool: {e}")
            return None

    @classmethod
    def get_conexion_sesion(cls):
        if cls._conexion_sesion is None or not cls._conexion_sesion.is_connected():
           print("🔄 Reestableciendo conexión de sesión...")
           cls._conexion_sesion = cls.get_conexion()

           # 🔄 Verificar la conexión forzando un ping
           if cls._conexion_sesion:
              try:
                 cls._conexion_sesion.ping(reconnect=True, attempts=3, delay=2)
                 print("✅ Conexión de sesión verificada y activa.")
              except mysql.connector.Error as e:
                 print(f"❌ Error al verificar la conexión: {e}")
                 cls._conexion_sesion = None
        else:
            print("✅ Conexión de sesión activa.")

        return cls._conexion_sesion


    @classmethod
    def cerrar_conexion_sesion(cls):
        """
        Cierra la conexión de sesión de forma segura.
        """
        if cls._conexion_sesion is not None and cls._conexion_sesion.is_connected():
            try:
                cls._conexion_sesion.close()
                print("🔒 Conexión de sesión cerrada correctamente.")
            except mysql.connector.Error as e:
                print(f"❌ Error al cerrar la conexión de sesión: {e}")
            finally:
                cls._conexion_sesion = None
        else:
            print("ℹ️ No hay una conexión de sesión activa para cerrar.")
