DROP DATABASE IF EXISTS studshiny_django;
CREATE DATABASE studshiny_django CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE studshiny_django;

CREATE TABLE django_migrations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME(6) NOT NULL
);

CREATE TABLE django_content_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE KEY django_content_type_app_label_model_uniq (app_label, model)
);

CREATE TABLE auth_group (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE auth_permission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INT NOT NULL,
    codename VARCHAR(100) NOT NULL,
    UNIQUE KEY auth_permission_content_type_codename_uniq (content_type_id, codename),
    CONSTRAINT auth_permission_content_type_fk FOREIGN KEY (content_type_id) REFERENCES django_content_type(id)
);

CREATE TABLE auth_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME(6) NULL,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined DATETIME(6) NOT NULL
);

CREATE TABLE auth_user_groups (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    group_id INT NOT NULL,
    UNIQUE KEY auth_user_groups_user_group_uniq (user_id, group_id),
    CONSTRAINT auth_user_groups_user_fk FOREIGN KEY (user_id) REFERENCES auth_user(id),
    CONSTRAINT auth_user_groups_group_fk FOREIGN KEY (group_id) REFERENCES auth_group(id)
);

CREATE TABLE auth_user_user_permissions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    permission_id INT NOT NULL,
    UNIQUE KEY auth_user_permissions_user_permission_uniq (user_id, permission_id),
    CONSTRAINT auth_user_permissions_user_fk FOREIGN KEY (user_id) REFERENCES auth_user(id),
    CONSTRAINT auth_user_permissions_permission_fk FOREIGN KEY (permission_id) REFERENCES auth_permission(id)
);

CREATE TABLE auth_group_permissions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    permission_id INT NOT NULL,
    UNIQUE KEY auth_group_permissions_group_permission_uniq (group_id, permission_id),
    CONSTRAINT auth_group_permissions_group_fk FOREIGN KEY (group_id) REFERENCES auth_group(id),
    CONSTRAINT auth_group_permissions_permission_fk FOREIGN KEY (permission_id) REFERENCES auth_permission(id)
);

CREATE TABLE django_admin_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action_time DATETIME(6) NOT NULL,
    object_id LONGTEXT NULL,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT UNSIGNED NOT NULL,
    change_message LONGTEXT NOT NULL,
    content_type_id INT NULL,
    user_id INT NOT NULL,
    CONSTRAINT django_admin_log_content_type_fk FOREIGN KEY (content_type_id) REFERENCES django_content_type(id),
    CONSTRAINT django_admin_log_user_fk FOREIGN KEY (user_id) REFERENCES auth_user(id)
);

CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data LONGTEXT NOT NULL,
    expire_date DATETIME(6) NOT NULL
);

CREATE TABLE core_configuracionestudio (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    direccion VARCHAR(160) NOT NULL,
    telefono VARCHAR(40) NOT NULL,
    correo VARCHAR(254) NOT NULL,
    horario VARCHAR(160) NOT NULL,
    mensaje_cuidados LONGTEXT NOT NULL
);

CREATE TABLE core_galeriatrabajo (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(120) NOT NULL,
    descripcion LONGTEXT NOT NULL,
    imagen VARCHAR(255) NOT NULL,
    visible BOOLEAN NOT NULL,
    creado DATETIME(6) NOT NULL
);

CREATE TABLE core_producto (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    categoria VARCHAR(60) NOT NULL,
    material VARCHAR(60) NOT NULL,
    color VARCHAR(40) NOT NULL,
    calibre VARCHAR(40) NOT NULL,
    medida VARCHAR(40) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT UNSIGNED NOT NULL,
    stock_minimo INT UNSIGNED NOT NULL,
    descripcion LONGTEXT NOT NULL,
    imagen VARCHAR(255) NOT NULL,
    en_promocion BOOLEAN NOT NULL,
    estado VARCHAR(20) NOT NULL,
    creado DATETIME(6) NOT NULL,
    actualizado DATETIME(6) NOT NULL,
    CHECK (stock >= 0),
    CHECK (stock_minimo >= 0)
);

CREATE TABLE core_promocion (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    descripcion LONGTEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    activa BOOLEAN NOT NULL
);

CREATE TABLE core_cliente (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(140) NOT NULL,
    tipo_documento VARCHAR(60) NOT NULL,
    numero_documento VARCHAR(40) NOT NULL UNIQUE,
    edad INT UNSIGNED NOT NULL,
    tipo_sangre VARCHAR(20) NOT NULL,
    correo VARCHAR(254) NOT NULL UNIQUE,
    telefono VARCHAR(30) NOT NULL,
    contacto_emergencia VARCHAR(120) NOT NULL,
    tipo_perforacion_interes VARCHAR(80) NOT NULL,
    alergias_patologias LONGTEXT NOT NULL,
    numero_perforaciones INT UNSIGNED NOT NULL,
    creado DATETIME(6) NOT NULL,
    usuario_id INT NULL UNIQUE,
    CONSTRAINT core_cliente_usuario_fk FOREIGN KEY (usuario_id) REFERENCES auth_user(id),
    CHECK (edad >= 0),
    CHECK (numero_perforaciones >= 0)
);

