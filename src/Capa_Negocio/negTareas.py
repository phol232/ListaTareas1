from src.Capa_Datos.TareaDAO import TareaDAO
from src.Capa_Datos.Tarea import Tarea
from src.Capa_Negocio.negUsuarios import NegUsuarios
from src.Capa_Datos.UsuariosDAO import UsuariosDAO

class NegTareas:
    def __init__(self):
        self.conexion = None  # 📌 Inicializar como None
        self._inicializar_conexion()

    def _inicializar_conexion(self):
        """📌 Verifica y obtiene la conexión activa con la base de datos."""
        try:
            self.conexion = NegUsuarios.obtener_conexion_activa()
            if not self.conexion or not self.conexion.is_connected():
                raise Exception("❌ No hay una sesión de usuario activa o la conexión está cerrada.")
            self.tarea_dao = TareaDAO(self.conexion)
            self.usuarios_dao = UsuariosDAO(self.conexion)  # 📌 Instancia de UsuariosDAO
        except Exception as e:
            print(f"❌ Error al inicializar la conexión: {e}")
            self.conexion = None  # Si hay error, se mantiene como None

    def verificar_conexion(self):
        """📌 Verifica si la conexión sigue activa y la reinicia si es necesario."""
        if not self.conexion or not self.conexion.is_connected():
            print("🔄 Reconectando a la base de datos...")
            self._inicializar_conexion()

    def crear_tarea(self, titulo, descripcion, cat_id, prioridad, estado, fecha):
        """📌 Crea una nueva tarea en la base de datos."""
        if not NegUsuarios.usuario_actual:
            return {"error": "❌ No hay un usuario logueado para asignar la tarea."}

        try:
            self.verificar_conexion()  # ✅ Asegurar conexión

            user_id = NegUsuarios.usuario_actual.get("user_id")
            if not user_id:
                return {"error": "❌ No se pudo obtener el ID del usuario."}

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
            return resultado if "error" in resultado else {"success": True, "message": "✅ Tarea creada exitosamente."}

        except Exception as e:
            return {"error": f"❌ Error al crear la tarea: {e}"}

    def listar_tareas(self, user_id=None):
        """📌 Lista todas las tareas del usuario autenticado."""
        try:
            self.verificar_conexion()  # ✅ Asegurar conexión

            user_id = user_id or NegUsuarios.usuario_actual.get("user_id")
            if not user_id:
                return {"error": "❌ No se pudo identificar al usuario para listar tareas."}

            response = self.tarea_dao.listar_tareas(user_id=user_id)
            if "error" in response:
                return response

            tareas = response.get("tareas", [])

            # 📌 Asegurar que todas las tareas tengan ID
            for tarea in tareas:
                if not tarea.get("idTarea"):
                    print(f"⚠️ Advertencia: Tarea sin ID detectada {tarea}")

            return {"success": True, "tareas": tareas}

        except Exception as e:
            return {"error": f"❌ Error al listar tareas: {e}"}

    def actualizar_tarea(self, id_tarea, titulo, descripcion, cat_id, prioridad, estado, fecha):
        """📌 Actualiza una tarea existente."""
        if not id_tarea:
            return {"error": "❌ El ID de la tarea es obligatorio para actualizar."}

        try:
            self.verificar_conexion()  # ✅ Asegurar conexión

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
            return resultado if "error" in resultado else {"success": True, "message": "✅ Tarea actualizada exitosamente."}

        except Exception as e:
            return {"error": f"❌ Error al actualizar la tarea: {e}"}

    def eliminar_tarea(self, id_tarea):
        """📌 Elimina una tarea por su ID."""
        if not id_tarea:
            return {"error": "❌ El ID de la tarea es obligatorio para eliminar."}

        try:
            self.verificar_conexion()  # ✅ Asegurar conexión

            resultado = self.tarea_dao.eliminar_tarea(id_tarea)
            return resultado if "error" in resultado else {"success": True, "message": "✅ Tarea eliminada exitosamente."}

        except Exception as e:
            return {"error": f"❌ Error al eliminar la tarea: {e}"}
