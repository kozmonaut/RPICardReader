RPICardReader
=============
Card Reader will provide interface in which it will send message when there is an action from users side. All these actions will be stored in database, and later can be used for displaying data in some web application.

#### Installation steps:
#####1. Connect RPI with your RFID (here is used MIFARE MF522-AN)
Look at the pins positions and do the wiring. Disconnect RPi before you start to connect the cables.

#####2. Enable SPI comunication
Enable SPI device by editing file **/etc/modprobe.d/raspi-blacklist.conf** and comment the line **blacklist spi-bcm2708**.
```
# blacklist spi and i2c by default (many users don't need them)
# blacklist spi-bcm2708
blacklist i2c-bcm2708
```
Before installing driver for enabling SPI install python development package.

``` $ sudo apt-get install python-dev ```

Download SPI-Py driver.

``` $ git clone https://github.com/lthiery/SPI-Py	```

Position into downloaded folder and start the setup.

``` $ sudo python setup.py install ```

##### 3. Download MFRC522 driver

A small class to interface with the MFRC522 on the Raspberry Pi.

``` $ git clone https://github.com/mxgxw/MFRC522-python ```

Copy MFRC522.py file into working directory. It will be used by importing MFRC522 at the top of **main.py** python script.

##### 4. Install GPIO for Python

Download package from:	https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.5.6.tar.gz

Extract the package and install.
``` 
$ tar zxf RPi.GPIO-0.5.6.tar.gz
$ cd RPi.GPIO-0.5.6
$ sudo python setup.py install
```
##### 5. Configure database for storing actions

Because RPi has low performance for running e.g. phpmyadmin, it's better solution to manage database under command line.

Install MySQL packages.

``` $ sudo apt-get install mysql-server python-mysqldb ``` 

Login to MySQL and type username password.

``` $ mysql -u root -p  ```

Create database.
``` 
CREATE DATABASE rpicard;
USE rpicard;
``` 
Create database user and grant permissions.

``` 
CREATE USER 'pi'@'localhost' IDENTIFIED BY '<password>'
GRANT ALL PRIVILEGES ON rpicard.* TO 'pi'@'localhost';
``` 

Import database structure.

``` 
CREATE TABLE `cards` (
 `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
 `userId` VARCHAR(50) DEFAULT NULL,
 `tagId` BIGINT(18) UNSIGNED NOT NULL,
 `permission` INT(10) NOT NULL,
 `added` VARCHAR(50) NOT NULL,
 PRIMARY KEY (`id`),
 KEY `ix_cardId` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
 
CREATE TABLE `readings` (
`id` BIGINT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
`tagId` BIGINT(18) UNSIGNED NOT NULL,
`time` VARCHAR(50) DEFAULT NULL,
`action` INT(2) UNSIGNED NOT NULL,
PRIMARY KEY (`id`),
KEY `ix_id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
``` 

Save this structure to a mysql.sql file and import it to a database.

``` 
mysql -u pi -p rpicard < mysql.sql
``` 

##### 6. Run the app

``` $ python main.py ```


##### 7. Logs example

``` 
11/09/2014 06:53:40 AM Arrival for: 31191254130220
11/09/2014 06:54:06 AM Going home: 31191254130220
11/09/2014 06:54:23 AM Created new card user: Pero Peric
11/09/2014 07:16:27 AM Going home: 31191254130220
11/09/2014 07:17:33 AM 31191254130220:Arrive
11/09/2014 07:17:36 AM 31191254130220:Leaving
12/09/2014 02:40:06 AM Created new card user: admin, Permission: 1
``` 


