from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from decimal import Decimal
import json
import pymysql.cursors
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'project',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
app = Flask(__name__)
connection = pymysql.connect(**config)
#mysql = MySQL(app)


app.json_provider_class = CustomJSONEncoder
'''
1. Show a list of all courses that have not been assigned a lecturer, along with the room number
and building name where each course is held.
2. Show a list of all courses taught by a specific teacher in a given semester.
3. Show a list of all courses taught in a specific room on a given date and a specific time range.
4. Show a list of all courses taught in a specific room on a given date and at a specific time.
5. Show a list of all courses, along with the name and email of the teacher teaching each course.
6. Show a list of all courses taught by a specific teacher, along with the institute and faculty
where each course belongs.
7. Show a list of all courses taught by a specific lecturer, along with the room number and
building name where each course is held.
8. Show a list of all rooms available for a given date and time range.
9. Show a list of all reservations made by a specific user, along with the room number and
building name for each reservation.
10. Show a list of all rooms and the reservations made for each room, including the name of the
person who made each reservation
11. Show a list of all rooms, along with the number and type of reservations made for each room.
12. Show a list of all teachers and the number of courses they are teaching in each semester, sorted by the number of courses.
13. Show a list of all teachers and the courses, they teach, including the room number and building name where each course is held.
14. Show a list of all teachers and the total number of hours they teach each week.
15. Show a list of all courses that are taught on Mondays, along with the name and email of the teachers teaching each course.
16. Show a list of all teachers and the average number of students in the courses they teach, sorted by the average number of students.
'''

# TODO: Implement all the sql queries for the different endpoints
@app.route('/')
def root():
    return render_template("endpoints.html")

# 1. Show a list of all courses that have not been assigned a lecturer, along with the room number and building name where each course is held.
# room is not conected to a course but rather a room is connected to a lecture and multiple lectures are to a course
# example: /Courses/noLecturer
@app.route('/Courses/noLecturer', methods=['GET'])
def listOfAllCoursesWithoutLecturer():       
    with connection.cursor() as cursor:
        if request.method == 'GET':
            sqlData = cursor.execute("SELECT * FROM `Course` WHERE lecturer IS NULL;")    # Currently lecturer, lecturer_id might be the new one
            if sqlData >0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else: return jsonify('Nothing Found'), 404
        else: return jsonify('405 Method Not Allowed'), 405

# 2. Show a list of all courses taught by a specific teacher in a given semester.
# example: /courses/specificTeacher/David
@app.route('/courses/specificTeacher/<lecturer>', methods=['GET'])
def coursesSpecificTeacher(lecturer): 
    with connection.cursor() as cursor:
        if request.method == 'GET':
            sqlData = cursor.execute(f'''
            SELECT course.course_code, course.course_name, t.title, t.institute, CONCAT(u.first_name, " ", u.last_name) AS full_name
            FROM `Course` 
            INNER JOIN teacher AS t
            ON t.teacher_id = course.lecturer
            INNER JOIN user AS u
            ON u.user_id = t.teacher_id
            WHERE CONCAT(u.first_name, " ", u.last_name) LIKE '%{lecturer}%'
            ''')
            if sqlData >0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else: return jsonify('Nothing Found'), 404
        else: return jsonify('405 Method Not Allowed'), 405

# 3. Show a list of all courses taught in a specific room on a given date and a specific time range.
# example /courses/specificRoomGivenDataTime/103/2023-04-04/13:13:13/20:20:20
@app.route('/courses/specificRoomGivenDataTime/<roomNum>/<date>/<startTime>/<endTime>', methods=['GET']) 
def getRoom(roomNum, date, startTime, endTime):
    with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
                SELECT l.course_code, l.activity, r.room_num, r.booking_description, r.reservation_type
                FROM Lecture AS l
                INNER JOIN room_booking AS r
                ON l.room_booking = r.booking_id
                WHERE r.room_num = '{roomNum}'
                AND r.booking_date = '{date}'
                AND r.start_time >= '{startTime}'
                AND r.end_time <= '{endTime}'
                AND r.reservation_type = 'Lecture';
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sql_query = cursor.fetchall()
                return jsonify(sql_query), 200
            else: return jsonify('Nothing Found'), 404
        else: return jsonify('405 Method Not Allowed'), 405

