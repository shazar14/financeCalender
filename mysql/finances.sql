-- MySQL dump 10.13  Distrib 5.6.10, for osx10.8 (x86_64)
--
-- Host: localhost    Database: finances2
-- ------------------------------------------------------
-- Server version	5.6.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `finances2`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `finances` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `finances`;

--
-- Table structure for table `tbl_Accounts`
--

DROP TABLE IF EXISTS `tbl_Accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_Accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_Accounts`
--

LOCK TABLES `tbl_Accounts` WRITE;
/*!40000 ALTER TABLE `tbl_Accounts` DISABLE KEYS */;
INSERT INTO `tbl_Accounts` VALUES (1,'Wright-Patt'),(2,'Checking'),(3,'None');
/*!40000 ALTER TABLE `tbl_Accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_April`
--

DROP TABLE IF EXISTS `tbl_April`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_April` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_april_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_April`
--

LOCK TABLES `tbl_April` WRITE;
/*!40000 ALTER TABLE `tbl_April` DISABLE KEYS */;
INSERT INTO `tbl_April` VALUES (1,2,'Paid',4,58.00),(2,3,'Paid',10,25.00),(3,4,'Paid',5,86.50),(4,5,'Paid',12,393.00),(5,6,'Paid',25,50.00),(6,7,'Paid',1,857.65),(7,8,'Paid',16,60.00),(8,9,'Paid',24,17.05),(9,10,'Paid',21,40.29),(10,11,'Paid',7,47.25),(11,12,'Paid',30,28.00),(12,13,'Paid',10,58.00),(13,14,'Paid',28,139.67),(14,15,'Paid',22,75.28);
/*!40000 ALTER TABLE `tbl_April` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_August`
--

DROP TABLE IF EXISTS `tbl_August`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_August` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_august_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_August`
--

LOCK TABLES `tbl_August` WRITE;
/*!40000 ALTER TABLE `tbl_August` DISABLE KEYS */;
INSERT INTO `tbl_August` VALUES (1,2,'Paid',9,58.00),(2,3,'Due',10,25.00),(3,4,'Paid',5,86.50),(4,5,'Due',12,393.00),(5,6,'Due',25,50.00),(6,7,'Paid',1,857.65),(7,8,'Due',16,60.00),(8,9,'Due',24,17.05),(9,10,'Due',21,40.29),(10,11,'Paid',7,47.25),(11,12,'Due',30,28.00),(12,13,'Due',10,58.00),(13,14,'Due',28,139.67),(14,15,'Due',22,75.28);
/*!40000 ALTER TABLE `tbl_August` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_Bills`
--

DROP TABLE IF EXISTS `tbl_Bills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_Bills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `amount_due` decimal(6,2) DEFAULT NULL,
  `day_of_month` int(11) DEFAULT NULL,
  `payment_type` enum('Automatic','Manual') DEFAULT NULL,
  `account_index` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `test` (`account_index`),
  CONSTRAINT `tbl_bills_ibfk_1` FOREIGN KEY (`account_index`) REFERENCES `tbl_Accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_Bills`
--

LOCK TABLES `tbl_Bills` WRITE;
/*!40000 ALTER TABLE `tbl_Bills` DISABLE KEYS */;
INSERT INTO `tbl_Bills` VALUES (2,'Discover',58.00,9,'Automatic',2),(3,'Capitol One',25.00,10,'Automatic',2),(4,'Verizon',86.50,5,'Automatic',1),(5,'Car Loan',393.00,12,'Automatic',2),(6,'Wright Pat',50.00,25,'Automatic',2),(7,'Mortgage',857.65,1,'Manual',3),(8,'Directv',60.00,16,'Automatic',2),(9,'Intermountain Gas',17.05,24,'Manual',3),(10,'Rocky Mountain Electric',40.29,21,'Automatic',2),(11,'Water/garbage',47.25,7,'Automatic',2),(12,'Sewage',28.00,30,'Automatic',2),(13,'Cable One',58.00,10,'Automatic',1),(14,'Nelnet',139.67,28,'Automatic',2),(15,'Sallie Mae',75.28,22,'Manual',3);
/*!40000 ALTER TABLE `tbl_Bills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_December`
--

DROP TABLE IF EXISTS `tbl_December`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_December` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_december_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_December`
--

LOCK TABLES `tbl_December` WRITE;
/*!40000 ALTER TABLE `tbl_December` DISABLE KEYS */;
INSERT INTO `tbl_December` VALUES (1,2,'Due',4,58.00),(2,3,'Due',10,25.00),(3,4,'Due',5,86.50),(4,5,'Due',12,393.00),(5,6,'Due',25,50.00),(6,7,'Due',1,857.65),(7,8,'Due',16,60.00),(8,9,'Due',24,17.05),(9,10,'Due',21,40.29),(10,11,'Due',7,47.25),(11,12,'Due',30,28.00),(12,13,'Due',10,58.00),(13,14,'Due',28,139.67),(14,15,'Due',22,75.28);
/*!40000 ALTER TABLE `tbl_December` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_February`
--

DROP TABLE IF EXISTS `tbl_February`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_February` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_february_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_February`
--

LOCK TABLES `tbl_February` WRITE;
/*!40000 ALTER TABLE `tbl_February` DISABLE KEYS */;
INSERT INTO `tbl_February` VALUES (1,2,'Paid',4,58.00),(2,3,'Paid',10,25.00),(3,4,'Paid',5,86.50),(4,5,'Paid',12,393.00),(5,6,'Paid',25,50.00),(6,7,'Paid',1,857.65),(7,8,'Paid',16,60.00),(8,9,'Paid',24,17.05),(9,10,'Paid',21,40.29),(10,11,'Paid',7,47.25),(11,12,'Paid',30,28.00),(12,13,'Paid',10,58.00),(13,14,'Paid',28,139.67),(14,15,'Paid',22,75.28);
/*!40000 ALTER TABLE `tbl_February` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_January`
--

DROP TABLE IF EXISTS `tbl_January`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_January` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_january_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_January`
--

LOCK TABLES `tbl_January` WRITE;
/*!40000 ALTER TABLE `tbl_January` DISABLE KEYS */;
INSERT INTO `tbl_January` VALUES (1,2,'Paid',4,58.00),(2,3,'Paid',10,25.00),(3,4,'Paid',5,86.50),(4,5,'Paid',12,393.00),(5,6,'Paid',25,50.00),(6,7,'Paid',1,857.65),(7,8,'Paid',16,60.00),(8,9,'Paid',24,17.05),(9,10,'Paid',21,40.29),(10,11,'Paid',7,47.25),(11,12,'Paid',30,28.00),(12,13,'Paid',10,58.00),(13,14,'Paid',28,139.67),(14,15,'Paid',22,75.28);
/*!40000 ALTER TABLE `tbl_January` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_July`
--

DROP TABLE IF EXISTS `tbl_July`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_July` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_july_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_July`
--

LOCK TABLES `tbl_July` WRITE;
/*!40000 ALTER TABLE `tbl_July` DISABLE KEYS */;
INSERT INTO `tbl_July` VALUES (1,2,'Paid',4,58.00),(2,3,'Paid',10,25.00),(3,4,'Paid',5,86.50),(4,5,'Paid',12,393.00),(5,6,'Paid',25,50.00),(6,7,'Paid',1,857.65),(7,8,'Paid',12,60.00),(8,9,'Paid',24,17.05),(9,10,'Paid',21,40.29),(10,11,'Paid',7,47.25),(11,12,'Paid',30,28.00),(12,13,'Paid',10,58.00),(13,14,'Paid',28,139.67),(14,15,'Paid',22,75.28);
/*!40000 ALTER TABLE `tbl_July` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_June`
--

DROP TABLE IF EXISTS `tbl_June`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_June` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_june_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_June`
--

LOCK TABLES `tbl_June` WRITE;
/*!40000 ALTER TABLE `tbl_June` DISABLE KEYS */;
INSERT INTO `tbl_June` VALUES (1,2,'Paid',4,58.00),(2,3,'Paid',10,25.00),(3,4,'Paid',5,86.50),(4,5,'Paid',12,393.00),(5,6,'Paid',25,50.00),(6,7,'Paid',1,857.65),(7,8,'Paid',16,60.00),(8,9,'Paid',24,17.05),(9,10,'Paid',21,40.29),(10,11,'Paid',7,47.25),(11,12,'Paid',30,28.00),(12,13,'Paid',10,58.00),(13,14,'Paid',28,139.67),(14,15,'Paid',22,75.28);
/*!40000 ALTER TABLE `tbl_June` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_March`
--

DROP TABLE IF EXISTS `tbl_March`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_March` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_march_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_March`
--

LOCK TABLES `tbl_March` WRITE;
/*!40000 ALTER TABLE `tbl_March` DISABLE KEYS */;
INSERT INTO `tbl_March` VALUES (1,2,'Paid',4,58.00),(2,3,'Paid',10,25.00),(3,4,'Paid',5,86.50),(4,5,'Paid',12,393.00),(5,6,'Paid',25,50.00),(6,7,'Paid',1,857.65),(7,8,'Paid',16,60.00),(8,9,'Paid',24,17.05),(9,10,'Paid',21,40.29),(10,11,'Paid',7,47.25),(11,12,'Paid',30,28.00),(12,13,'Paid',10,58.00),(13,14,'Paid',28,139.67),(14,15,'Paid',22,75.28);
/*!40000 ALTER TABLE `tbl_March` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_May`
--

DROP TABLE IF EXISTS `tbl_May`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_May` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_may_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_May`
--

LOCK TABLES `tbl_May` WRITE;
/*!40000 ALTER TABLE `tbl_May` DISABLE KEYS */;
INSERT INTO `tbl_May` VALUES (1,2,'Paid',4,58.00),(2,3,'Paid',10,25.00),(3,4,'Paid',5,86.50),(4,5,'Paid',12,393.00),(5,6,'Paid',25,50.00),(6,7,'Paid',1,857.65),(7,8,'Paid',16,60.00),(8,9,'Paid',24,17.05),(9,10,'Paid',21,40.29),(10,11,'Paid',7,47.25),(11,12,'Paid',30,28.00),(12,13,'Paid',10,58.00),(13,14,'Paid',28,139.67),(14,15,'Paid',22,75.28);
/*!40000 ALTER TABLE `tbl_May` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_November`
--

DROP TABLE IF EXISTS `tbl_November`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_November` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_november_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_November`
--

LOCK TABLES `tbl_November` WRITE;
/*!40000 ALTER TABLE `tbl_November` DISABLE KEYS */;
INSERT INTO `tbl_November` VALUES (1,2,'Due',4,58.00),(2,3,'Due',10,25.00),(3,4,'Due',5,86.50),(4,5,'Due',12,393.00),(5,6,'Due',25,50.00),(6,7,'Due',1,857.65),(7,8,'Due',16,60.00),(8,9,'Due',24,17.05),(9,10,'Due',21,40.29),(10,11,'Due',7,47.25),(11,12,'Due',30,28.00),(12,13,'Due',10,58.00),(13,14,'Due',28,139.67),(14,15,'Due',22,75.28);
/*!40000 ALTER TABLE `tbl_November` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_October`
--

DROP TABLE IF EXISTS `tbl_October`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_October` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_october_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_October`
--

LOCK TABLES `tbl_October` WRITE;
/*!40000 ALTER TABLE `tbl_October` DISABLE KEYS */;
INSERT INTO `tbl_October` VALUES (1,2,'Due',4,58.00),(2,3,'Due',10,25.00),(3,4,'Due',5,86.50),(4,5,'Due',12,393.00),(5,6,'Due',25,50.00),(6,7,'Due',1,857.65),(7,8,'Due',16,60.00),(8,9,'Due',24,17.05),(9,10,'Due',21,40.29),(10,11,'Due',7,47.25),(11,12,'Due',30,28.00),(12,13,'Due',10,58.00),(13,14,'Due',28,139.67),(14,15,'Due',22,75.28);
/*!40000 ALTER TABLE `tbl_October` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_September`
--

DROP TABLE IF EXISTS `tbl_September`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_September` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `status` enum('Paid','Due','Skip') NOT NULL,
  `day_of_month` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `tbl_september_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `tbl_Bills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_September`
--

LOCK TABLES `tbl_September` WRITE;
/*!40000 ALTER TABLE `tbl_September` DISABLE KEYS */;
INSERT INTO `tbl_September` VALUES (1,2,'Due',4,58.00),(2,3,'Due',10,25.00),(3,4,'Due',5,86.50),(4,5,'Due',12,393.00),(5,6,'Due',25,50.00),(6,7,'Due',1,857.65),(7,8,'Due',16,60.00),(8,9,'Due',24,17.05),(9,10,'Due',21,40.29),(10,11,'Due',7,47.25),(11,12,'Due',30,28.00),(12,13,'Due',10,58.00),(13,14,'Due',28,139.67),(14,15,'Due',22,75.28);
/*!40000 ALTER TABLE `tbl_September` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-08-11 17:35:02
