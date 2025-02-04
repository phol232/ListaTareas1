from src.Capa_Conexion.ConexionMySql import ConexionMySql
from src.Capa_Datos.UsuariosDAO import UsuariosDAO  # Asegúrate de importar UsuariosDAO

class NegUsuarios:
    conexion_sesion = None  # Guardará la conexión de sesión
    usuario_actual = None   # Guardará la información del usuario logueado

    @staticmethod
    def autenticar_usuario(email, password):
        conexion = ConexionMySql.get_conexion_sesion()
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("CALL validate_user_login(%s, %s)", (email, password))
            resultado = cursor.fetchone()

            print(f"📢 Resultado del login: {resultado}")

            if resultado and resultado.get('message') == "Login successful":
               NegUsuarios.usuario_actual = {
                  "user_id": resultado.get('id'),  # Asegúrate de que exista 'id'
                  "name": resultado.get('name'),
                  "email": resultado.get('email')  # ✅ Añade 'email' si falta
               }
               return {"message": "Login successful", "user": NegUsuarios.usuario_actual}
            else:
                return {"message": "Invalid email or password"}
        except Exception as e:
            print(f"❌ Error al autenticar usuario: {e}")
            return {"message": f"Error: {str(e)}"}
        finally:
            cursor.close()


    @staticmethod
    def cerrar_sesion():
        """
        Cierra la sesión del usuario actual y limpia la variable de sesión en la base de datos.
        """
        if NegUsuarios.conexion_sesion and NegUsuarios.usuario_actual:
            try:
                cursor = NegUsuarios.conexion_sesion.cursor()
                cursor.execute("SET @current_user_id = NULL")  # Limpiar la variable de sesión en la BD
                NegUsuarios.usuario_actual = None  # Limpiar la información del usuario en memoria
                print("🚪 Sesión cerrada correctamente.")
            except Exception as e:
                print(f"❌ Error al cerrar sesión: {e}")
            finally:
                cursor.close()  # Cerrar el cursor
        else:
            print("ℹ️ No hay una sesión activa para cerrar.")
