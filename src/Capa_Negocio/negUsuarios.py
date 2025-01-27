from src.Capa_Datos.UsuariosDAO import Usuarios

class NegUsuarios:
    @staticmethod
    def autenticar_usuario(email, password):
        """Maneja la lógica de autenticación del usuario."""

        # Validar si los campos están vacíos
        if not email or not password:
            return {"message": "Debe ingresar email y contraseña"}

        try:
            # Llamar a la capa de datos para validar el usuario
            resultado = Usuarios.validate_user_login(email, password)

            # Verificar si el resultado contiene los datos correctos
            if isinstance(resultado, dict) and resultado.get('message') == "Login successful":
                return {
                    "message": "Login successful",
                    "id": resultado.get("id"),
                    "name": resultado.get("name"),
                    "email": resultado.get("email")
                }
            elif isinstance(resultado, dict) and resultado.get('message'):
                return {"message": resultado.get('message')}
            else:
                return {"message": "Invalid email or password"}

        except ConnectionError:
            return {"message": "Error de conexión con la base de datos"}
        except Exception as e:
            print("Error en la autenticación:", str(e))
            return {"message": "Error en la autenticación"}

# Código de prueba
if __name__ == "__main__":
    email = "alice.johnson@example.com"
    password = "123456"

    resultado = NegUsuarios.autenticar_usuario(email, password)

    if resultado.get("message") == "Login successful":
        print(f"Bienvenido {resultado['name']} (ID: {resultado['id']})")
    else:
        print(resultado["message"])
