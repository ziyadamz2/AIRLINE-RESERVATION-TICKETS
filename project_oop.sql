-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : lun. 04 déc. 2023 à 22:19
-- Version du serveur : 10.4.27-MariaDB
-- Version de PHP : 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `project_oop`
--

-- --------------------------------------------------------

--
-- Structure de la table `flight`
--

CREATE TABLE `flight` (
  `flight_id` int(16) NOT NULL,
  `flight_number` varchar(255) NOT NULL,
  `departure_airport` varchar(255) NOT NULL,
  `arrival_airport` varchar(255) NOT NULL,
  `departing` date NOT NULL,
  `timings` time NOT NULL,
  `take_off_time` time NOT NULL,
  `place` int(11) NOT NULL,
  `price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `flight`
--

INSERT INTO `flight` (`flight_id`, `flight_number`, `departure_airport`, `arrival_airport`, `departing`, `timings`, `take_off_time`, `place`, `price`) VALUES
(1, 'A380', 'Paris', 'London', '2023-12-05', '07:00:00', '05:00:00', 77, 288.99),
(2, 'A590', 'Rabat', 'Paris', '2023-12-24', '02:00:00', '15:00:00', 230, 120.89),
(14, 'A380', 'Rome', 'London', '2023-12-04', '07:00:00', '00:00:05', 100, 288.99),
(15, 'A380', 'Paris', 'Monaco', '2023-12-07', '07:00:00', '05:00:00', 77, 288.99),
(16, 'A380', 'Paris', 'Monaco', '2023-12-07', '07:00:00', '15:00:00', 77, 288.99),
(17, 'A380', 'Paris', 'Monaco', '2023-12-07', '07:00:00', '15:30:00', 77, 288.99),
(18, 'A380', 'Paris', 'Monaco', '2023-12-08', '07:00:00', '15:30:00', 77, 288.99),
(19, 'A380', 'Paris', 'Nice', '2023-12-08', '07:00:00', '16:30:00', 77, 288.99);

-- --------------------------------------------------------

--
-- Structure de la table `historique`
--

CREATE TABLE `historique` (
  `historic_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `flight_id` int(11) NOT NULL,
  `number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `historique`
--

INSERT INTO `historique` (`historic_id`, `member_id`, `flight_id`, `number`) VALUES
(35, 10, 1, 7),
(36, 10, 14, 1),
(37, 10, 15, 1),
(39, 0, 15, 2),
(40, 10, 16, 2),
(41, 10, 18, 2),
(42, 10, 2, 2);

-- --------------------------------------------------------

--
-- Structure de la table `member`
--

CREATE TABLE `member` (
  `member_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `age` int(11) NOT NULL,
  `adress` varchar(255) NOT NULL,
  `permission` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `member`
--

INSERT INTO `member` (`member_id`, `name`, `email`, `password`, `age`, `adress`, `permission`) VALUES
(1, 'admin', 'admin', 'admin', 84, '55 street', 1),
(10, 'test', 'test', 'test', 19, '15 avenue du belver', 0),
(22, 'test', 'paul', 'test', 19, '15 avenue du belver', 0),
(23, 'test', 'jack', 'test', 19, '15 avenue du tgt', 0),
(24, 'test', 'quacoubeh', 'test', 19, '15 rue des tilleuls', 0),
(25, 'test', 'colins', 'test', 19, '15 rue des till', 0);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`flight_id`);

--
-- Index pour la table `historique`
--
ALTER TABLE `historique`
  ADD PRIMARY KEY (`historic_id`);

--
-- Index pour la table `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`member_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `flight`
--
ALTER TABLE `flight`
  MODIFY `flight_id` int(16) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT pour la table `historique`
--
ALTER TABLE `historique`
  MODIFY `historic_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT pour la table `member`
--
ALTER TABLE `member`
  MODIFY `member_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
