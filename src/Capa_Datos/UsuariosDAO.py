from src.Capa_Conexion.ConexionMySql import ConexionMySql

class UsuariosDAO:
    def __init__(self, conexion=None):  # ✅ Aceptar un argumento opcional
        self.conexion = conexion if conexion else ConexionMySql.get_conexion_sesion()

    def validar_login(self, email: str, password_hash: str):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.callproc('validate_user_login', [email, password_hash])

            resultado = None
            for result in cursor.stored_results():
                rows = result.fetchall()
                if rows:
                    resultado = rows[0]  # ✅ Obtener la primera fila del resultado

            cursor.close()
            return resultado if resultado else {"message": "Invalid email or password"}

        except Exception as e:
            return {"message": f"Database error: {str(e)}"}