# 4. Show a list of all courses taught in a specific room on a given date and at a specific time.  
# example: /courses/courseRoomDateTime/103/2023-04-04/15:15:15
@app.route('/courses/courseRoomDateTime/<roomNum>/<date>/<time>', methods=['GET'])  
def courseRoomDateTime(roomNum, date, time):
    with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
                SELECT Course.course_code, Course.course_name, CONCAT(u.first_name, " ", u.last_name) AS lecturer_name
                FROM Course
                INNER JOIN Lecture
                ON Course.course_code = Lecture.course_code
                INNER JOIN Room_booking
                ON Lecture.room_booking = Room_booking.booking_id
                INNER JOIN user AS u
                ON u.user_ID = Course.lecturer
                WHERE Room_booking.room_num = '{roomNum}'
                AND Room_booking.booking_date = '{date}'
                AND '{time}' BETWEEN Room_booking.start_time AND Room_booking.end_time
                AND Room_booking.reservation_type = 'Lecture';
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                results = cursor.fetchall()
                return jsonify(results), 200
            else:
                return jsonify('Nothing Found'), 404
        else:
            return jsonify('405 Method Not Allowed'), 405

# 5. Show a list of all courses, along with the name and email of the teacher teaching each course.   
# example: /courses/NameEmailTeacher
@app.route('/courses/NameEmailTeacher', methods=['GET'])
def coursesNameEmailTeacher():
    with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
                SELECT Course.course_code, Course.course_name, CONCAT(User.first_name, " ", User.last_name) as teacherName, User.email
                FROM Course
                INNER JOIN User
                ON User.user_id = Course.lecturer
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else: return jsonify('Nothing Found'), 404
        else: return jsonify('405 Method Not Allowed'), 405

# 6. Show a list of all courses taught by a specific teacher, along with the institute and faculty where each course belongs.
# example: /courses/teacherInstituteFaculty/LEE
@app.route('/courses/teacherInstituteFaculty/<lecturer>', methods=['GET'])
def coursesTeacherInstituteFaculty(lecturer):
    with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
                SELECT Course.course_code, Course.course_name, i.faculty, Teacher.institute, CONCAT(u.first_name, " ", u.last_name) AS lecturer_name
                FROM Course
                INNER JOIN Teacher
                ON Teacher.teacher_id = Course.lecturer
                INNER JOIN institute AS i
                ON Teacher.institute = i.institute_name
                INNER JOIN user AS u
                ON Teacher.teacher_id = u.user_ID
                WHERE CONCAT(u.first_name, " ", u.last_name) LIKE '%{lecturer}%'
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else: return jsonify('Nothing Found'), 404
        else: return jsonify('405 Method Not Allowed'), 405

# 7. Show a list of all courses taught by a specific lecturer, along with the room number and building name where each course is held.
# Due to how our database is a course is not tied to a room, but rather courses can book a room or multiple rooms depending on what is accesible
# we show repeat some courses since they can have bookings for multiple rooms
# example: '/courses/coursesByTeacher/James'
@app.route('/courses/coursesByTeacher/<lecturer>', methods=['GET'])
def coursesByTeacher(lecturer):
    with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
                SELECT DISTINCT c.course_code, c.course_name, CONCAT(u.first_name, " ", u.last_name) AS teacher, r.room_num, r.building
                FROM course AS c
                INNER JOIN user AS u ON u.user_id = c.lecturer    
                INNER JOIN room_booking	AS rb ON u.user_ID = rb.user_ID
                INNER JOIN room AS r ON r.room_num = rb.room_num
                WHERE CONCAT(u.first_name, " ", u.last_name) LIKE '%{lecturer}%';
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else: return jsonify('Nothing Found'), 404
        else: return jsonify('405 Method Not Allowed'), 405


