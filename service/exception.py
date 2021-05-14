class InvalidProjectError(Exception):
    def __init__(self, project_id):
        self.project_id = project_id

    def __str__(self):
        return f'Cannot find project {self.project_id}'

class InvalidServiceError(Exception):
    def __init__(self, project_id, service_id):
        self.project_id = project_id
        self.service_id = service_id
    
    def __str__(self):
        return (f'Cannot find service {self.service_id} '
               f'in project {self.project_id}')

class InvalidLogRequest(Exception):
    pass


class TokenError(Exception):
    pass


def exception_detail(e):
    exception=e.__class__.__name__
    msg = str(e)

    if 'NotFound' in exception:
        exception = 'NotFound'

    if exception == 'InvalidServiceError':
        reason = 'ServiceNotFound'
    elif exception == 'InvalidProjectError':
        reason = 'ProjectNotFound'
    elif exception == 'InvalidLogRequest':
        reason = 'ServiceNotRunning'
    elif exception == 'TokenError':
        reason = exception
    else:
        reason = 'InternalError'
        # reason = exception

    return {'msg': msg, 'reason': reason}