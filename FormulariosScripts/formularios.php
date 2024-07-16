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

    <!-- Eu só quero mostrar o dia e o mês da reserva e as horas, mas o mysql precisa da data completa A-D-M // H-M-S então preciso extrair
      e concatenar no script depois pois precisa vir com o DATETIME completo então lá embaixo vai ta la -->
       
        <label for="dia">Dia (DD):</label><br>
        <input type="number" id="dia" name="dia" min="1" max="31"><br>
        
        <label for="mes">Mês (MM):</label><br>
        <input type="number" id="mes" name="mes" min="1" max="12"><br>
        
        <label for="inicio">Início (HH:MM):</label><br>
        <input type="text" id="inicio" name="inicio" placeholder="HH:MM"><br>
        <label for="fim">Fim (HH:MM):</label><br>
        <input type="text" id="fim" name="fim" placeholder="HH:MM"><br>
        <input type="submit" value="Reservar">
    </form>

    <!-- Exibir lista de salas (Tem que achar uma maneira de separar certinho as salas de cade prédio ((Mesmo que a sigla indique))) -->
    <h2>Lista de Salas</h2>
    <?php
    // Puxa o arquivo de configurações de conexão com o banco de dados (placeholder)  
      include 'conexao.php';

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

    // Código para reservar sala (placeholder) e dados dos formulários para os scripts
    if (isset($_POST['reservar_sala'])) {
        $sala_id = $_POST['sala_id'];
        $dia = $_POST['dia'];
        $mes = $_POST['mes'];
        $inicio = $_POST['inicio'];
        $fim = $_POST['fim'];

    // Aqui que pega o ano que deveria aparecer o formulário
        $ano = date("Y");

    // Força pra concatenar o dia, mês, ano e hora para formar o formato DATETIME pro mysql
        $inicio_datetime = "$ano-$mes-$dia $inicio:00";
        $fim_datetime = "$ano-$mes-$dia $fim:00";


    // Insere aqui os dados na tabela reservas
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

    // Código para listar salas (script)
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
