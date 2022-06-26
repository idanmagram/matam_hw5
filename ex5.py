import json
import os



def names_of_registered_students(input_json_path, course_name):
    """
    This function returns a list of the names of the students who registered for
    the course with the name "course_name".

    :param input_json_path: Path of the students database json file.
    :param course_name: The name of the course.
    :return: List of the names of the students.
    """
    students_registered_to_course = []

    with open(input_json_path, 'r') as file:
        db = json.load(file)

    for id in db:
        if course_name in db[id]['registered_courses']:
            students_registered_to_course.append(db[id]['student_name'])

    return students_registered_to_course


def enrollment_numbers(input_json_path, output_file_path):
    """
    This function writes all the course names and the number of enrolled
    student in ascending order to the output file in the given path.

    :param input_json_path: Path of the students database json file.
    :param output_file_path: Path of the output text file.
    """

    with open(input_json_path, 'r') as file:
        db = json.load(file)

    courses_amount = {}

    for id in db:
        for course in db[id]['registered_courses']:
            if course in courses_amount.keys():
                courses_amount[course] += 1
            else:
                courses_amount[course] = 1

    course_list = list(courses_amount)
    course_list.sort()

    with open(output_file_path, 'w') as out_file:
        for course in course_list:
            line = "\"" + course + "\" " + str(courses_amount[course]) + "\n"
            out_file.write(line)


def courses_for_lecturers(json_directory_path, output_json_path):
    """
    This function writes the courses given by each lecturer in json format.

    :param json_directory_path: Path of the semsters_data files.
    :param output_json_path: Path of the output json file.
    """
    out_dict = {}

    for file_name in os.listdir(json_directory_path):
        file_path = os.path.join(json_directory_path, file_name)
        if file_name[-len('.json'):] == '.json':
            parse_file(file_path, out_dict)

    with open(output_json_path, 'w') as out_file:
        json.dump(out_dict, out_file)


def parse_file(file_path, out_dict):
    with open(file_path, 'r') as file:
        db = json.load(file)
        for course_id in db:
            for lecturer in db[course_id]["lecturers"]:
                add_course_to_lecturer(course_id, db, lecturer, out_dict)


def add_course_to_lecturer(course_id, db, lecturer, out_dict):
    if lecturer in out_dict:
        if db[course_id]["course_name"] not in out_dict[lecturer]:
            out_dict[lecturer].append(db[course_id]["course_name"])
    else:
        out_dict[lecturer] = [db[course_id]["course_name"]]



