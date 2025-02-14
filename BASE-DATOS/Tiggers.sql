-- TIGGERS --

DELIMITER $$

CREATE TRIGGER before_insert_tarea
BEFORE INSERT ON Tareas
FOR EACH ROW
BEGIN
    -- Verificar si la variable de sesión @current_user_id está definida
    IF @current_user_id IS NOT NULL THEN
        SET NEW.userId = @current_user_id;
    ELSE
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Error: No user logged in to assign the task.';
    END IF;
END $$

DELIMITER ;


SELECT @current_user_id;


..