# 8. Show a list of all rooms available for a given date and time range.
# example: /availabelRooms/2023-04-04/14:00:00/16:00:00
@app.route('/availabelRooms/<date>/<startTime>/<endTime>', methods=['GET'])
def availabelRooms(date, startTime, endTime):
    with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
                SELECT Room.*
                FROM Room
                LEFT JOIN Room_booking
                ON Room_booking.room_num = Room.room_num AND Room_booking.booking_date = '{date}'
                WHERE Room.room_num NOT IN (
                    SELECT Room_booking.room_num
                    FROM Room_booking
                    WHERE Room_booking.booking_date = '{date}'
                    AND (
                        (Room_booking.start_time <= '{startTime}' AND Room_booking.end_time > '{startTime}') OR
                        (Room_booking.start_time >= '{startTime}' AND Room_booking.start_time < '{endTime}')
                    )
                );
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else:
                return jsonify('Nothing Found'), 404
        else:
            return jsonify('405 Method Not Allowed'), 405

'''
Sice room_booking.* includes a time value we have to change the format in the sql code so instead of just writing room_booking.*, we have to type:

room_booking.booking_id, room_booking.user_ID, room_booking.room_num, room_booking.booking_description,
                TIME_FORMAT(room_booking.start_time, '%H:%i:%s') as start_time_str, 
                TIME_FORMAT(room_booking.end_time, '%H:%i:%s') as end_time_str,
                room_booking.booking_date, room_booking.reservation_type, room.building
'''

# 9. Show a list of all reservations made by a specific user, along with the room number and building name for each reservation.
# example /reservationsByUser/Jennifer
@app.route('/reservationsByUser/<user>', methods=['GET'])
def reservationsByUser(user):
     with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
                SELECT CONCAT (user.first_name, " ", user.last_name) AS name, room_booking.booking_id, room_booking.user_ID, room_booking.room_num, room_booking.booking_description,
                TIME_FORMAT(room_booking.start_time, '%H:%i:%s') as start_time_str, 
                TIME_FORMAT(room_booking.end_time, '%H:%i:%s') as end_time_str,
                room_booking.booking_date, room_booking.reservation_type, room.building
                FROM user
                INNER JOIN room_booking
                ON user.user_id = room_booking.user_id
                INNER JOIN room
                ON room_booking.room_num = room.room_num
                WHERE CONCAT(user.first_name, " ", user.last_name) LIKE '%{user}%'
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else:
                return jsonify('Nothing Found'), 404
        else:
            return jsonify('405 Method Not Allowed'), 405

# 10. Show a list of all rooms and the reservations made for each room, including the name of the person who made each reservation
# example: /roomsReservationName
@app.route('/roomsReservationName', methods=['GET'])
def roomsReservationName():
     with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
                SELECT CONCAT(user.first_name, " ", user.last_name) AS booker_name, room.building, room_booking.room_num, room_booking.booking_id, room_booking.booking_description,
                TIME_FORMAT(room_booking.start_time, '%H:%i:%s') as start_time_str, 
                TIME_FORMAT(room_booking.end_time, '%H:%i:%s') as end_time_str,
                room_booking.booking_date, room_booking.reservation_type
                FROM user
                INNER JOIN room_booking
                ON user.user_id = room_booking.user_id
                INNER JOIN room
                ON room_booking.room_num = room.room_num;
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else:
                return jsonify('Nothing Found'), 404
        else:
            return jsonify('405 Method Not Allowed'), 405

# 11. Show a list of all rooms, along with the number and type of reservations made for each room.
# example: /roomsNumberReservationType
@app.route('/roomsNumberReservationType', methods=['GET'])
def roomsNumberReservationType():
     with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
            SELECT room_num, GROUP_CONCAT(DISTINCT reservation_type SEPARATOR ', ') AS reservation_types, COUNT(*) AS num_reservations
            FROM room_booking
            GROUP BY room_num;
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else:
                return jsonify('Nothing Found'), 404
        else:
            return jsonify('405 Method Not Allowed'), 405
        
# 12. Show a list of all teachers and the number of courses they are teaching in each semester, sorted by the number of courses.
# ADD NAME OF TEACHER
@app.route('/teachers/semester/courses', methods=['GET'])
def teachersSemesterCourses():
    with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
                SELECT CONCAT(user.first_name, " ", user.last_name) AS teacher_name, COUNT(*) as num_courses
                FROM teacher
                INNER JOIN course ON teacher.teacher_id = course.lecturer
		        INNER JOIN user ON teacher.teacher_id = user.user_id
                GROUP BY teacher.teacher_id
                ORDER BY num_courses DESC;
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else: return jsonify('Nothing Found'), 404
        else: return jsonify('405 Method Not Allowed'), 405

