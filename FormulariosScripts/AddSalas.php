<?php
include 'conexao.php';
// Código para adicionar sala (placeholder)
    if (isset($_POST['adicionar_sala'])) {
        $nome = $_POST['nome'];
        $descrição = $_POST['descrição'];

        $sql = "INSERT INTO salas (nome, descrição) VALUES ('$nome', '$descrição')";

        if ($conn->query($sql) === TRUE) {
            echo "Sala adicionada com sucesso!<br>";
        } else {
            echo "Erro: " . $sql . "<br>" . $conn->error;
        }
    }