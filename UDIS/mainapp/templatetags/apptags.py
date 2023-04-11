
from django import template
register = template.Library()


@register.filter
def at_index(array, index):
    return array[index]


@register.filter
def arr_contains(array, item):
    if item in array:
        return True
    else:
        return False
@register.filter
def to_str(project):
    str=""
    array=project.professor_set.all()
    for item in array:
        str+=item.name+","
    return str[:-2]

@register.filter
def prereq(course):
    str=""
    print(course.name)
    array=course.prerequisites.all()
    print(array)
    for item in array:
        str+=item.subno+","
    return str[:-1]

@register.filter
def multiply(a,b):
    return a*b



@register.filter
def getProfs(course):
    str=""
    profs = course.professor_set.all()
    for prof in profs:
        str += prof.name+", "
    return str[:-2]
