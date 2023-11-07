import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.connect_db import session
from conf.models import Student, Teacher, Group, Grade, Subject

fake = Faker('uk-UA')


def insert_student():
    for _ in range(30):
        student = Student(fullname=fake.name(),
                          group_id=random.randint(1, 3))
        session.add(student)


def insert_student_group_id():
    students = session.query(Student).all()

    for student in students:
        student.group_id = random.randint(1, 3)


def insert_groups():
    group_names = ['A', 'B', 'C']
    for name in group_names:
        group = Group(name=name)
        session.add(group)


def insert_subjects():
    for _ in range(6):
        subject = Subject(name=fake.job(),
                          teacher_id=random.randint(1, 4))
        session.add(subject)


def insert_teachers():
    for _ in range(5):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)


def insert_grades():
    for s in range(1, 31):
        for n_s in range(1, 7):
            for _ in range(10):
                grade = Grade(
                    student_id=s,
                    subjects_id=n_s,
                    grade=random.randint(3, 5),
                    grade_date=fake.date_between(start_date='-3y', end_date='today')
                )
                session.add(grade)


if __name__ == '__main__':
    try:
        insert_grades()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
