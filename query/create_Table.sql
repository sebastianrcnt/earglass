SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema team9
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `team9` DEFAULT CHARACTER SET utf8 ;
USE `team9` ;

-- -----------------------------------------------------
-- Table `team9`.`USERTYPE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `team9`.`USERTYPE` (
  `UserTypeName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`UserTypeName`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `team9`.`USER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `team9`.`USER` (
  `idUSER` int(11) NOT NULL AUTO_INCREMENT,
  `Id` varchar(45) NOT NULL,
  `Password` varchar(45) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Gender` varchar(1) NOT NULL,
  `BirthDate` varchar(8) NOT NULL,
  `PhoneNum` varchar(13) NOT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `UserScore` float DEFAULT 50,
  `FK_UserTypeName` varchar(45) NOT NULL,
  INDEX `FK_UserTypeName_idx` (`FK_UserTypeName` ASC),
  UNIQUE INDEX `PhoneNum_UNIQUE` (`PhoneNum` ASC),
  UNIQUE INDEX `Id_UNIQUE` (`Id` ASC),
  UNIQUE INDEX `idUSER_UNIQUE` (`idUSER` ASC),
  PRIMARY KEY (`idUSER`),
  CONSTRAINT `fk_USER_has_USERTYPE`
    FOREIGN KEY (`FK_UserTypeName`)
    REFERENCES `team9`.`USERTYPE` (`UserTypeName`)
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `team9`.`TASK`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `team9`.`TASK` (
  `TaskName` varchar(45) NOT NULL,
  `Description` longtext NOT NULL,
  `MinPeriod` int(11) NOT NULL DEFAULT 0,
  `Status` varchar(45) NOT NULL DEFAULT 'ongoing',
  `TaskDataTableName` varchar(100) NOT NULL,
  `TaskDataTableSchemaInfo` text DEFAULT NULL,
  `FK_idManager` int(11) NOT NULL,
  `MaxDuplicatedRowRatio` float NOT NULL,
  `MaxNullRatioPerColumn` float NOT NULL,
  `PassCriteria` text NOT NULL,
  INDEX `FK_idManager_idx` (`FK_idManager` ASC),
  PRIMARY KEY (`TaskName`),
  CONSTRAINT `fk_TASK_has_USER`
    FOREIGN KEY (`FK_idManager`)
    REFERENCES `team9`.`USER` (`idUSER`)
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `team9`.`PARTICIPATION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `team9`.`PARTICIPATION` (
  `FK_TaskName` varchar(45) NOT NULL,
  `FK_idUSER` int(11) NOT NULL,
  `Status` varchar(45) DEFAULT NULL,
  `Comment` text DEFAULT NULL,
  PRIMARY KEY (`FK_TaskName`, `FK_idUSER`),
  INDEX `FK_idUSER_idx` (`FK_idUSER` ASC),
  INDEX `FK_idTaskName_idx` (`FK_TaskName` ASC),
  CONSTRAINT `fk_PARTICIPATION_has_TASK`
    FOREIGN KEY (`FK_TaskName`)
    REFERENCES `team9`.`TASK` (`TaskName`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_PARTICIPATION_has_USER`
    FOREIGN KEY (`FK_idUSER`)
    REFERENCES `team9`.`USER` (`idUSER`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `team9`.`ORIGIN_DATA_TYPE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `team9`.`ORIGIN_DATA_TYPE` (
  `idORIGIN_DATA_TYPE` int(11) NOT NULL AUTO_INCREMENT,
  `SchemaInfo` varchar(1000) DEFAULT NULL,
  `MappingInfo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `DataTypeName` varchar(45) DEFAULT NULL,
  `TaskName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idORIGIN_DATA_TYPE`),
  INDEX `fk_ORIGIN_DATA_TYPE_TASK1_idx` (`TaskName` ASC),
  CONSTRAINT `fk_ORIGIN_DATA_TYPE_TASK1`
    FOREIGN KEY (`TaskName`)
    REFERENCES `team9`.`TASK` (`TaskName`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `team9`.`ORIGIN_DSF`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `team9`.`ORIGIN_DSF` (
  `idORIGIN_DSF` int(11) NOT NULL AUTO_INCREMENT,
  `OriginFile` longtext NOT NULL,
  `SubmitNum` int(11) NOT NULL DEFAULT 0,
  `DateTime` datetime NOT NULL,
  `Period` varchar(45) NOT NULL,
  `FK_TaskName` varchar(45) DEFAULT NULL,
  `FK_idUSER` int(11) DEFAULT NULL,
  `FK_idORIGIN_DATA_TYPE` int(11) DEFAULT NULL,
  `Round` int(11) NOT NULL,
  PRIMARY KEY (`idORIGIN_DSF`),
  UNIQUE INDEX `idORIGIN_DSF_UNIQUE` (`idORIGIN_DSF` ASC),
  INDEX `fk_ORIGIN_DSF_PARTICIPATION1_idx` (`FK_TaskName` ASC, `FK_idUSER` ASC),
  INDEX `fk_ORIGIN_DSF_ORIGIN_DATA_TYPE1_idx` (`FK_idORIGIN_DATA_TYPE` ASC),
  CONSTRAINT `fk_ORIGIN_DSF_has_PARTICIPATION`
    FOREIGN KEY (`FK_TaskName` , `FK_idUSER`)
    REFERENCES `team9`.`PARTICIPATION` (`FK_TaskName` , `FK_idUSER`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fk_ORIGIN_DSF_ORIGIN_DATA_TYPE1`
    FOREIGN KEY (`FK_idORIGIN_DATA_TYPE`)
    REFERENCES `team9`.`ORIGIN_DATA_TYPE` (`idORIGIN_DATA_TYPE`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `team9`.`PARSING_DSF`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `team9`.`PARSING_DSF` (
  `idPARSING_DSF` int(11) NOT NULL AUTO_INCREMENT,
  `TaskName` varchar(45) NOT NULL,
  `ParsingFile` longtext NOT NULL,
  `OriginDataTypeID` int(11) DEFAULT NULL,
  `SubmitterID` int(11) DEFAULT NULL,
  `SubmitNum` int(11) NOT NULL DEFAULT 0,
  `Period` varchar(45) DEFAULT NULL,
  `SystemScore` float DEFAULT NULL,
  `AverageScore` float DEFAULT NULL,
  `TotalScore` float DEFAULT NULL,
  `Pass` varchar(45) DEFAULT NULL,
  `TotalStatus` varchar(45) DEFAULT NULL,
  `FK_idORIGIN_DSF` int(11) DEFAULT NULL,
  `Round` int(11) NOT NULL,
  PRIMARY KEY (`idPARSING_DSF`),
  UNIQUE INDEX `idPARSING_DSF_UNIQUE` (`idPARSING_DSF` ASC),
  INDEX `fk_PARSING_DSF_ORIGIN_DSF1_idx` (`FK_idORIGIN_DSF` ASC),
  CONSTRAINT `fk_PARSING_DSF_has_ORIGIN_DSF`
    FOREIGN KEY (`FK_idORIGIN_DSF`)
    REFERENCES `team9`.`ORIGIN_DSF` (`idORIGIN_DSF`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `team9`.`EVALUATION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `team9`.`EVALUATION` (
  `idEVALUATION` int(11) NOT NULL AUTO_INCREMENT,
  `FK_idPARSING_DSF` int(11) NOT NULL,
  `FK_idEstimator` int(11) DEFAULT NULL,
  `Score` int(11) DEFAULT NULL,
  `Pass` varchar(45) DEFAULT NULL,
  `StartTime` datetime NOT NULL,
  `EndTime` datetime DEFAULT NULL,
  `Deadline` datetime NOT NULL,
  `Status` varchar(45) NOT NULL DEFAULT 'ongoing',
  PRIMARY KEY (`idEVALUATION`),
  INDEX `fk_PARSING_DSF_has_USER_USER1_idx` (`FK_idEstimator` ASC),
  INDEX `fk_PARSING_DSF_has_USER_PARSING_DSF1_idx` (`FK_idPARSING_DSF` ASC),
  CONSTRAINT `fk_EVALUATION_has_PARSING_DSF`
    FOREIGN KEY (`FK_idPARSING_DSF`)
    REFERENCES `team9`.`PARSING_DSF` (`idPARSING_DSF`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_EVALUATION_has_USER`
    FOREIGN KEY (`FK_idEstimator`)
    REFERENCES `team9`.`USER` (`idUSER`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
