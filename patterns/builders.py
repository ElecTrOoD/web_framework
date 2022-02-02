import courses.models as models


class CourseBuilder:
    def __init__(self, course):
        self.course = models.CourseFactory.create(course)

    def name(self, name):
        self.course.name = name
        return self

    def title(self, title):
        self.course.title = title
        return self

    def text(self, text):
        self.course.text = text
        return self

    def categories(self, categories):
        self.course.categories = categories
        return self

    def additional_links(self, links):
        self.course.links = links
        return self

    def build(self):
        return self.course
