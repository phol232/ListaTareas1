from mysql.connector import pooling, Error

class ConexionMySql:
    _config = {
        "host": "localhost",
        "database": "gestiontareas",
        "user": "root",
        "password": "230902trph",
    }
    _pool = None
    _conexion_sesion = None

    @classmethod
    def iniciar_pool(cls, pool_size=10):
        """Inicia el pool de conexiones a MySQL."""
        if cls._pool is None:
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=pool_size,
                    pool_reset_session=True,
                    connection_timeout=300,
                    **cls._config
                )
                print("✅ Conexión al pool de MySQL establecida correctamente.")
            except Error as e:
                print(f"❌ Error al conectar a la base de datos: {e}")
                cls._pool = None

    @classmethod
    def get_conexion(cls):
        """Obtiene una conexión del pool."""
        if cls._pool is None:
            cls.iniciar_pool()
        try:
            conexion = cls._pool.get_connection()
            if conexion.is_connected():
                print("🔗 Conexión obtenida y verificada.")
            else:
                conexion.ping(reconnect=True, attempts=3, delay=2)
            return conexion
        except Error as e:
            print(f"❌ Error al obtener conexión del pool: {e}")
            return None

    @classmethod
    def get_conexion_sesion(cls):
        """Devuelve una conexión de sesión activa o la establece si está inactiva."""
        if cls._conexion_sesion is None or not cls._conexion_sesion.is_connected():
            print("🔄 Reestableciendo conexión de sesión...")
            cls._conexion_sesion = cls.get_conexion()

            if cls._conexion_sesion:
                try:
                    cls._conexion_sesion.ping(reconnect=True, attempts=3, delay=2)
                    print("✅ Conexión de sesión verificada y activa.")
                except Error as e:
                    print(f"❌ Error al verificar la conexión: {e}")
                    cls._conexion_sesion = None
        else:
            print("✅ Conexión de sesión activa.")

        return cls._conexion_sesion
