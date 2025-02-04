from mysql.connector import Error
from src.Capa_Datos.Tarea import Tarea
from src.Capa_Conexion.ConexionMySql import ConexionMySql

class TareaDAO:
    def __init__(self, conexion=None):
        # Usar la conexión de sesión activa o crear una nueva si no existe
        self.conexion = conexion if conexion else ConexionMySql.get_conexion_sesion()

    def crear_tarea(self, tarea: Tarea):
        if not self.conexion or not self.conexion.is_connected():
            return {"error": "❌ No hay una conexión activa con la base de datos."}

        try:
            with self.conexion.cursor() as cursor:
                procedimiento = "CALL CrearTarea(%s, %s, %s, %s, %s, %s)"
                valores = (
                    tarea.get_titulo(),
                    tarea.get_descripcion(),
                    tarea.get_cat_id(),
                    tarea.get_prioridad(),
                    tarea.get_estado(),
                    tarea.get_fecha()
                )
                cursor.execute(procedimiento, valores)
                self.conexion.commit()
                print("✅ Tarea creada exitosamente.")
                return {"message": "✅ Tarea creada exitosamente."}
        except Error as e:
            print(f"❌ Error al crear la tarea: {e}")
            return {"error": f"❌ Error al crear la tarea: {e}"}

    def listar_tareas(self):
        if not self.conexion or not self.conexion.is_connected():
            return {"error": "❌ No hay una conexión activa con la base de datos."}

        tareas = []
        try:
            with self.conexion.cursor(dictionary=True) as cursor:
                print("📦 Ejecutando ListarTodasLasTareas()")
                cursor.execute("CALL ListarTodasLasTareas()")

                resultados = cursor.fetchall()
                print(f"📋 Resultados obtenidos: {resultados}")

                for fila in resultados:
                    tarea = Tarea(
                        titulo=fila.get('titulo', ''),
                        descripcion=fila.get('descripcion', ''),
                        cat_id=fila.get('categoria', ''),
                        prioridad=fila.get('prioridad', ''),
                        estado=fila.get('estado', ''),
                        fecha=fila.get('fecha')
                    )
                    tareas.append(tarea.to_dict())

        except Error as e:
            print(f"❌ Error al listar tareas: {e}")
            return {"error": f"❌ Error al listar tareas: {e}"}

        return tareas

    def actualizar_tarea(self, tarea: Tarea):
        if not self.conexion or not self.conexion.is_connected():
            return {"error": "❌ No hay una conexión activa con la base de datos."}

        try:
            with self.conexion.cursor() as cursor:
                procedimiento = "CALL EditarTarea(%s, %s, %s, %s, %s, %s, %s)"
                valores = (
                    tarea.get_id_tarea(),
                    tarea.get_titulo(),
                    tarea.get_descripcion(),
                    tarea.get_cat_id(),
                    tarea.get_prioridad(),
                    tarea.get_estado(),
                    tarea.get_fecha()
                )
                cursor.execute(procedimiento, valores)
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
                procedimiento = "CALL EliminarTarea(%s)"
                cursor.execute(procedimiento, (id_tarea,))
                self.conexion.commit()
                print("✅ Tarea eliminada exitosamente.")
                return {"message": "✅ Tarea eliminada exitosamente."}
        except Error as e:
            print(f"❌ Error al eliminar la tarea: {e}")
            return {"error": f"❌ Error al eliminar la tarea: {e}"}
