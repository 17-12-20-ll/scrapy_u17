create database youyaoqi default character set='utf8';

use youyaoqi;
create table u(
  id int primary key auto_increment,
  comic_id varchar(32),
  name varchar(128),
  cover varchar(1024),
  category varchar(512)
);