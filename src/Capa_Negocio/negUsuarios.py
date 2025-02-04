from src.Capa_Conexion.ConexionMySql import ConexionMySql
from src.Capa_Datos.UsuariosDAO import UsuariosDAO

class NegUsuarios:
    conexion_sesion = None
    usuario_actual = None

    @staticmethod
    def autenticar_usuario(email, password):
        try:
            if not NegUsuarios.conexion_sesion or not NegUsuarios.conexion_sesion.is_connected():
               NegUsuarios.conexion_sesion = ConexionMySql.get_conexion_sesion()

            usuarios_dao = UsuariosDAO(NegUsuarios.conexion_sesion)
            resultado = usuarios_dao.validar_login(email, password)

            if resultado.get('message') == "Login successful":
               NegUsuarios.usuario_actual = {
                  "user_id": resultado.get('id'),
                  "name": resultado.get('name'),
                  "email": resultado.get('email')
               }

               # ✅ Asegúrate de no duplicar el cursor
               with NegUsuarios.conexion_sesion.cursor() as cursor:
                    cursor.execute("SET @current_user_id = %s", (NegUsuarios.usuario_actual['user_id'],))
                    NegUsuarios.conexion_sesion.commit()

               return {"message": "Login successful", "user": NegUsuarios.usuario_actual}
            else:
               return {"message": "Invalid email or password"}

        except Exception as e:
            return {"message": f"Error: {str(e)}"}


    @staticmethod
    def obtener_conexion_activa():
        if not NegUsuarios.conexion_sesion or not NegUsuarios.conexion_sesion.is_connected():
            print("🔄 Restableciendo la conexión de sesión...")
            NegUsuarios.conexion_sesion = ConexionMySql.get_conexion_sesion()

        if NegUsuarios.conexion_sesion and NegUsuarios.conexion_sesion.is_connected():
            print("✅ Conexión de sesión activa.")
            return NegUsuarios.conexion_sesion
        else:
            print("❌ No se pudo establecer una conexión activa.")
            return None

    @staticmethod
    def cerrar_sesion():
        if NegUsuarios.conexion_sesion and NegUsuarios.conexion_sesion.is_connected():
            try:
                cursor = NegUsuarios.conexion_sesion.cursor()
                cursor.execute("SET @current_user_id = NULL")
                NegUsuarios.usuario_actual = None
                NegUsuarios.conexion_sesion.close()
                print("🚪 Sesión cerrada y conexión finalizada correctamente.")
            except Exception as e:
                print(f"❌ Error al cerrar la sesión: {e}")
            finally:
                if 'cursor' in locals() and cursor:
                    cursor.close()
                NegUsuarios.conexion_sesion = None
        else:
            print("ℹ️ No hay una sesión activa para cerrar.")
