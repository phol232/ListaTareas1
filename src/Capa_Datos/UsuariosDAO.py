from src.Capa_Conexion.ConexionMySql import ConexionMySql

class UsuariosDAO:
    def __init__(self, conexion=None):
        self.conexion = conexion if conexion else ConexionMySql.get_conexion_sesion()

    def validar_login(self, email: str, password_hash: str):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.callproc('validate_user_login', [email, password_hash])

            resultado = None
            for result in cursor.stored_results():
                rows = result.fetchall()
                if rows:
                    resultado = rows[0]

            cursor.close()
            return resultado if resultado else {"message": "Invalid email or password"}

        except Exception as e:
            return {"message": f"Database error: {str(e)}"}

    def obtener_usuario_por_id(self, user_id):
        """Obtiene un usuario por su ID desde la base de datos."""
        if not self.conexion or not self.conexion.is_connected():
            return {"error": "❌ No hay una conexión activa con la base de datos."}

        try:
            with self.conexion.cursor(dictionary=True) as cursor:
                query = "SELECT id, nombre, email FROM usuarios WHERE id = %s"
                cursor.execute(query, (user_id,))
                usuario = cursor.fetchone()
                return usuario if usuario else None
        except Exception as e:
            return {"error": f"❌ Error al obtener usuario: {e}"}
