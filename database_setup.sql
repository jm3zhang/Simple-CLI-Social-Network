CREATE DATABASE  IF NOT EXISTS `ece356_proj`;
USE `ece356_proj`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `Users`
-- ----------------------------
DROP TABLE IF EXISTS `Users`;
CREATE TABLE `Users` (
  `UserID` varchar(255) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Birthday` date DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `Posts`
-- ----------------------------
DROP TABLE IF EXISTS `Posts`;
CREATE TABLE `Posts` (
  `PostID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Type` varchar(255) DEFAULT NULL,
  `Content` varchar(255) DEFAULT NULL,
  `CreatedBy` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`PostID`),
  FOREIGN KEY (`CreatedBy`) REFERENCES  Users(`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `UserGroups`
-- ----------------------------
DROP TABLE IF EXISTS `UserGroups`;
CREATE TABLE `UserGroups` (
  `GroupID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `CreatedBy` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`GroupID`),
  FOREIGN KEY (`CreatedBy`) REFERENCES  Users(`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `Topics`
-- ----------------------------
DROP TABLE IF EXISTS `Topics`;
CREATE TABLE `Topics` (
  `TopicID` varchar(255) NOT NULL,
  PRIMARY KEY (`TopicID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `UserFollowsUser`
-- ----------------------------
DROP TABLE IF EXISTS `UserFollowsUser`;
CREATE TABLE `UserFollowsUser` (
  `UserID` varchar(255) NOT NULL,
  `FollowUserID` varchar(255) NOT NULL,
  `LastReadPost` int DEFAULT NULL,
  PRIMARY KEY (`UserID`,`FollowUserID`),
  FOREIGN KEY (`UserID`) REFERENCES  Users(`UserID`),
  FOREIGN KEY (`FollowUserID`) REFERENCES  Users(`UserID`),
  FOREIGN KEY (`LastReadPost`) REFERENCES  Posts(`PostID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `UserFollowsTopic`
-- ----------------------------
DROP TABLE IF EXISTS `UserFollowsTopic`;
CREATE TABLE `UserFollowsTopic` (
  `UserID` varchar(255) NOT NULL,
  `FollowTopicID` varchar(255) NOT NULL,
  `LastReadPost` int DEFAULT NULL,
  PRIMARY KEY (`UserID`,`FollowTopicID`),
  FOREIGN KEY (`UserID`) REFERENCES  Users(`UserID`),
  FOREIGN KEY (`FollowTopicID`) REFERENCES  Topics(`TopicID`),
  FOREIGN KEY (`LastReadPost`) REFERENCES  Posts(`PostID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `UserJoinGroup`
-- ----------------------------
DROP TABLE IF EXISTS `UserJoinGroup`;
CREATE TABLE `UserJoinGroup` (
  `UserID` varchar(255) NOT NULL,
  `GroupID` int NOT NULL,
  PRIMARY KEY (`UserID`,`GroupID`),
  FOREIGN KEY (`UserID`) REFERENCES  Users(`UserID`),
  FOREIGN KEY (`GroupID`) REFERENCES  UserGroups(`GroupID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `PostRespPost`
-- ----------------------------
DROP TABLE IF EXISTS `PostRespPost`;
CREATE TABLE `PostRespPost` (
  `PostID` int NOT NULL,
  `ResponseID` int NOT NULL,
  PRIMARY KEY (`PostID`,`ResponseID`),
  FOREIGN KEY (`PostID`) REFERENCES  Posts(`PostID`),
  FOREIGN KEY (`ResponseID`) REFERENCES  Posts(`PostID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `PostUnderTopic`
-- ----------------------------
DROP TABLE IF EXISTS `PostUnderTopic`;
CREATE TABLE `PostUnderTopic` (
  `PostID` int NOT NULL,
  `TopicID` varchar(255) NOT NULL,
  PRIMARY KEY (`PostID`,`TopicID`),
  FOREIGN KEY (`PostID`) REFERENCES  Posts(`PostID`),
  FOREIGN KEY (`TopicID`) REFERENCES  Topics(`TopicID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




-- Sample Data Population --

-- Corresponding sample commands for python interface are given above the procedure as comments
  -- Indented comments are not related to the database population procedure, but are necessary if python interface commands are used for the population

BEGIN;
-- create_user tuser1 testuser1 1990-01-23
INSERT INTO `Users` VALUES ('tuser1','testuser1','1990-01-23');
-- create_user tuser2 testuser2 1990-04-05
INSERT INTO `Users` VALUES ('tuser2','testuser2','1990-04-05');
-- create_topic testtopic1
INSERT INTO Topics  VALUES("testtopic1");
-- create_topic testtopic2
INSERT INTO Topics  VALUES("testtopic2");
  -- login tuser1
-- create_group testgroup
INSERT INTO UserGroups (Name,CreatedBy) VALUES("testgroup","tuser1");
-- init_post testtitle testtopic1,testtopic2 testcontent
INSERT INTO Posts (Name,Type,Content,CreatedBy) VALUES("testtitle","initial","testcontent","tuser1");
INSERT INTO PostUnderTopic  VALUES("1","testtopic1");
INSERT INTO PostUnderTopic  VALUES("1","testtopic2");
-- follow_user tuser2
INSERT INTO UserFollowsUser  VALUES("tuser1","tuser2",NULL);
-- follow_topic testtopic1
INSERT INTO UserFollowsTopic  VALUES("tuser1","testtopic1",NULL);
-- reply_post 1 response testresponse
INSERT INTO Posts (Name,Type,Content,CreatedBy) VALUES("testtitle","response","testresponse","tuser1");
INSERT INTO PostRespPost  VALUES("1","2");
INSERT INTO PostUnderTopic  VALUES("2","testtopic1");
INSERT INTO PostUnderTopic  VALUES("2","testtopic2");
-- reply_post 1 thumb up
INSERT INTO Posts (Name,Type,Content,CreatedBy) VALUES("testtitle","thumb","up","tuser1");
INSERT INTO PostRespPost  VALUES("1","3");
INSERT INTO PostUnderTopic  VALUES("3","testtopic1");
INSERT INTO PostUnderTopic  VALUES("3","testtopic2");
-- join_group 1
INSERT INTO UserJoinGroup  VALUES("tuser1","1");
  -- login tuser2
-- join_group 1
INSERT INTO UserJoinGroup  VALUES("tuser2","1");
-- reply_post 1 response testresponse
INSERT INTO Posts (Name,Type,Content,CreatedBy) VALUES("testtitle","response","testresponse","tuser2");
INSERT INTO PostRespPost  VALUES("1","4");
INSERT INTO PostUnderTopic  VALUES("4","testtopic1");
INSERT INTO PostUnderTopic  VALUES("4","testtopic2");
  -- logout
COMMIT;