# 13. Show a list of all teachers and the courses, they teach, including the room number and building name where each course is held.
# TEACHER NAME INSTEAD OF ID
@app.route('/teachers/courses/roomNumberBuilding', methods=['GET'])
def teachersCoursesRoomNumberBuilding():
    with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
                SELECT teacher.institute, teacher.title, CONCAT(user.first_name, " ", user.last_name) AS teacher_name, course.course_name, room.room_num, room.building
                FROM teacher
                INNER JOIN course ON teacher.teacher_id = course.lecturer
                INNER JOIN lecture ON course.course_code = lecture.course_code
                INNER JOIN room_booking ON lecture.room_booking = room_booking.booking_id
                INNER JOIN room ON room_booking.room_num = room.room_num
                INNER JOIN user ON teacher.teacher_id = user.user_id;
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else: return jsonify('Nothing Found'), 404
        else: return jsonify('405 Method Not Allowed'), 405

# 14. Show a list of all teachers and the total number of hours they teach each week.
# TEACHER NAME INSTEAD OF ID
@app.route('/teachers/hours', methods=['GET'])
def teacherHours():
     with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
            SELECT teacher.institute, teacher.office_room, teacher.title, CONCAT(user.first_name, " ", user.last_name) AS full_name, weeks.week, TIME_FORMAT(weeks.numHours, '%H:%i:%s') AS hours
            FROM teacher
            INNER JOIN (
                SELECT room_booking.user_ID AS id, WEEK(room_booking.booking_date) AS week, 
                SEC_TO_TIME(SUM(TIME_TO_SEC(TIMEDIFF(room_booking.end_time, room_booking.start_time)))) AS numHours
            FROM room_booking
            GROUP BY id, week
            )AS weeks
            ON teacher.teacher_id = weeks.id
	        INNER JOIN user ON teacher.teacher_id = user.user_id 
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else:
                return jsonify('Nothing Found'), 404
        else:
            return jsonify('405 Method Not Allowed'), 405

# 15. Show a list of all courses that are taught on Mondays, along with the name and email of the teachers teaching each course.
# TEACHER NAME INSTEAD OF ID
@app.route('/courses/monday/nameEmailTeachers', methods=['GET'])
def coursesMondayNameEmailTeachers():
    with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
                SELECT course.course_name, course.course_code, user.first_name, user.last_name, user.email, room_booking.booking_date
                FROM course 
                JOIN lecture ON course.course_code = lecture.course_code 
                JOIN room_booking ON lecture.room_booking = room_booking.booking_id 
                JOIN teacher ON course.lecturer = teacher.teacher_id 
                JOIN user ON teacher.teacher_id = user.user_id 
                WHERE WEEKDAY(room_booking.booking_date) = 0;
            """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else: return jsonify('Nothing Found'), 404
        else: return jsonify('405 Method Not Allowed'), 405

#16. Show a list of all teachers and the average number of students in the courses they teach, sorted by the average number of students.
@app.route('/teachers/avgStudentsCourses', methods=['GET'])
def teachersAvgStudentCourses():
     with connection.cursor() as cursor:
        if request.method == 'GET':
            sql_query = f"""
            SELECT 
            teacher.*, 
            user.first_name, 
            user.last_name, 
            AVG(count_students.num_students) AS avg_num_students
            FROM user
            INNER JOIN teacher ON teacher.teacher_id = user.user_ID
            INNER JOIN course ON course.lecturer = teacher.teacher_id
            INNER JOIN (
            SELECT course_code, COUNT(DISTINCT student_id) AS num_students
            FROM list_students
            GROUP BY course_code
            ) AS count_students ON course.course_code = count_students.course_code
            GROUP BY teacher.teacher_id
            ORDER BY avg_num_students;
                        """
            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                sqlData = cursor.fetchall()
                return jsonify(sqlData), 200
            else:
                return jsonify('Nothing Found'), 404
        else:
            return jsonify('405 Method Not Allowed'), 405

if __name__ == '__main__':
    app.run(debug=True, port=3333)

