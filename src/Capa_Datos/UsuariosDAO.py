from src.Capa_Conexion.ConexionMySql import ConexionMySql
from src.Capa_Datos.Usuarios import Usuario
import mysql.connector

class UsuariosDAO:
    def __init__(self, conexion=None):
        # Si no se pasa una conexión, obtiene una del pool
        self.conexion = conexion if conexion else ConexionMySql.get_conexion_sesion()

    def validar_login(self, email: str, password_hash: str):
        """
        Valida el login del usuario utilizando un procedimiento almacenado en MySQL.
        """
        try:
            cursor = self.conexion.cursor(dictionary=True)

            # Llamada al procedimiento almacenado
            cursor.callproc('validate_user_login', [email, password_hash])

            resultado = None
            for result in cursor.stored_results():
                rows = result.fetchall()
                if rows:
                    for row in rows:
                        print(f"📢 Resultado del login: {row.get('message')}")
                        if row.get('message') == "Login successful":
                            # Crear una instancia de Usuario si el login es exitoso
                            usuario = Usuario(
                                id=row['id'],
                                name=row['name'],
                                email=row['email'],
                                password_hash=row['password_hash']
                            )
                            resultado = usuario.to_dict()  # Convertimos el usuario a diccionario
                        else:
                            resultado = {"message": row.get('message')}

            cursor.close()
            return resultado if resultado else {"message": "Invalid email or password"}

        except mysql.connector.Error as e:
            print(f"❌ Error en la base de datos: {e}")
            return {"message": f"Database error: {str(e)}"}

    def obtener_usuario_por_id(self, user_id: int):
        """
        Obtiene la información de un usuario por su ID.
        """
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = "SELECT id, name, email, password_hash FROM usuarios WHERE id = %s"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()

            if row:
                usuario = Usuario(
                    id=row['id'],
                    name=row['name'],
                    email=row['email'],
                    password_hash=row['password_hash']
                )
                return usuario.to_dict()
            else:
                return None

        except mysql.connector.Error as e:
            print(f"❌ Error al obtener usuario por ID: {e}")
            return None
        finally:
            cursor.close()

    def registrar_usuario(self, usuario: Usuario):
        """
        Registra un nuevo usuario en la base de datos.
        """
        try:
            cursor = self.conexion.cursor()
            query = """
                INSERT INTO usuarios (name, email, password_hash)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (usuario.get_name(), usuario.get_email(), usuario.get_password_hash()))
            self.conexion.commit()
            print("✅ Usuario registrado exitosamente.")
            return {"message": "User registered successfully"}
        except mysql.connector.Error as e:
            print(f"❌ Error al registrar usuario: {e}")
            return {"message": f"Error registering user: {str(e)}"}
        finally:
            cursor.close()

    def actualizar_usuario(self, usuario: Usuario):
        """
        Actualiza la información de un usuario existente.
        """
        try:
            cursor = self.conexion.cursor()
            query = """
                UPDATE usuarios
                SET name = %s, email = %s, password_hash = %s
                WHERE id = %s
            """
            cursor.execute(query, (usuario.get_name(), usuario.get_email(), usuario.get_password_hash(), usuario.get_id()))
            self.conexion.commit()
            print(f"✅ Usuario actualizado correctamente: {usuario.get_id()}")
            return {"message": "User updated successfully"}
        except mysql.connector.Error as e:
            print(f"❌ Error al actualizar usuario: {e}")
            return {"message": f"Error updating user: {str(e)}"}
        finally:
            cursor.close()

    def eliminar_usuario(self, user_id: int):
        """
        Elimina un usuario de la base de datos por su ID.
        """
        try:
            cursor = self.conexion.cursor()
            query = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(query, (user_id,))
            self.conexion.commit()
            print(f"✅ Usuario eliminado correctamente: ID {user_id}")
            return {"message": "User deleted successfully"}
        except mysql.connector.Error as e:
            print(f"❌ Error al eliminar usuario: {e}")
            return {"message": f"Error deleting user: {str(e)}"}
        finally:
            cursor.close()
