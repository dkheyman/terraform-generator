from terraform import Resource
from terraform import Template

class aws_iam_role(Resource):

    def __init__(self, **kwargs):
        Resource.__init__(self, kwargs)
        self.assume_role_policy = ""

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

class aws_iam_policy(Resource):

    def __init__(self, **kwargs):
        Resource.__init__(self, kwargs)
        self.policy = ""
        self.path = "/"

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

class aws_iam_instance_profile(Resource):

    def __init__(self, **kwargs):
        Resource.__init__(self, kwargs)

        for key, value in kwargs.iteritems():
            setattr(self, key, value)
            
class IamTemplate(Template):
    def __init__(self, body):
        Template.__init__(self, body)
        self.add_resources()

    def add_resources(self):
        print(self.body['resources'])
        for type, resources in self.body['resources'].iteritems():
            if type == 'aws_iam_role':
                for resource_name, resource_body in resources.iteritems():
                    print resource_body['assume_role_policy']
                    self.add_resource(
                        aws_iam_role(
                            name=resource_body['name'],
                            assume_role_policy=resource_body['assume_role_policy']
                        )
                    )
            elif type == 'aws_iam_policy':
                for resource_name, resource_body in resources.iteritems():
                    self.add_resource(
                        aws_iam_policy(
                            name=resource_body['name'],
                            policy=resource_body['policy'],
                            path=resource_body['path']
                        )
                    )

def generate_terraform(body):
    IamTemplate(body).print_to_file()
