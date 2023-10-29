SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
CREATE DATABASE edubase;
USE edubase;
--

-- --------------------------------------------------------

--
-- Table structure for table `students_src`
--
DROP TABLE IF EXISTS `students_src`;
CREATE TABLE IF NOT EXISTS `students_src`(
  `roll_no` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY(`roll_no`)
);

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--
DROP TABLE IF EXISTS `attendance`;
CREATE TABLE IF NOT EXISTS `attendance` (
  `roll_no` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`roll_no`)
);

-- --------------------------------------------------------

--
-- Table structure for table `marks`
--
DROP TABLE IF EXISTS `marks`;
CREATE TABLE IF NOT EXISTS `marks` (
  `roll_no` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `UT-1` int,
  `UT-2` int,
  `Internals-1` int,
  `Mid-Term` int,
  `UT-3` int,
  `UT-4` int,
  `Internals-2` int,
  `Annuals` int,
  PRIMARY KEY (`roll_no`)
);

-- --------------------------------------------------------

--
-- Remove table 'submission', if exists
--

DROP TABLE IF EXISTS `submission`;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;