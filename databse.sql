SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- INT and int(8) has the same range of values (4-byte signed integer)
-- the number in paranthesis only indicates the display width which is a hint for applications.

--
-- Table structure for table `Lecture`
--
CREATE TABLE `Lecture` (
    `lecture_id`         SMALLINT(4) NOT NULL, -- Should not be more than 9999 lecturers
    `room_booking`       int(8)      NOT NULL,
    `course_code`        varchar(50) NOT NULL,
    `activity`           varchar(50),
    PRIMARY KEY (`lecture_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `Lecture` (lecture_id, room_booking, course_code, activity) VALUES
(1, 1, 'IDATG2204', 'Introduction to cloud technologies'),
(2, 2, 'PROG2005', 'Database Managment introduction'),
(3, 3, 'PROG2006', 'Introductory lecture');

--
-- Table structure for table `Room_booking`
--
CREATE TABLE `Room_booking` (
    `booking_id`                int(8) NOT NULL,    
    `user_ID`             MEDIUMINT(5) NOT NULL, 
    `room_num`                      SMALLINT(4),    
    `booking_description`          varchar(500),   
    `start_time`                  TIME NOT NULL,
    `end_time`                    TIME NOT NULL,
    `booking_date`                DATE NOT NULL,
    `reservation_type`              varchar(50),
    PRIMARY KEY (`booking_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `Room_booking` (booking_id, user_ID, room_num, booking_description, start_time, end_time, booking_date, reservation_type) VALUES
(1, 3, 103, 'Introduction lecture', '14:00:00', '16:00:00', '2023-04-04', 'Lecture'),
(2, 2, 101, 'Introduction lecture', '10:00:00', '12:00:00', '2023-04-03', 'Lecture'),
(3, 9, 103, 'Conference for computer students', '9:00:00', '17:00:00', '2023-04-08', 'Conference'),
(4, 2, 102, 'Databases Lab', '10:00:00', '12:00:00', '2023-04-18', 'Lab'),
(5, 4, 106, 'Seminar about digital security', '13:30:00', '15:30:00', '2023-04-21', 'Seminar'),
(6, 3, 103, 'Meeting', '16:00:01', '18:00:00', '2023-04-04', 'Meeting');


--
-- Table structure for table `Room`
--
CREATE TABLE `Room` (
    `room_num`     SMALLINT(4)  NOT NULL, 
    `room_type`     varchar(50) NOT NULL,  
    `room_capacity` TINYINT(2)  NOT NULL,
    `floor_level`   TINYINT(1)  NOT NULL,
    `building`     varchar(50)  NOT NULL,
    PRIMARY KEY (`room_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `Room` (room_num, room_type, room_capacity, floor_level, building) VALUES
(101, 'Lecture Hall', 100, 2, 'S-206'),
(102, 'Computer Lab', 30, 2, 'A-254'),
(103, 'Conference Room', 20, 2, 'A-250'),
(104, 'Group Room', 10, 1, 'A-117'),
(105, 'Group Room', 10, 1, 'A-120'),
(106, 'Seminar room', 40, 2, 'S-215');


--
-- Table structure for table `User`
--
CREATE TABLE `User` (
    `user_ID`     MEDIUMINT(5) NOT NULL, 
    `first_name`   varchar(50) NOT NULL,
    `last_name`    varchar(50) NOT NULL,
    `dob`                 DATE NOT NULL,
    `age`           TINYINT(3) NOT NULL,
    `gender`       varchar(50) NOT NULL,
    `email`       varchar(150) NOT NULL,
    `phone`             int(8) NOT NULL,
    `user_type`     ENUM('admin', 'lecturer', 'student', 'general_public') NOT NULL,
    `access_level`  TINYINT(1) NOT NULL,
    PRIMARY KEY (`user_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `User` (user_ID, first_name, last_name, dob, age, gender, email, phone, user_type, access_level) VALUES
(1, 'David', 'Lee', '1985-07-21', 38, 'Male','david.lee@example.com', 12345678, 'lecturer', 2),
(2, 'James', 'Chen', '1976-09-05', 47, 'Male','james.chen@example.com', 23456789, 'lecturer', 2),
(3, 'Jennifer', 'Allen', '1990-01-15', 33, 'Female', 'jennifer.kim@example.com', 34567890, 'lecturer', 2),
(4, 'Ola', 'Nordmann', '1988-03-15', 33, 'Male', 'jane.doe@example.com', 23456787, 'student', 1),
(5, 'Bob', 'Smith', '1995-05-10', 28, 'Male', 'bob.smith@example.com', 34567898, 'student', 1),
(6, 'Alice', 'Johnson', '1992-07-20', 31, 'Female', 'alice.johnson@example.com', 45678901, 'student', 1),
(7, 'Sarah', 'Lee', '1998-11-05', 25, 'Female', 'sarah.lee@example.com', 56789012, 'general_public', 0),
(8, 'David', 'Kim', '1985-09-23', 38, 'Male', 'david.kim@example.com', 67890123, 'general_public', 0),
(9, 'Linda', 'Davis', '1979-12-30', 44, 'Female', 'linda.davis@example.com', 78901234, 'general_public', 0),
(10, 'Tom', 'Wilson', '2000-02-14', 23, 'Male', 'tom.wilson@example.com', 89012345, 'admin', 3),
(11, 'Karen', 'Brown', '1991-04-18', 32, 'Female', 'karen.brown@example.com', 90123456, 'admin', 3),
(12, 'Michael', 'Garcia', '1993-06-25', 28, 'Male', 'michael.garcia@example.com', 12348901, 'admin', 3);


--
-- Table structure for table `Teacher`
--
CREATE TABLE `Teacher` (
    `teacher_id`  MEDIUMINT(5) NOT NULL, 
    `office_room` SMALLINT(4) NOT NULL,
    `institute`   varchar(50) NOT NULL,
    `title`       varchar(50) NOT NULL,
    PRIMARY KEY (`teacher_id`),
    UNIQUE KEY (`institute`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `Teacher` (teacher_id, office_room, institute, title) VALUES
(1, 101, 'Computer Science', 'Professor'),
(2, 102, 'Electrical Engineering', 'Associate Professor'),
(3, 103, 'Business Administration', 'Assistant Professor');


-- 
-- Table structure for table `Institute` 
--
CREATE TABLE `Institute` (
    `institute_name`   varchar(50) NOT NULL,
    `faculty`          varchar(50) NOT NULL,
    PRIMARY KEY (`institute_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `Institute` (institute_name, faculty) VALUES
('Computer Science', 'Engineering'),
('Electrical Engineering', 'Engineering'),
('Business Administration', 'Business');

--
-- Table structure for table `Course`
--
CREATE TABLE `Course` (
    `course_code`  varchar(50) NOT NULL,
    `lecturer`     MEDIUMINT(5)        ,
    `course_name`  varchar(50) NOT NULL,   
    PRIMARY KEY (`course_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `Course`(course_code, lecturer, course_name) VALUES
('IDATG2204', 1, 'Databases and datamodelling'),
('PROG2005', 2, 'Cloud technologies'),
('PROG2006', 3, 'Advanced programming'),
('BMA1010', 1, 'Mathematics for information technology'),
('IMT3601', 1, 'Game programming'),
('PROG2007', 2, 'Mobile programming'),
('IDATG2102', 1, 'Algorithms and datastructures'),
('imt2291', NULL, 'www-technologies');

--
-- Table structure for table `List_students`
--
CREATE TABLE `List_students` (
    `course_code`  varchar(50) NOT NULL,
    `student_id`  MEDIUMINT(5) NOT NULL,
    PRIMARY KEY (`course_code`, `student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `List_students`(course_code, student_id) VALUES
('PROG2006',  4),
('PROG2006',  5),
('PROG2006',  6),
('PROG2005',  5),
('PROG2005',  4),
('PROG2005',  6),
('IDATG2204', 4),
('IDATG2204', 5),
('IDATG2204', 6),
('PROG2007', 4),
('PROG2007', 5),
('PROG2007', 6),
('IMT3601', 6),
('BMA1010', 4),
('IDATG2102', 5);


ALTER TABLE `Lecture`
    ADD CONSTRAINT `Lecture_ibfk_1` FOREIGN KEY (`room_booking`) REFERENCES `Room_booking`(`booking_id`) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT `Lecture_ibfk_2` FOREIGN KEY (`course_code`) REFERENCES `Course`(`course_code`) 
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Room_booking`
    ADD CONSTRAINT Room_booking_ibfk_1 FOREIGN KEY (`user_ID`) REFERENCES `User`(`user_ID`),
    ADD CONSTRAINT Room_booking_ibfk_2 FOREIGN KEY (`room_num`) REFERENCES `Room`(`room_num`);

ALTER TABLE `Teacher`
    ADD CONSTRAINT Teacher_ibfk_1 FOREIGN KEY (`office_room`) REFERENCES `Room`(`room_num`) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT Teacher_ibfk_2 FOREIGN KEY (`teacher_id`) REFERENCES `User`(`user_ID`) 
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Institute`
    ADD CONSTRAINT Institute_ibfk_1 FOREIGN KEY (`institute_name`) REFERENCES `Teacher`(`institute`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Course`
    ADD CONSTRAINT Course_ibfk_1 FOREIGN KEY (`lecturer`) REFERENCES `Teacher`(`teacher_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `List_students`
    ADD CONSTRAINT List_students_list_ibfk_1 FOREIGN KEY (`course_code`) REFERENCES `Course`(`course_code`) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT List_students_list_ibfk_2 FOREIGN KEY (`student_id`) REFERENCES `User`(`user_ID`) 
    ON DELETE CASCADE ON UPDATE CASCADE;

COMMIT;