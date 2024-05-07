from main.models import Course


def document_list(documents):
    doc = []
    for document in list(documents):
        ele = {}
        ele['title'] = document.title
        ele['url'] = document.url
        print(document.url)
        print(document.title)
        doc.append(ele)
    return doc
def collect_data(data,permission):
    ele = {}
    ele['meet'] = data.meet
    ele['id'] = data.id
    ele['teacher'] = data.teacher.user.username
    ele['name'] = data.name
    if data.photo:
        ele['photo'] = data.photo.name
    else:
        ele['photo'] = 'course/course-lg.jpg'
    if permission == 2:
        students = []
        for student in list(data.mystudent.all()):
            students.append(student.profile.user.username)
        ele['your_student'] = students
    return ele

def course_list(datas,permission,name):
    courses = []
    for data in datas:
        courses.append(collect_data(data,permission))
    if name == None:
        # 待更改 courses[0] 可能有error
        try:
            return courses, courses[0]
        except:
            return courses,'no course'
    # 尚未完成的功能
    else:
        main_course = Course.objects.filter(name = name).first()
        print(main_course)
        if main_course:
            course = []
            course.append(collect_data(main_course,permission))
            return courses, course[0]
        else :
            return courses,'no permission'