<?php
include 'conexao.php';
   // Código para reservar sala (placeholder) e dados dos formulários para os scripts
if (isset($_POST['reservar_sala'])) {
    $sala_id = $_POST['sala_id'];
    $usuario = $_POST['usuario']; // Adicionado campo usuario
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
$conn->close();