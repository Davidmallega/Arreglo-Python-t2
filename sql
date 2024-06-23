CREATE TABLE productos (
id INT AUTO_INCREMENT PRIMARY KEY,
marca VARCHAR(50),
modelo VARCHAR(50),
talla VARCHAR(5),
color VARCHAR(20),
material VARCHAR(50),
unidades INT,
precio DECIMAL(10, 2)
);