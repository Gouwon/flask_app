from flask_mogokit_driect.flask_mongokit_direct import connection
from mongokit import Document


def max_length(length):
    def validate(value):
        if (len(value) <= length):
            return True
        raise Exception('%s must be at most %s characters long' % length)
    return validate


class User(Document):
    structure = {
        'name': unicode,
        'email': unicode,
    }

    validators = {
        'name': max_length(50),
        'email': max_length(120)
    }

    use_dot_notation = True

    def __repr__(self):
        return '<User %r>' % (self.name)


# register the User document wit our current connection
connection.register([User])