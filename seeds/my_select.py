from sqlalchemy import func

from conf.connect_db import session
from conf.models import Student, Teacher, Group, Grade, Subject


def select_01():
    average_grades = (
        session.query(Student, func.avg(Grade.grade).label('average_grade'))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )

    for student, avg_grade in average_grades:
        print(f"Студент: {student.fullname}, Середній бал: {avg_grade}")


def select_02(subject_id=1):
    average_grades = (
        session.query(Student, func.avg(Grade.grade).label('average_grade'))
        .join(Grade)
        .filter(Grade.subjects_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )

    student, avg_grade = average_grades
    print(f"Студент: {student.fullname}, Середній бал: {avg_grade}")


def select_03(subject_id=1):
    average_grades_by_group = (
        session.query(Group.name, func.avg(Grade.grade).label('average_grade'))
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .filter(Grade.subjects_id == subject_id)
        .group_by(Group.name)
        .all()
    )

    for group_name, avg_grade in average_grades_by_group:
        print(f"Група: {group_name}, Середній бал: {avg_grade}")



def select_04():
    average_grade_overall = (
        session.query(func.avg(Grade.grade).label('average_grade'))
        .scalar()
    )

    print(f"Середній бал на потоці: {average_grade_overall}")


def select_05(teacher_id=1):
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()

    if teacher:
        subjects_taught = teacher.subjects
        for subject in subjects_taught:
            print(f"Викладач {teacher.fullname} читає предмет {subject.name}")
    else:
        print(f"Викладач з ID {teacher_id} не знайдений.")


def select_06(group_id=1):
    group = session.query(Group).filter_by(id=group_id).first()

    if group:
        students_in_group = group.students
        for student in students_in_group:
            print(f"Студент: {student.fullname}")
    else:
        print(f"Група з ID {group_id} не знайдена.")


def select_07(group_id=1, subject_id=1):
    group = session.get(Group, group_id)
    subject = session.get(Subject, subject_id)

    if group and subject:
        grades_in_group = session.query(Grade). \
            filter(Grade.student_id.in_([student.id for student in group.students])). \
            filter(Grade.subjects_id == subject.id).all()

        for grade in grades_in_group:
            print(f"Студент: {grade.student.fullname}, Оцінка: {grade.grade}")
    else:
        print(f"Група з ID {group_id} або предмет з ID {subject_id} не знайдені.")


def select_08(teacher_id=1):
    teacher = session.get(Teacher, teacher_id)

    if teacher:
        subjects = teacher.subjects

        for subject in subjects:
            grades_for_subject = session.query(Grade).filter(Grade.subjects_id == subject.id).all()
            if grades_for_subject:
                total_grades = sum(grade.grade for grade in grades_for_subject)
                average_grade = total_grades / len(grades_for_subject)

                print(f"Предмет: {subject.name}, Середній бал: {average_grade}")
            else:
                print(f"Для предмета {subject.name} немає оцінок.")
    else:
        print(f"Викладача з ID {teacher_id} не знайдено.")


def select_09(student_id=1):
    student = session.get(Student, student_id)

    if student:
        group = student.group
        if group:
            subjects_for_group = [grade.discipline for grade in student.grade]
            sub = set(subjects_for_group)

            if sub:
                print(f"Студент {student.fullname} відвідує курси:")
                for subject in sub:
                    print(subject.name)
            else:
                print(f"Група {group.name} не має предметів.")
        else:
            print(f"Студент {student.fullname} не має призначеної групи.")
    else:
        print(f"Студента з ID {student_id} не знайдено.")


def select_10(student_id=1, teacher_id=1):
    student = session.get(Student, student_id)
    teacher = session.get(Teacher, teacher_id)

    if student and teacher:
        grades_for_student_and_teacher = session.query(Grade).filter(
            Grade.student_id == student_id,
            Grade.discipline.has(teacher_id=teacher_id)
        ).all()

        if grades_for_student_and_teacher:
            g = []
            print(f"Студент {student.fullname} отримав оцінки від викладача {teacher.fullname} за курси:")
            for grade in grades_for_student_and_teacher:
                if grade.discipline.name not in g:
                    print(grade.discipline.name)
                    g.append(grade.discipline.name)
        else:
            print(f"Студент {student.fullname} не отримав оцінок від викладача {teacher.fullname}.")
    else:
        print(f"Студента з ID {student_id} або викладача з ID {teacher_id} не знайдено.")


if __name__ == '__main__':
    select_01()
    # select_02()
    # select_03()
    # select_04()
    # select_05()
    # select_06()
    # select_07()
    # select_08()
    # select_09()
    # select_10()
