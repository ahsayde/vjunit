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
                children = list(testcase)
                if children:
                    stdout = []
                    for child in children:
                        if child.tag == "system-out":
                            stdout.append(child.text)
                        else:
                            _testcase["status"] = child.tag
                            _testcase["text"] = child.text
                            _testcase["type"] = child.attrib.get("type")
                            _testcase["message"] = child.attrib.get("message")
                    else:
                        _testcase["stdout"] = "\n".join(stdout)
                else:
                    _testcase["status"] = "success"

                _testsuite["testcases"].append(_testcase)

            tests = testsuite.attrib.get("tests", 0)
            errors = testsuite.attrib.get("errors", 0)
            failures = testsuite.attrib.get("failures", 0)
            skipped = testsuite.attrib.get("skip", 0) or testsuite.attrib.get(
                "skipped", 0
            )

            if int(errors):
                _testsuite["summary"]["status"] = "error"
            elif int(failures):
                _testsuite["summary"]["status"] = "failure"
            elif int(tests) == int(skipped):
                _testsuite["summary"]["status"] = "skipped"
            else:
                _testsuite["summary"]["status"] = "success"

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
