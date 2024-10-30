<?php
// Connexion à la base de données
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "Climate_db";

try {
    $conn = new PDO("mysql:host=$servername", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Création de la base de données si elle n'existe pas
    $sql = "CREATE DATABASE IF NOT EXISTS $dbname";
    $conn->exec($sql);
    echo "Base de données créée avec succès<br>";

    // Connexion à la base de données créée
    $conn->exec("USE $dbname");

    // Création de la table CLimate_data
    $sql = "CREATE TABLE IF NOT EXISTS Climate_data (
        id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        temperature FLOAT NOT NULL,
        sunshine FLOAT NOT NULL
    )";
    $conn->exec($sql);
    echo "Table 'Climate_data' créée avec succès<br>";
} catch (PDOException $e) {
    echo "Erreur : " . $e->getMessage();
}

// Fermeture de la connexion
$conn = null;
?>
