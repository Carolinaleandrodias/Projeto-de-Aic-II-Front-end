<!-- Cabeçalho do HTML -->
<!DOCTYPE html>
<html>
<head>
    <title>Gerenciar as Salas</title>
</head>
<body>
    <h1>Gerenciamento de Salas</h1>

    <!-- Formulário para adicionar sala -->
    <h2>Adicionar Sala</h2>
    <form action="" method="post">
        <label for="nome">Nome:</label><br>
        <input type="text" id="nome" name="nome"><br>
        <label for="descricao">Descrição:</label><br>
        <textarea id="descricao" name="descricao"></textarea><br>
        <label for="capacidade">Capacidade:</label><br>
        <input type="number" id="capacidade" name="capacidade"><br>
        <input type="submit" name="adicionar_sala" value="Adicionar">
    </form>

    <!-- Formulário para reservar sala -->
    <h2>Reservar Sala</h2>
    <form action="" method="post">
        <label for="sala_id">ID da Sala:</label><br>
        <input type="number" id="sala_id" name="sala_id"><br>
        <label for="usuario">Usuário:</label><br>
        <input type="text" id="usuario" name="usuario"><br>
        <label for="inicio">Início (AAAA-MM-DD HH:MM:SS):</label><br>
        <input type="text" id="inicio" name="inicio"><br>
        <label for="fim">Fim (AAAA-MM-DD HH:MM:SS):</label><br>
        <input type="text" id="fim" name="fim"><br>
        <input type="submit" name="reservar_sala" value="Reservar">
    </form>

    <!-- Exibir lista de salas -->
    <h2>Lista de Salas</h2>
    <?php
    // Configurações de conexão com o banco de dados (place holder)
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "reserva_salas";

    // Cria conexão
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Verifica conexão
    if ($conn->connect_error) {
        die("Conexão falhou: " . $conn->connect_error);
    }
    // Scripts dos formularios PHP para as salas
    // Código para adicionar sala (placeholder)
    if (isset($_POST['adicionar_sala'])) {
        $nome = $_POST['nome'];
        $descricao = $_POST['descricao'];
        $capacidade = $_POST['capacidade'];

        $sql = "INSERT INTO salas (nome, descricao, capacidade) VALUES ('$nome', '$descricao', '$capacidade')";

        if ($conn->query($sql) === TRUE) {
            echo "Sala adicionada com sucesso!<br>";
        } else {
            echo "Erro: " . $sql . "<br>" . $conn->error;
        }
    }

    // Código para reservar sala (placeholder)
    if (isset($_POST['reservar_sala'])) {
        $sala_id = $_POST['sala_id'];
        $usuario = $_POST['usuario'];
        $inicio = $_POST['inicio'];
        $fim = $_POST['fim'];

        $sql = "INSERT INTO reservas (sala_id, usuario, inicio, fim) VALUES ('$sala_id', '$usuario', '$inicio', '$fim')";

        if ($conn->query($sql) === TRUE) {
            echo "Sala reservada com sucesso!<br>";
            // Atualiza disponibilidade da sala
            $sql_update = "UPDATE salas SET disponivel = FALSE WHERE id = '$sala_id'";
            $conn->query($sql_update);
        } else {
            echo "Erro: " . $sql . "<br>" . $conn->error;
        }
    }

    // Código para listar salas
    $sql = "SELECT * FROM salas";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            echo "Sala: " . $row["nome"]. " - Capacidade: " . $row["capacidade"]. " - Disponível: " . ($row["disponivel"] ? 'Sim' : 'Não'). "<br>";
        }
    } else {
        echo "0 resultados";
    }

    $conn->close();
    ?>
</body>
</html>
