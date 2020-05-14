CREATE DATABASE taxiData;
use taxiData;

CREATE TABLE IF NOT EXISTS tblTaxiImport (
    `id` int AUTO_INCREMENT,
    `distance_miles` NUMERIC(3, 1),
    `fare` NUMERIC(5, 2),
    PRIMARY KEY (`id`)
);
INSERT INTO tblTaxiImport (distance_miles, fare) VALUES
    ( 4.5,   18.00),
    (26.7,   73.75),
    ( 6.7,   23.00),
    (16.4,   56.00),
    (32.7,   83.25),
    ( 5.7,   17.50),
    (77.0,  190.50),
    ( 8.3,   19.65);
