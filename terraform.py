#!/usr/bin/env python

import sys
import os
import glob
import yaml
import json
import imp
import subprocess
import argparse
import pprint

class TerraformGenerator(object):
    def __init__(self):
        return

    def run(self):
        for filename in glob.glob("./*.yaml"):
            with open(filename, "r") as file:
                config_file = yaml.load(file)
                try:
                    template_file = config_file['template_file']
                    del config_file['template_file']
                except KeyError:
                    print("Key 'template_file' not found in " + filename)
                    sys.exit(1)
                try:
                    #template_cmd = " ".join(["python", template_file, pickle.dumps(template)])
                    #print(template_cmd)
                    #rendered_template = subprocess.check_output(template_cmd, stderr=subprocess.PIPE)
                    template_name = os.path.basename(template_file).split(".")[0]
                    template = __import__(template_name)
                    template.generate_terraform(config_file)
                except subprocess.CalledProcessError as e:
                    print('exit code: {}'.format(e.returncode))
                    print('stdout: {}'.format(e.output.decode(sys.getfilesystemencoding())))
                    print('stderr: {}'.format(e.stderr.decode(sys.getfilesystemencoding())))

class Element(object):
    def __init__(self, name):
        self.name = name

    def print_element(self):
        return

class Resource(Element):
    def __init__(self, kwargs):
        Element.__init__(self, self.__class__.__name__)
        self.body = {}
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def print_element(self):
        for key, value in self.__dict__.iteritems():
            self.body.update({key: value})
        del self.body['body']
        resource = ("resource \"{type}\" \"{name}\" \n {body} \n").format(
            type=self.__class__.__name__,
            name=self.name,
            body=self.body
        )
        return resource

class Template(object):
    def __init__(self, body):
        self.body = body
        self.resources = []
        self.data = []
        self.modules = []
        self.outputs = []
        self.variables = []

    def add_resource(self, resource):
        list.append(self.resources, resource)

    def add_data(self, kwargs):
        return

    def add_module(self, kwargs):
        return

    def add_output(self, kwargs):
        return

    def add_variable(self, kwargs):
        return

    def print_to_file(self):
        for attribute in ['resources', 'data', 'modules']:
            elements = getattr(self, attribute)
            if len(elements) != 0:
                with open("main.tf", 'w') as fh:
                    for element in elements:
                        fh.write(element.print_element())
        outputs = getattr(self, 'outputs')
        if len(outputs) != 0:
            with open("outputs.tf", 'w') as fh:
                for output in outputs:
                    fh.write(output.print_element())
        variables = getattr(self, 'variables')
        if len(variables) != 0:
            with open("variables.tf", 'w') as fh:
                for variable in variables:
                    fh.write(variable.print_element())

if __name__ == '__main__':
    generator = TerraformGenerator()
    generator.run()
