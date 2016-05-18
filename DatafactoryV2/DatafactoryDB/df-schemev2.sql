-- MySQL dump 10.13  Distrib 5.5.38, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: df
-- ------------------------------------------------------
-- Server version	5.5.38-0ubuntu0.14.04.1

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
-- Table structure for table `camera`
--

DROP TABLE IF EXISTS `camera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camera` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `instrument` varchar(255) NOT NULL,
  `camera` varchar(255) NOT NULL,
  `gcs_component` varchar(255) NOT NULL,
  `display_name` varchar(255) NOT NULL,
  `archive_directory` varchar(255) NOT NULL,
  `active` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fitsKeyword_df`
--

DROP TABLE IF EXISTS `fitsKeyword_df`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fitsKeyword_df` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_observation_mode` int(11) NOT NULL,
  `store_in_db` tinyint(4) NOT NULL,
  `gather_process` enum('FROM_DAS','FROM_MONITOR','CALCULATED','FROM_SEQUENCE') NOT NULL,
  `gcs_component` varchar(255) DEFAULT NULL,
  `gcs_monitor` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `data_type` varchar(255) DEFAULT NULL,
  `enum_label` varchar(255) DEFAULT NULL,
  `dfrange` varchar(255) DEFAULT NULL,
  `monitor_type` enum('SAMPLED','DISCRETE') NOT NULL,
  `convertion` enum('RAD_TO_HMS','RAD_TO_DMS','RAD_TO_DEG') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_obsmode` (`id_observation_mode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `frame`
--

DROP TABLE IF EXISTS `frame`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `frame` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_camera` int(11) NOT NULL,
  `id_observation_mode` int(11) NOT NULL,
  `observation_date` datetime NOT NULL,
  `observation_date_microsecond` int(11) NOT NULL,
  `exposition_time` float NOT NULL,
  `state` varchar(255) NOT NULL,
  `is_raw` tinyint(4) NOT NULL,
  `id_program` varchar(255) NOT NULL,
  `id_observation_block` varchar(255) NOT NULL,
  `path` varchar(255) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `number_extensions` int(11) NOT NULL,
  `number_frame` int(25) NOT NULL,
  `id_principal_investigator` varchar(255) DEFAULT NULL,
  `radeg` double DEFAULT NULL,
  `decdeg` double DEFAULT NULL,
  PRIMARY KEY (`id`,`observation_date`),
  KEY `frame_index` (`id_camera`,`id_observation_mode`,`observation_date`,`radeg`,`decdeg`,`exposition_time`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1
/*!50100 PARTITION BY HASH ( DAYOFYEAR(observation_date))
PARTITIONS 365 */;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `header`
--

DROP TABLE IF EXISTS `header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `header` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_header_definition` int(11) NOT NULL,
  `id_frame` int(11) NOT NULL,
  `order_keyword` int(11) NOT NULL,
  `extension` int(11) NOT NULL,
  `string_value` varchar(255) DEFAULT NULL,
  `long_value` int(11) DEFAULT NULL,
  `double_value` double DEFAULT NULL,
  PRIMARY KEY (`id`,`id_frame`, `id_header_definition`),
  KEY `header_index` (`id_frame`)
) ENGINE=InnoDB AUTO_INCREMENT=16356 DEFAULT CHARSET=latin1
/*!50100 PARTITION BY HASH ( `id_frame`)
PARTITIONS 1000 */;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `header_definition`
--

DROP TABLE IF EXISTS `header_definition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `header_definition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` varchar(256) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `data_type` varchar(256) DEFAULT NULL,
  `version` int(11) DEFAULT 0,
  `visible` tinyint(1) DEFAULT NULL,
  `id_camera` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`,`id_camera`),
  KEY `header_definition_index` (`id_camera`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1123 DEFAULT CHARSET=latin1
/*!50100 PARTITION BY HASH ( id_camera)
PARTITIONS 100 */;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `observation_mode`
--

DROP TABLE IF EXISTS `observation_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `observation_mode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mode` varchar(255) NOT NULL,
  `id_camera` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `observation_mode_index` (`id_camera`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `observation_result`
--

DROP TABLE IF EXISTS `observation_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `observation_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_observation_mode` int(11) NOT NULL,
  `commit_date` datetime NOT NULL,
  `id_program` varchar(255) DEFAULT NULL,
  `id_observation_block` varchar(255) NOT NULL,
  `path` varchar(255) NOT NULL,
  PRIMARY KEY (`id`,`commit_date`),
  KEY `observation_result_index` (`id_observation_mode`,`commit_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
/*!50100 PARTITION BY HASH ( DAYOFYEAR(commit_date))
PARTITIONS 365 */;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `observation_result_frame`
--

DROP TABLE IF EXISTS `observation_result_frame`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `observation_result_frame` (
  `id_observation_result` int(11) NOT NULL,
  `id_frame` int(11) NOT NULL,
  PRIMARY KEY (`id_observation_result`,`id_frame`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reduction_result`
--

DROP TABLE IF EXISTS `reduction_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reduction_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_observation_result` int(11) DEFAULT NULL,
  `reduction_date` datetime NOT NULL,
  `id_program` varchar(255) DEFAULT NULL,
  `id_observation_block` varchar(255) NOT NULL,
  `id_observation_mode` int(11) NOT NULL,
  `path` varchar(255) NOT NULL,
  `qc` enum('QC_GOOD','QC_BAD','QC_PARTIAL','QC_UNKNOWN') NOT NULL DEFAULT 'QC_UNKNOWN',
  PRIMARY KEY (`id`,`reduction_date`),
  KEY `reduction_result_index` (`id_observation_result`,`reduction_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
/*!50100 PARTITION BY HASH ( DAYOFYEAR(reduction_date))
PARTITIONS 365 */;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `reduction_result_data`;
CREATE TABLE `reduction_result_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `id_reduction_result` int(11) NOT NULL,
  `string_value` varchar(255) DEFAULT NULL,
  `long_value` int(11) DEFAULT NULL,
  `double_value` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `reduction_result_data_config`;
CREATE TABLE `reduction_result_data_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_observation_mode` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `filter` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sequence_table`
--

DROP TABLE IF EXISTS `sequence_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sequence_table` (
  `seq_name` varchar(255) NOT NULL,
  `seq_count` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `enabled` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_role`
--

DROP TABLE IF EXISTS `user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_role` (
  `username` varchar(255) NOT NULL,
  `role` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-10-16 16:49:21
