import os
import jinja2
import xml.etree.ElementTree as ET


class VJunit(object):
    def __init__(self, *args, **kwargs):
        self._envrionment = jinja2.Environment()
        self._load_template()

    def _load_file(self, path):
        with open(path, "r") as f:
            content = f.read()
        return content

    def _load_template(self):
        path = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(path, "template.html")
        self._template = self._load_file(template_path)

    def parse(self, path):
        return self.parse_content(self._load_file(path))

    def parse_content(self, content):
        result = list()
        tree = ET.fromstring(content)
        for testsuite in tree.iter(tag="testsuite"):
            _testsuite = dict(summary={}, testcases=[])
            _testsuite["summary"] = testsuite.attrib
            for testcase in testsuite.iter(tag="testcase"):
                _testcase = testcase.attrib
                children = testcase.getchildren()
                if children:
                    stdout = []
                    for child in children:
                        if child.tag == "system-out":
                            stdout.append(child.text)
                        else:
                            _testcase["status"] = child.tag
                            _testcase["text"] = child.text
                    else:
                        _testcase["stdout"] = "\n".join(stdout)
                else:
                    _testcase["status"] = "success"

                _testsuite["testcases"].append(_testcase)

            result.append(_testsuite)
        return result

    def generate_html(self, result, embed=False):
        template = self._envrionment.from_string(self._template)
        html = template.render(embed=embed, testsuites=result)
        return html

    def _export_html(self, html, path="."):
        with open(path, "w") as f:
            f.write(html)
        print("File saved to {}".format(path))

    def convert(self, path, dest):
        testsuites = self.parse(path)
        html = self.generate_html(testsuites)
        self._export_html(html, dest)
