import os
import jinja2
import xmltodict

class Junit2HTML(object):
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
        result = dict(summary={}, testcases=[])
        content = xmltodict.parse(self._load_file(path), attr_prefix='', cdata_key='content')["testsuite"]
        result["summary"]["name"] = content["name"]
        for key in ["tests", "errors", "failures", "skip"]:
            result["summary"][key] = int(content[key])
        # this check for one test case in xml file 
        if not isinstance (content['testcase'], list):
            content['testcase'] = [content['testcase']]

        status_map = {"error":"errored", "failure":"failed", "skipped":"skipped"}
        for testcase in content["testcase"]:
            obj = dict()
            for key in testcase.keys():
                if key in status_map:
                    obj["status"] = status_map[key]
                    obj["details"] = dict(testcase[key])
                else:
                    obj[key] = testcase[key]
            
            if not obj.get("status"):
                obj["status"] = "passed"

            result["testcases"].append(obj)
        return result

    def _generate_html(self, result):
        template = self._envrionment.from_string(self._template)
        html = template.render(** result)
        return html

    def _export_html(self, html, path="."):
        with open(path, "w") as f:
            f.write(html)
        print("File saved to {}".format(path))

    def convert(self, path, dest):
        result = self.parse(path)
        html = self._generate_html(result)
        self._export_html(html, dest)