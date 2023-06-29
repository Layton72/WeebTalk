-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema weebtalk
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `weebtalk` ;

-- -----------------------------------------------------
-- Schema weebtalk
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `weebtalk` DEFAULT CHARACTER SET utf8 ;
USE `weebtalk` ;

-- -----------------------------------------------------
-- Table `weebtalk`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `weebtalk`.`users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(45) NULL,
    `birthday` DATE NULL,
    `email` VARCHAR(255) NULL,
    `password` VARCHAR(255) NULL,
    `created_at` DATETIME NULL DEFAULT now(),
    `updated_at` DATETIME NULL DEFAULT now(),
    PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `weebtalk`.`animes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `weebtalk`.`animes` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `mal_id` INT NULL,
    `title` VARCHAR(255) NULL,
    `thumbnail` VARCHAR(255) NULL,
    `synopsis` VARCHAR(2000) NULL,
    `created_at` DATETIME NULL DEFAULT now(),
    `updated_at` DATETIME NULL DEFAULT now(),
    PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `weebtalk`.`reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `weebtalk`.`reviews` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `score` INT NULL,
    `review` VARCHAR(1000) NULL,
    `created_at` DATETIME NULL DEFAULT now(),
    `updated_at` DATETIME NULL DEFAULT now(),
    `user_id` INT NOT NULL,
    `anime_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    INDEX `fk_reviews_users_idx` (`user_id` ASC) VISIBLE,
    INDEX `fk_reviews_animes1_idx` (`anime_id` ASC) VISIBLE,
    CONSTRAINT `fk_reviews_users`
        FOREIGN KEY (`user_id`)
        REFERENCES `weebtalk`.`users` (`id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `fk_reviews_animes1`
        FOREIGN KEY (`anime_id`)
        REFERENCES `weebtalk`.`animes` (`id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `weebtalk`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `weebtalk`.`likes` (
    `user_id` INT NOT NULL,
    `review_id` INT NOT NULL,
    `like` INT NULL,
    INDEX `fk_likes_users1_idx` (`user_id` ASC) VISIBLE,
    INDEX `fk_likes_reviews1_idx` (`review_id` ASC) VISIBLE,
    CONSTRAINT `fk_likes_users1`
        FOREIGN KEY (`user_id`)
        REFERENCES `weebtalk`.`users` (`id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `fk_likes_reviews1`
        FOREIGN KEY (`review_id`)
        REFERENCES `weebtalk`.`reviews` (`id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