CREATE TABLE core_procedimiento (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre_cliente VARCHAR(140) NOT NULL,
    telefono_cliente VARCHAR(30) NOT NULL,
    tipo_perforacion VARCHAR(100) NOT NULL,
    fecha_cita DATETIME(6) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    estado_pago BOOLEAN NOT NULL,
    notas_cuidados LONGTEXT NOT NULL,
    cliente_id BIGINT NULL,
    joya_utilizada_id BIGINT NULL,
    CONSTRAINT core_procedimiento_cliente_fk FOREIGN KEY (cliente_id) REFERENCES core_cliente(id),
    CONSTRAINT core_procedimiento_joya_fk FOREIGN KEY (joya_utilizada_id) REFERENCES core_producto(id)
);

CREATE TABLE core_procedimiento_materiales_medicos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    procedimiento_id BIGINT NOT NULL,
    producto_id BIGINT NOT NULL,
    UNIQUE KEY core_proc_materiales_uniq (procedimiento_id, producto_id),
    CONSTRAINT core_proc_materiales_proc_fk FOREIGN KEY (procedimiento_id) REFERENCES core_procedimiento(id),
    CONSTRAINT core_proc_materiales_prod_fk FOREIGN KEY (producto_id) REFERENCES core_producto(id)
);

CREATE TABLE core_factura (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    total DECIMAL(10,2) NOT NULL,
    fecha DATETIME(6) NOT NULL,
    metodo_pago VARCHAR(40) NOT NULL,
    pagada BOOLEAN NOT NULL,
    cliente_id BIGINT NULL,
    procedimiento_id BIGINT NULL,
    CONSTRAINT core_factura_cliente_fk FOREIGN KEY (cliente_id) REFERENCES core_cliente(id),
    CONSTRAINT core_factura_procedimiento_fk FOREIGN KEY (procedimiento_id) REFERENCES core_procedimiento(id)
);

INSERT INTO django_content_type (id, app_label, model) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'core', 'configuracionestudio'),
(8, 'core', 'galeriatrabajo'),
(9, 'core', 'producto'),
(10, 'core', 'promocion'),
(11, 'core', 'cliente'),
(12, 'core', 'procedimiento'),
(13, 'core', 'factura');

INSERT INTO django_migrations (app, name, applied) VALUES
('contenttypes', '0001_initial', NOW(6)),
('auth', '0001_initial', NOW(6)),
('admin', '0001_initial', NOW(6)),
('admin', '0002_logentry_remove_auto_add', NOW(6)),
('admin', '0003_logentry_add_action_flag_choices', NOW(6)),
('contenttypes', '0002_remove_content_type_name', NOW(6)),
('auth', '0002_alter_permission_name_max_length', NOW(6)),
('auth', '0003_alter_user_email_max_length', NOW(6)),
('auth', '0004_alter_user_username_opts', NOW(6)),
('auth', '0005_alter_user_last_login_null', NOW(6)),
('auth', '0006_require_contenttypes_0002', NOW(6)),
('auth', '0007_alter_validators_add_error_messages', NOW(6)),
('auth', '0008_alter_user_username_max_length', NOW(6)),
('auth', '0009_alter_user_last_name_max_length', NOW(6)),
('auth', '0010_alter_group_name_max_length', NOW(6)),
('auth', '0011_update_proxy_permissions', NOW(6)),
('auth', '0012_alter_user_first_name_max_length', NOW(6)),
('core', '0001_initial', NOW(6)),
('sessions', '0001_initial', NOW(6));

-- Accesos listos para Django.
-- Admin: admin@studshiny.com / 1234
-- Empleado: empleado@studshiny.com / 1234
-- Cliente: cliente@studshiny.com / cliente123
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
(1, 'pbkdf2_sha256$1000000$lfsmwcWhxwV8AMuFpy7wQL$1hVVuzXc9nFq21NQG56Fr151OgzRZJVRGKDCa4BVeV8=', NULL, TRUE, 'admin@studshiny.com', 'Administradora StudShiny', '', 'admin@studshiny.com', TRUE, TRUE, NOW(6)),
(2, 'pbkdf2_sha256$1000000$fNiIOskaf0axFsbsrppYbS$mq0HePAel1vlVeHfXq11SU+Rvm1CNhyep0EcgVtYhJg=', NULL, FALSE, 'empleado@studshiny.com', 'Empleado StudShiny', '', 'empleado@studshiny.com', TRUE, TRUE, NOW(6)),
(3, 'pbkdf2_sha256$1000000$M3TaRSamZa98yhEJep6ONT$AJpoM2FH7gN4Zph9YuAjmBCo5LRn6sw84ROo8XWWu+o=', NULL, FALSE, 'cliente@studshiny.com', 'Cliente Demo StudShiny', '', 'cliente@studshiny.com', FALSE, TRUE, NOW(6));

