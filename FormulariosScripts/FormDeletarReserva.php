<!DOCTYPE html>
<html>
<head>
    <title>Deletar Reserva</title>
</head>
<body>
    <h1>Deletar Reserva</h1>
    <form action="deletar_reserva.php" method="post">
        <label for="reserva_id">Selecione a Reserva:</label><br>
        <select id="reserva_id" name="reserva_id" required>
            <?php 
            ini_set('display_errors', 1);
            ini_set('display_startup_errors', 1);
            error_reporting(E_ALL);
            
            include 'ListarAsSalas.php'; // Reutilizando o script para listar as reservas (Deus abençoe pra nao dar gargalo)
            $sql = "SELECT r.id, r.inicio, r.fim, s.nome AS sala_nome, r.usuario 
                    FROM reservas r
                    JOIN salas s ON r.sala_id = s.id";
            $result = $conn->query($sql);
            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
                    echo "<option value='" . $row['id'] . "'>Reserva ID: " . $row['id'] . " - Sala: " . $row['sala_nome'] . " - Usuário: " . $row['usuario'] . " - Início: " . $row['inicio'] . " - Fim: " . $row['fim'] . "</option>";
                }
            } else {
                echo "<option value=''>Nenhuma reserva encontrada</option>";
            }
            $conn->close();
            ?>
        </select><br>
        <input type="submit" name="deletar_reserva" value="Deletar">
    </form>
</body>
</html>
