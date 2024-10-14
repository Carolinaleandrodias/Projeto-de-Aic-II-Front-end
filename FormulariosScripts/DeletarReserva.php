<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

session_start();
include 'conexao.php';

// Verificar se o usuário é professor(a)
if (!isset($_SESSION['id']) || $_SESSION['tipo_usuario'] !== 'professor') {

    echo "Você não tem permissão para acessar esta página.";
 
    exit();
}
include 'conexao.php';

if (isset($_POST['deletar_reserva'])) {
    $reserva_id = $_POST['reserva_id'];

    // Recuperar o ID da sala da reserva
    $sql = "SELECT sala_id FROM reservas WHERE id = '$reserva_id'";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $sala_id = $row['sala_id'];

        // Deletar a reserva
        $sql_delete = "DELETE FROM reservas WHERE id = '$reserva_id'";
        if ($conn->query($sql_delete) === TRUE) {
            echo "Reserva deletada com sucesso!<br>";

            // Atualizar a disponibilidade da sala
            $sql_update = "UPDATE salas SET disponivel = TRUE WHERE id = '$sala_id'";
            $conn->query($sql_update);
        } else {
            echo "Erro: " . $sql_delete . "<br>" . $conn->error;
        }
    } else {
        echo "Reserva não encontrada.";
    }

    $conn->close();
} else {
    echo "ID da reserva não fornecido.";
}
