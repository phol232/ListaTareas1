from src.Capa_Datos.TareaDAO import TareaDAO
from src.Capa_Datos.Tarea import Tarea
from src.Capa_Conexion.ConexionMySql import ConexionMySql
from src.Capa_Negocio.negUsuarios import NegUsuarios

class NegTareas:
    def __init__(self):
        self.conexion = ConexionMySql.get_conexion_sesion()
        if self.conexion is None or not self.conexion.is_connected():
            raise Exception("❌ No hay una sesión de usuario activa o la conexión está cerrada.")

        self.tarea_dao = TareaDAO(self.conexion)

    # ✅ Método para crear una tarea
    def crear_tarea(self, titulo, descripcion, cat_id, prioridad, estado, fecha):
        if not NegUsuarios.usuario_actual:
            return {"error": "❌ No hay un usuario logueado para asignar la tarea."}

        try:
            user_id = NegUsuarios.usuario_actual['user_id']

            with self.conexion.cursor() as cursor:
                cursor.execute("SET @current_user_id = %s", (user_id,))

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
            print(f"❌ Error al crear la tarea: {e}")
            return {"error": f"❌ Error al crear la tarea: {e}"}

    # ✅ Método para listar todas las tareas
    def listar_tareas(self):
        if not NegUsuarios.usuario_actual:
            return {"error": "❌ No hay un usuario logueado para listar tareas."}

        try:
            tareas = self.tarea_dao.listar_tareas()
            if isinstance(tareas, dict) and 'error' in tareas:
                return tareas

            if not tareas:
                return {"message": "ℹ️ No hay tareas registradas."}

            return {"success": True, "tareas": tareas}
        except Exception as e:
            print(f"❌ Error en NegTareas.listar_tareas: {e}")
            return {"error": f"❌ Error en NegTareas.listar_tareas: {e}"}

    # ✅ Método para actualizar una tarea existente
    def actualizar_tarea(self, id_tarea, titulo, descripcion, cat_id, prioridad, estado, fecha):
        if not id_tarea:
            return {"error": "❌ El ID de la tarea es obligatorio para actualizar."}

        try:
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
            print(f"❌ Error al actualizar la tarea: {e}")
            return {"error": f"❌ Error al actualizar la tarea: {e}"}

    # ✅ Método para eliminar una tarea
    def eliminar_tarea(self, id_tarea):
        if not id_tarea:
            return {"error": "❌ El ID de la tarea es obligatorio para eliminar."}

        try:
            resultado = self.tarea_dao.eliminar_tarea(id_tarea)
            if "error" in resultado:
                return resultado
            return {"success": True, "message": resultado.get("message", "✅ Tarea eliminada exitosamente.")}
        except Exception as e:
            print(f"❌ Error al eliminar la tarea: {e}")
            return {"error": f"❌ Error al eliminar la tarea: {e}"}