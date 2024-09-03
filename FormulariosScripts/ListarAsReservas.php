<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

include 'conexao.php';

// Consultar todas as reservas
$sql = "SELECT r.id, s.nome AS sala_nome, r.usuario AS usuario_nome, r.inicio, r.fim
        FROM reservas r
        JOIN salas s ON r.sala_id = s.id
        ORDER BY r.inicio DESC";
$result = $conn->query($sql);

if (!$result) {
    echo "Erro na consulta ao banco de dados: " . $conn->error;
    exit();
}

// Exibir dados das reservas
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        echo "ID: " . htmlspecialchars($row['id']) . "<br>";
        echo "Sala: " . htmlspecialchars($row['sala_nome']) . "<br>";
        echo "Professor(a): " . htmlspecialchars($row['usuario_nome']) . "<br>";
        echo "Início: " . htmlspecialchars($row['inicio']) . "<br>";
        echo "Fim: " . htmlspecialchars($row['fim']) . "<br>";
        echo "<a href='deletar_reserva.php?id=" . urlencode($row['id']) . "' onclick=\"return confirm('Tem certeza que deseja deletar esta reserva?');\">Deletar</a><br><br>";
    }
} else {
    echo "Nenhuma reserva encontrada.";
}

$conn->close();
