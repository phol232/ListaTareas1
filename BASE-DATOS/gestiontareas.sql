create database GestionTareas;

use GestionTareas;

-- Tabla de Usuarios
CREATE TABLE users (
    id VARCHAR(12) PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);


CREATE TABLE Categorias (
    idCat VARCHAR(12) PRIMARY KEY NOT NULL,
    nombre VARCHAR(20) NOT NULL,
    fecha datetime
);

CREATE TABLE Tareas (
    idTarea VARCHAR(12) PRIMARY KEY NOT NULL,
    userId varchar (12),
    titulo varchar (12) not null,
    descripcion text,
	catId varchar (12),
    prioridad varchar (13) not null,
    estado varchar (12) not null,
    fecha datetime,
    FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (catId) REFERENCES Categorias(idCat) ON DELETE SET NULL
);
    
CREATE TABLE notifications (
    idNot VARCHAR(12) PRIMARY KEY NOT NULL,
    user_id VARCHAR(12),
    task_id VARCHAR(12),
    message TEXT NOT NULL,
    status ENUM('Unread', 'Read') DEFAULT 'Unread',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tareas(idTarea) ON DELETE CASCADE
);






