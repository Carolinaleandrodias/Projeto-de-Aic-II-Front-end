<?php
include 'conexao.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nome = trim($_POST['nome']);
    $email = trim($_POST['email']);
    $senha = $_POST['senha'];
    $tipo = $_POST['tipo']; #Se é aluno(a) ou professor(a)
    
    // Validações básicas
    if (empty($nome) || empty($email) || empty($senha) || empty($tipo)) {
        die("Por favor, preencha todos os campos.");
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        die("Email inválido.");
    }
    
    if (!in_array($tipo, ['professor', 'aluno'])) {
        die("Tipo de usuário inválido.");
    }
    
    // Hash da senha
    $senha_hash = password_hash($senha, PASSWORD_BCRYPT);
    
    // Inserir no banco de dados usando prepared statements
    $stmt = $conn->prepare("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("ssss", $nome, $email, $senha_hash, $tipo);
    
    if ($stmt->execute()) {
        echo "Usuário registrado";
    } else {
        if ($conn->errno == 1062) { // Duplicate entry
            echo "Email já registrado.";
        } else {
            echo "Erro: " . $stmt->error;
        }
    }
    
    $stmt->close();
    $conn->close();
}
