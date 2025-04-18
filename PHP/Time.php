<?php
// Connexion à la base de données
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "Time_db";

try {
    $conn = new PDO("mysql:host=$servername", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $sql = "CREATE DATABASE IF NOT EXISTS $dbname";
    $conn->exec($sql);
    echo "Base de données créée avec succès<br>";

    $conn->exec("USE $dbname");

    // Création de la table Time_data
    $sql = "CREATE TABLE IF NOT EXISTS Time_data (
        id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        HourTime TIME NOT NULL,
        DatTime DATE NOT NULL
    )";
    $conn->exec($sql);
    echo "Table 'Time_data' créée avec succès<br>";
} catch (PDOException $e) {
    echo "Erreur : " . $e->getMessage();
}

$conn = null;
?>
