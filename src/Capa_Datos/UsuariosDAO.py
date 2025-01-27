import mysql.connector
from src.Capa_Conexion.ConexionMySql import ConexionMySql
from src.Capa_Datos.Usuarios import Usuario  # Importar la clase Usuario del archivo correspondiente

class Usuarios:
    @staticmethod
    def validate_user_login(email, password_hash):
        """Llama al procedimiento almacenado para validar el inicio de sesión."""
        try:
            # Obtener conexión a la base de datos
            conexion = ConexionMySql.get_conexion()
            if not conexion:
                print("No se pudo obtener conexión a la base de datos.")
                return {"message": "Error de conexión"}

            cursor = conexion.cursor(dictionary=True)

            # Llamar al procedimiento almacenado en MySQL
            cursor.callproc('validate_user_login', [email, password_hash])

            # Recuperar resultados
            resultado = None
            for result in cursor.stored_results():
                rows = result.fetchall()
                if rows:
                    for row in rows:
                        print(f"Mensaje: {row.get('message')}")
                        if 'id' in row and 'name' in row and 'email' in row and 'password_hash' in row:
                            # Crear instancia de Usuario con los datos recuperados
                            usuario = Usuario(row['id'], row['name'], row['email'], row['password_hash'])
                            resultado = usuario
                        else:
                            resultado = {"message": row.get('message')}

            cursor.close()
            conexion.close()

            return resultado if resultado else {"message": "Invalid email or password"}

        except mysql.connector.Error as e:
            print("Error al ejecutar el procedimiento almacenado:", str(e))
            return {"message": "Error al conectar con la base de datos"}
