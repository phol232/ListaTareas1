from src.Capa_Datos.TareaDAO import TareaDAO
from src.Capa_Datos.Tarea import Tarea
from src.Capa_Negocio.negUsuarios import NegUsuarios
from src.Capa_Datos.UsuariosDAO import UsuariosDAO

class NegTareas:
    def __init__(self):
        self._inicializar_conexion()

    def _inicializar_conexion(self):
        self.conexion = NegUsuarios.obtener_conexion_activa()
        if not self.conexion or not self.conexion.is_connected():
            raise Exception("❌ No hay una sesión de usuario activa o la conexión está cerrada.")
        self.tarea_dao = TareaDAO(self.conexion)
        self.usuarios_dao = UsuariosDAO(self.conexion)  # Instancia de UsuariosDAO

    def crear_tarea(self, titulo, descripcion, cat_id, prioridad, estado, fecha):
        if not NegUsuarios.usuario_actual:
            return {"error": "❌ No hay un usuario logueado para asignar la tarea."}

        try:
            if not self.conexion.is_connected():
                self._inicializar_conexion()  # Reconectar si la conexión se pierde

            # Verificar si el usuario existe en la base de datos
            user_id = NegUsuarios.usuario_actual['user_id']
            usuario_db = self.usuarios_dao.obtener_usuario_por_id(user_id)

            if not usuario_db:
                return {"error": "❌ El usuario actual no existe en la base de datos."}

            nueva_tarea = Tarea(
                user_id=user_id,
                titulo=titulo,
                descripcion=descripcion,
                cat_id=cat_id,
                prioridad=prioridad,
                estado=estado,
                fecha=fecha
            )

            resultado = self.tarea_dao.crear_tarea(nueva_tarea)
            if "error" in resultado:
                return resultado
            return {"success": True, "message": resultado.get("message", "✅ Tarea creada exitosamente.")}

        except Exception as e:
            return {"error": f"❌ Error al crear la tarea: {e}"}

    def listar_tareas(self, user_id=None):
        try:
            if not self.conexion.is_connected():
                self._inicializar_conexion()

            user_id = user_id or (NegUsuarios.usuario_actual.get('user_id') if NegUsuarios.usuario_actual else None)
            if not user_id:
                return {"error": "❌ No se pudo identificar al usuario para listar tareas."}

            response = self.tarea_dao.listar_tareas(user_id=user_id)

            if response.get("error"):
                return {"error": response["error"]}

            tareas = response.get("tareas", [])
            return {"success": True, "tareas": tareas}

        except Exception as e:
            return {"error": f"❌ Error al listar tareas: {e}"}

    def actualizar_tarea(self, id_tarea, titulo, descripcion, cat_id, prioridad, estado, fecha):
        if not id_tarea:
            return {"error": "❌ El ID de la tarea es obligatorio para actualizar."}

        try:
            if not self.conexion.is_connected():
                self._inicializar_conexion()

            tarea = Tarea(
                id_tarea=id_tarea,
                titulo=titulo,
                descripcion=descripcion,
                cat_id=cat_id,
                prioridad=prioridad,
                estado=estado,
                fecha=fecha
            )
            resultado = self.tarea_dao.actualizar_tarea(tarea)
            if "error" in resultado:
                return resultado
            return {"success": True, "message": resultado.get("message", "✅ Tarea actualizada exitosamente.")}

        except Exception as e:
            return {"error": f"❌ Error al actualizar la tarea: {e}"}

    def eliminar_tarea(self, id_tarea):
        if not id_tarea:
            return {"error": "❌ El ID de la tarea es obligatorio para eliminar."}

        try:
            if not self.conexion.is_connected():
                self._inicializar_conexion()

            resultado = self.tarea_dao.eliminar_tarea(id_tarea)
            if "error" in resultado:
                return resultado
            return {"success": True, "message": resultado.get("message", "✅ Tarea eliminada exitosamente.")}

        except Exception as e:
            return {"error": f"❌ Error al eliminar la tarea: {e}"}
