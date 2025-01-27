class Usuario:
    def __init__(self, id: str, name: str, email: str, password_hash: str):

        self._id = id
        self._name = name
        self._email = email
        self._password_hash = password_hash

    # Getters
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def get_password_hash(self):
        return self._password_hash

    # Setters
    def set_id(self, id: str):
        self._id = id

    def set_name(self, name: str):
        self._name = name

    def set_email(self, email: str):
        self._email = email

    def set_password_hash(self, password_hash: str):
        self._password_hash = password_hash

    # Método para imprimir los datos del usuario
    def __str__(self):
        return f"Usuario(id='{self._id}', name='{self._name}', email='{self._email}', password_hash='{self._password_hash}')"


# Ejemplo de uso
if __name__ == "__main__":
    usuario = Usuario("123456", "Alice Johnson", "alice.johnson@example.com", "hashed_password_123")
    print(usuario)

    # Actualizando algunos atributos
    usuario.set_email("new.email@example.com")
    print(f"Email actualizado: {usuario.get_email()}")
