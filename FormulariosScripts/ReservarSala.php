<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

include 'conexao.php';

// Verifica se o formulário foi enviado
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Exibe o conteúdo de $_POST para depuração
    echo "<pre>";
    var_dump($_POST);
    echo "</pre>";

    if (isset($_POST['reservar_sala'])) {
        $sala_id = $_POST['sala_id'];
        $usuario = $_POST['usuario'];
        $dia = $_POST['dia'];
        $mes = $_POST['mes'];
        $inicio = $_POST['inicio'];
        $fim = $_POST['fim'];
        
        $ano = date("Y");

        // Formata as datas e horários de início e fim para o formato DATETIME do MySQL
        $inicio_datetime = "$ano-$mes-$dia $inicio:00";
        $fim_datetime = "$ano-$mes-$dia $fim:00";

        // Insere os dados na tabela reservas
        $sql = "INSERT INTO reservas (sala_id, usuario, inicio, fim) VALUES ('$sala_id', '$usuario', '$inicio_datetime', '$fim_datetime')";

        if ($conn->query($sql) === TRUE) {
            echo "Sala reservada com sucesso!<br>";
            
            // Atualiza a disponibilidade da sala
            $sql_update = "UPDATE salas SET disponivel = FALSE WHERE id = '$sala_id'";
            $conn->query($sql_update);
        } else {
            echo "Erro: " . $sql . "<br>" . $conn->error;
        }
    } else {
        echo "Botão de submissão não encontrado.";
    }
} else {
    echo "Formulário não submetido corretamente.";
}

$conn->close();
