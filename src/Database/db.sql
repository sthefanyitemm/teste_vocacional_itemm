CREATE TABLE IF NOT EXISTS test_bd(
    nome varchar(50) NOT NULL,
    email varchar(40) NOT NULL,
    datanascimento date,
    telefone int(20)
    sexo enum('M','F','O')
    estado varchar(40)
    areainterresse varchar(40)
    cidade varchar(40)
    confirm tinyint(1)
    PRIMARY KEY('email')

)

