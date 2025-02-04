import mysql
from mysql.connector import Error
from src.Capa_Datos.Tarea import Tarea
from src.Capa_Conexion.ConexionMySql import ConexionMySql

class TareaDAO:
    def __init__(self, conexion=None):
        self.conexion = conexion if conexion else ConexionMySql.get_conexion_sesion()

    def crear_tarea(self, tarea: Tarea):
        if not self.conexion or not self.conexion.is_connected():
            return {"error": "❌ No hay una conexión activa con la base de datos."}
        try:
            with self.conexion.cursor() as cursor:
                procedimiento = "CrearTarea"
                valores = (
                    tarea.get_titulo(),
                    tarea.get_descripcion(),
                    tarea.get_cat_id(),
                    tarea.get_prioridad(),
                    tarea.get_estado(),
                    tarea.get_fecha()
                )
                cursor.callproc(procedimiento, valores)
                self.conexion.commit()
                print("✅ Tarea creada exitosamente.")
                return {"message": "✅ Tarea creada exitosamente."}
        except Error as e:
            print(f"❌ Error al crear la tarea: {e}")
            return {"error": f"❌ Error al crear la tarea: {e}"}

    def listar_tareas(self, user_id=None):
        if not self.conexion or not self.conexion.is_connected():
            return {"error": "❌ No hay una conexión activa con la base de datos."}

        tareas = []
        try:
            with self.conexion.cursor(dictionary=True, buffered=True) as cursor:
                print("📦 Ejecutando ListarTodasLasTareas()")
                print(f"👤 Cargando tareas para el usuario: {user_id}")

                # Llamada al procedimiento almacenado usando callproc()
                cursor.callproc("ListarTodasLasTareas", (user_id,))

                # Recuperar los resultados usando stored_results()
                resultados = []
                for result in cursor.stored_results():
                    # Se agrega cada fila devuelta por el procedimiento
                    resultados.extend(result.fetchall())

                print(f"📋 Resultados obtenidos desde MySQL: {resultados}")

                for fila in resultados:
                    tareas.append({
                        'titulo': fila.get('titulo', ''),
                        'descripcion': fila.get('descripcion', ''),
                        'categoria': fila.get('categoria', 'Sin categoría'),
                        'prioridad': fila.get('prioridad', ''),
                        'estado': fila.get('estado', ''),
                        'fecha': fila.get('fecha', '')
                    })

                print(f"✅ Tareas procesadas: {tareas}")
                return {"success": True, "tareas": tareas}
        except mysql.connector.Error as e:
            print(f"❌ Error al listar tareas: {e}")
            return {"error": f"❌ Error al listar tareas: {e}"}

    def actualizar_tarea(self, tarea: Tarea):
        if not self.conexion or not self.conexion.is_connected():
            return {"error": "❌ No hay una conexión activa con la base de datos."}
        try:
            with self.conexion.cursor() as cursor:
                procedimiento = "EditarTarea"
                valores = (
                    tarea.get_id_tarea(),
                    tarea.get_titulo(),
                    tarea.get_descripcion(),
                    tarea.get_cat_id(),
                    tarea.get_prioridad(),
                    tarea.get_estado(),
                    tarea.get_fecha()
                )
                cursor.callproc(procedimiento, valores)
                self.conexion.commit()
                print("✅ Tarea actualizada exitosamente.")
                return {"message": "✅ Tarea actualizada exitosamente."}
        except Error as e:
            print(f"❌ Error al actualizar la tarea: {e}")
            return {"error": f"❌ Error al actualizar la tarea: {e}"}

    def eliminar_tarea(self, id_tarea: str):
        if not self.conexion or not self.conexion.is_connected():
            return {"error": "❌ No hay una conexión activa con la base de datos."}
        try:
            with self.conexion.cursor() as cursor:
                procedimiento = "EliminarTarea"
                cursor.callproc(procedimiento, (id_tarea,))
                self.conexion.commit()
                print("✅ Tarea eliminada exitosamente.")
                return {"message": "✅ Tarea eliminada exitosamente."}
        except Error as e:
            print(f"❌ Error al eliminar la tarea: {e}")
            return {"error": f"❌ Error al eliminar la tarea: {e}"}
