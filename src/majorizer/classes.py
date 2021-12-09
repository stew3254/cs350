# from models import *
from majorizer.models import *


def _get_data(obj) -> dict:
    """

    :param obj: The object all public data fields should be grabbed from
    :return: Dictionary where the key is the field name and the value is the object's field value
    """

    return {e: getattr(obj, e) for e in dir(obj) if not e.startswith("_") and e != "objects" and not callable(getattr(obj, e))}


class ABC:
    """
    An abstract base class to derive all classes from. This will define the init functionality
    to reduce the amount of copied code
    """

    def __init__(self, obj=None, **kwargs):
        """
        :param obj: A database object if one exists
        :param kwargs: The list of arguments to be passed to initialize the class
        """

        # Get the name of the object
        name = self.__getname()

        # Add the object under the name of the class
        self.__setattr__(name, obj)

        # If an object is passed in, ignore everything else
        if obj is not None:
            # Set data from object to the same as this object
            for k, v in _get_data(obj).items():
                self.__setattr__(k, v)

        # No object passed in, so just take keyword args and make our own new object
        else:
            # Set all keyword arguments as passed in
            for k, v in kwargs:
                self.__setattr__(k, v)

            # Leave it up to the deriving class to set the object(s) appropriately

    def __getname(self) -> str:
        # Get class name
        class_name = str(self.__class__).strip("DB").split("'")[1]
        # Strip preceding dots
        class_name = class_name.split('.')[-1]

        # Transform name to snake case
        name = ""
        for i, c in enumerate(class_name):
            if c.isupper():
                name += "_" + c.lower()
            else:
                name += c
        return name

    def to_json(self) -> dict:
        return _get_data(self)

    def db(self):
        return self.__getattribute__(self.__getname()).__class__


class Department(ABC):

    def __init__(self, obj=None, **kwargs):
        # Call parent class init
        super().__init__(obj, **kwargs)

        # Set the appropriate object name and initialize the class with the data
        if obj is None:
            self.__setattr__(self.__getname(), DBDepartment(**_get_data(self)))


class Course(ABC):

    def __init__(self, obj=None, **kwargs):
        # Call parent class init
        super().__init__(obj, **kwargs)

        # Set the appropriate object name and initialize the class with the data
        if obj is None:
            # Special since courses are instances of course offerings
            self._course_offering = DBCourseOffering(**_get_data(self))

    def db(self):
        return self.__getattribute__(self._course_offering).__class__


class Major(ABC):

    def __init__(self, obj=None, **kwargs):
        # Call parent class init
        super().__init__(obj, **kwargs)

        # Set the appropriate object name and initialize the class with the data
        if obj is None:
            self.__setattr__(self.__getname(), DBDegreeProgram(**_get_data(self), is_major=True))


class Minor(ABC):

    def __init__(self, obj=None, **kwargs):
        # Call parent class init
        super().__init__(obj, **kwargs)

        # Set the appropriate object name and initialize the class with the data
        if obj is None:
            self.__setattr__(self.__getname(), DBDegreeProgram(**_get_data(self), is_major=False))


# TODO figure out how to get authentication information in here
class Student(ABC):

    def __init__(self, obj=None, **kwargs):
        # Call parent class init
        super().__init__(obj, **kwargs)

        # Set the appropriate object name and initialize the class with the data
        if obj is None:
            self.__setattr__(self.__getname(), DBStudent(**_get_data(self)))


# TODO figure out how to get authentication information in here
class Advisor(ABC):

    def __init__(self, obj=None, **kwargs):
        # Call parent class init
        super().__init__(obj, **kwargs)

        # Set the appropriate object name and initialize the class with the data
        if obj is None:
            self.__setattr__(self.__getname(), DBAdvisor(**_get_data(self)))


class Schedule(ABC):

    def __init__(self, obj=None, **kwargs):
        # Call parent class init
        super().__init__(obj, **kwargs)

        # Set the appropriate object name and initialize the class with the data
        if obj is None:
            self.__setattr__(self.__getname(), DBSchedule(**_get_data(self)))


class Comment(ABC):

    def __init__(self, obj=None, **kwargs):
        # Call parent class init
        super().__init__(obj, **kwargs)

        # Set the appropriate object name and initialize the class with the data
        if obj is None:
            self.__setattr__(self.__getname(), DBComment(**_get_data(self)))
