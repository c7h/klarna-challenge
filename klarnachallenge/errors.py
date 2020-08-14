errors = {
    'ParameterException': {
        'message': "Wrong parameter provided",
        'status': 400,
        'extra' : "please provide valid arguments"
    },
    'RuntimeError': {
        'message': "Computation too hard",
        'status': 416,
        'extra' : "I am not a supercomputer"
    },
    'RecursionError': {
        'message': "Computation too hard",
        'status': 416,
        'extra' : "choose a different resource name"
    },
    'NotFoundException': {
        'message': "This resource does not exist",
        'status': 404,
        'extra': "I am very, very sorry..."
    },
    'ValueError': {
        'message': "Wrong values provided in request",
        'status': 400,
        'extra': "check your parameters and try again"
    }
}


class ParameterException(ValueError):
    pass

class NotFoundException(ValueError):
    pass
