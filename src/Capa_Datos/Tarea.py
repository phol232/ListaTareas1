class Tarea:
    def __init__(self, id_tarea: str = None, user_id: str = None, titulo: str = "",
                 descripcion: str = "", cat_id: str = None, prioridad: str = "",
                 estado: str = "", fecha: str = ""):
        self._id_tarea = id_tarea
        self._user_id = user_id
        self._titulo = titulo
        self._descripcion = descripcion
        self._cat_id = cat_id
        self._prioridad = prioridad
        self._estado = estado
        self._fecha = fecha

    # Getters y Setters
    def get_id_tarea(self):
        return self._id_tarea

    def set_id_tarea(self, id_tarea: str):
        self._id_tarea = id_tarea

    def get_user_id(self):
        return self._user_id

    def set_user_id(self, user_id: str):
        self._user_id = user_id

    def get_titulo(self):
        return self._titulo

    def set_titulo(self, titulo: str):
        self._titulo = titulo

    def get_descripcion(self):
        return self._descripcion

    def set_descripcion(self, descripcion: str):
        self._descripcion = descripcion

    def get_cat_id(self):
        return self._cat_id

    def set_cat_id(self, cat_id: str):
        self._cat_id = cat_id

    def get_prioridad(self):
        return self._prioridad

    def set_prioridad(self, prioridad: str):
        self._prioridad = prioridad

    def get_estado(self):
        return self._estado

    def set_estado(self, estado: str):
        self._estado = estado

    def get_fecha(self):
        return self._fecha

    def set_fecha(self, fecha: str):
        self._fecha = fecha

    # ✅ Método corregido para convertir la tarea en un diccionario
    def to_dict(self):
        return {
            "id_tarea": self._id_tarea,
            "user_id": self._user_id,
            "titulo": self._titulo,
            "descripcion": self._descripcion,
            "categoria": self._cat_id,
            "prioridad": self._prioridad,
            "estado": self._estado,
            "fecha": self._fecha
        }
