<?php
// Incluindo o arquivo de conexão com o banco de dados
include 'conexao.php';

//// Consultar salas do banco de dados, ordenadas por pavilhão ou o que der (não faço ideia como vou separar isso ainda)
$sql = "SELECT * FROM salas ORDER BY nome";
$result = $conn->query($sql);

$pavilhao_atual = '';

// Exibir lista de salas agrupadas por pavilhão ou prédio
echo "<h2>Lista de Salas</h2>";
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $nome_sala = $row['nome'];
        // Verificar se o nome começa com números ou letras (não sei como isso funciona)
        if (is_numeric(substr($nome_sala, 0, 1))) {
            $pavilhao = substr($nome_sala, 0, 1); // Primeiro caractere para pavilhões numerados
        } else {
            $pavilhao = substr($nome_sala, 0, 2); // Primeiros dois caracteres para prédios com sigla
        }
        
        if ($pavilhao !== $pavilhao_atual) {
            if ($pavilhao_atual !== '') {
                echo "</ul>"; // Fecha a lista do pavilhão ou prédio anterior
            }
            echo "<h3>Pavilhão/Prédio: $pavilhao</h3>";
            echo "<ul>"; // Abre uma nova lista para o novo pavilhão ou prédio
            $pavilhao_atual = $pavilhao;
        }
        
        echo "<li>Sala: " . $row['nome'] . " - Capacidade: " . $row['capacidade'] . " - Disponível: " . ($row['disponivel'] ? 'Sim' : 'Não') . "</li>";
    }
    echo "</ul>"; // Fecha a última lista
} else {
    echo "Nenhuma sala encontrada.";
}

$conn->close();