INSERT INTO core_cliente (id, nombre_completo, tipo_documento, numero_documento, edad, tipo_sangre, correo, telefono, contacto_emergencia, tipo_perforacion_interes, alergias_patologias, numero_perforaciones, creado, usuario_id) VALUES
(1, 'Cliente Demo StudShiny', 'Cedula de ciudadania', '1000000001', 22, 'O+', 'cliente@studshiny.com', '3001234567', 'Mama 3007654321', 'Septum', 'Sin alergias registradas', 2, NOW(6), 3);

INSERT INTO core_producto (id, nombre, categoria, material, color, calibre, medida, precio, stock, stock_minimo, descripcion, imagen, en_promocion, estado, creado, actualizado) VALUES
(1, 'Aro circular titanio', 'Circular', 'Titanio', 'Plateado', '16G', '8 mm', 45000.00, 20, 5, 'Joya corporal seleccionada para perforaciones seguras, con acabado pulido y estilo StudShiny.', 'core/images/circular-steel.jpeg', FALSE, 'DISPONIBLE', NOW(6), NOW(6)),
(2, 'Labret acero quirurgico', 'Labret', 'Acero Quirurgico', 'Plateado', '16G', '10 mm', 30000.00, 15, 5, 'Joya corporal seleccionada para perforaciones seguras, con acabado pulido y estilo StudShiny.', 'core/images/labret-steel.jpeg', FALSE, 'DISPONIBLE', NOW(6), NOW(6)),
(3, 'Barbell recto acero', 'Barbell', 'Acero Quirurgico', 'Plateado', '14G', '32 mm', 55000.00, 8, 5, 'Joya corporal seleccionada para perforaciones seguras, con acabado pulido y estilo StudShiny.', 'core/images/barbell-steel.jpeg', FALSE, 'DISPONIBLE', NOW(6), NOW(6)),
(4, 'Septum dorado con zirconias', 'Septum', 'Oro', 'Dorado', '16G', '8 mm', 70000.00, 5, 5, 'Joya corporal seleccionada para perforaciones seguras, con acabado pulido y estilo StudShiny.', 'core/images/septum-gold.jpeg', TRUE, 'DISPONIBLE', NOW(6), NOW(6)),
(5, 'Curved barbell plateado', 'Curved Barbell', 'Titanio', 'Plateado', '16G', '10 mm', 48000.00, 3, 5, 'Joya corporal seleccionada para perforaciones seguras, con acabado pulido y estilo StudShiny.', 'core/images/curved-barbell.jpeg', FALSE, 'DISPONIBLE', NOW(6), NOW(6));

INSERT INTO core_promocion (id, nombre, descripcion, precio, activa) VALUES
(1, 'Basico', 'Una perforacion con kit de limpieza y joya basica.', 50000.00, TRUE),
(2, 'Estandar', 'Dos perforaciones para una misma persona con kit de limpieza.', 90000.00, TRUE),
(3, 'VIP', 'Cinco perforaciones con joyas basicas o titanio y cuidados incluidos.', 150000.00, TRUE);

INSERT INTO core_procedimiento (id, nombre_cliente, telefono_cliente, tipo_perforacion, fecha_cita, estado, estado_pago, notas_cuidados, cliente_id, joya_utilizada_id) VALUES
(1, 'Cliente Demo StudShiny', '3001234567', 'Septum', DATE_ADD(NOW(6), INTERVAL 3 DAY), 'CONFIRMADA', TRUE, 'Limpiar con solucion salina dos veces al dia y evitar manipular la joya.', 1, 4);

INSERT INTO core_factura (id, total, fecha, metodo_pago, pagada, cliente_id, procedimiento_id) VALUES
(1, 70000.00, NOW(6), 'PSE', TRUE, 1, 1);

INSERT INTO core_galeriatrabajo (id, titulo, descripcion, imagen, visible, creado) VALUES
(1, 'Piercing labial', '', 'core/images/home-collage.jpeg', TRUE, NOW(6)),
(2, 'Joyeria circular', '', 'core/images/circular-steel.jpeg', TRUE, NOW(6));

INSERT INTO core_configuracionestudio (id, nombre, direccion, telefono, correo, horario, mensaje_cuidados) VALUES
(1, 'StudShiny', 'Bogota, Colombia', '+57 302 764 10 35', 'contacto@studshiny.com', 'Lunes a sabado, 10:00 a.m. a 7:00 p.m.', 'Lava la zona con solucion salina, evita tocar la perforacion y consulta al estudio ante molestias.');
