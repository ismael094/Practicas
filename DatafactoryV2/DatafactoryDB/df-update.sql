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

