-- Suppression des tables existantes si elles sont déjà présentes
DROP TABLE IF EXISTS `Climate`;
DROP TABLE IF EXISTS `Time`;
DROP TABLE IF EXISTS `Location`;

-- Création de la table Location
CREATE TABLE `Location` (
  `ID` INT AUTO_INCREMENT PRIMARY KEY,
  `City` VARCHAR(255) NOT NULL,
  `Department` VARCHAR(255) NOT NULL,
  `Latitude` FLOAT NOT NULL,
  `Longitude` FLOAT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Création de la table Time
CREATE TABLE `Time` (
  `ID` INT AUTO_INCREMENT PRIMARY KEY,
  `HourTime` TIME NOT NULL,
  `DateTime` DATE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Création de la table Climate
CREATE TABLE `Climate` (
  `ID` INT AUTO_INCREMENT PRIMARY KEY,
  `LocationID` INT NOT NULL,
  `TimeID` INT NOT NULL,
  `Temperature` FLOAT NOT NULL,
  `Sunshine` FLOAT NOT NULL,
  `Humidity` FLOAT NOT NULL,
  `WindSpeed` FLOAT NOT NULL,
  `WeatherCondition` VARCHAR(255),
  FOREIGN KEY (`LocationID`) REFERENCES `Location`(`ID`) ON DELETE CASCADE,
  FOREIGN KEY (`TimeID`) REFERENCES `Time`(`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
