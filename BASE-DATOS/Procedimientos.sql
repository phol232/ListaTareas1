DELIMITER $$

CREATE PROCEDURE `CrearTarea`(
    IN p_titulo VARCHAR(12),
    IN p_descripcion TEXT,
    IN p_nombre_categoria VARCHAR(50),  -- Se recibe el nombre de la categoría
    IN p_prioridad VARCHAR(13),
    IN p_estado VARCHAR(12),
    IN p_fecha DATETIME
)
BEGIN
    DECLARE nuevo_id VARCHAR(12);
    DECLARE ultimo_num INT;
    DECLARE v_catId VARCHAR(12);

    -- Obtener el idCat correspondiente al nombre de la categoría
    SELECT idCat INTO v_catId
    FROM Categorias
    WHERE nombre = p_nombre_categoria
    LIMIT 1;

    -- Verificar si la categoría existe
    IF v_catId IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '❌ La categoría no existe.';
    ELSE
        -- Generar un nuevo idTarea en el formato TA-XXX
        SELECT IFNULL(MAX(CAST(SUBSTRING(idTarea, 4) AS UNSIGNED)), 0) + 1 INTO ultimo_num
        FROM Tareas;

        SET nuevo_id = CONCAT('TA-', LPAD(ultimo_num, 3, '0'));

        -- Insertar la nueva tarea con el idCat obtenido
        INSERT INTO Tareas (idTarea, titulo, descripcion, catId, prioridad, estado, fecha)
        VALUES (nuevo_id, p_titulo, p_descripcion, v_catId, p_prioridad, p_estado, p_fecha);
    END IF;
END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE `EditarTarea`(
    IN p_idTarea VARCHAR(12),
    IN p_titulo VARCHAR(12),
    IN p_descripcion TEXT,
    IN p_nombre_categoria VARCHAR(50), -- Se recibe el nombre de la categoría
    IN p_prioridad VARCHAR(13),
    IN p_estado VARCHAR(12),
    IN p_fecha DATETIME
)
BEGIN
    DECLARE v_catId VARCHAR(12);

    -- Obtener el idCat correspondiente al nombre de la categoría
    SELECT idCat INTO v_catId
    FROM Categorias
    WHERE nombre = p_nombre_categoria
    LIMIT 1;

    -- Verificar si la categoría existe
    IF v_catId IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '❌ La categoría no existe.';
    ELSE
        -- Actualizar la tarea con el idCat obtenido
        UPDATE Tareas
        SET titulo = p_titulo,
            descripcion = p_descripcion,
            catId = v_catId,
            prioridad = p_prioridad,
            estado = p_estado,
            fecha = p_fecha
        WHERE idTarea = p_idTarea;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE `EliminarTarea`(
    IN p_idTarea VARCHAR(12)
)
BEGIN
    DELETE FROM Tareas WHERE idTarea = p_idTarea;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE `ListarTodasLasTareas`(
    IN userIdParam VARCHAR(12)
)
BEGIN
    SELECT
        t.idTarea,
        t.titulo,
        t.descripcion,
        IFNULL(c.nombre, 'Sin categoría') AS categoria,
        t.prioridad,
        t.estado,
        t.fecha
    FROM 
        Tareas t
    LEFT JOIN 
        Categorias c ON t.catId = c.idCat
    WHERE 
        t.userId = userIdParam;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE `validate_user_login`(
    IN p_email VARCHAR(100),
    IN p_password_hash VARCHAR(255)
)
BEGIN
    DECLARE user_id VARCHAR(12);
    DECLARE user_name VARCHAR(100);
    DECLARE user_email VARCHAR(100);

    -- Verificar si existe un usuario con el email y la contraseña
    SELECT id, name, email 
    INTO user_id, user_name, user_email
    FROM users 
    WHERE email = p_email AND password_hash = p_password_hash
    LIMIT 1;

    -- Retornar resultado basado en la existencia del usuario
    IF user_id IS NOT NULL THEN
        SET @current_user_id = user_id;

        SELECT 'Login successful' AS message, user_id AS id, user_name AS name, user_email AS email;
    ELSE
        SELECT 'Invalid email or password' AS message;
    END IF;
END$$

DELIMITER ;
