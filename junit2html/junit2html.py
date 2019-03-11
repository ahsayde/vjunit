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
        return self.parse_content(self._load_file(path))

    def parse_content(self, content):
        content = xmltodict.parse(content, attr_prefix='', cdata_key='content')["testsuite"]
        result = dict(summary={}, testcases=[])
        result["summary"]["name"] = content["name"]
        for key in ["tests", "errors", "failures", "skip"]:
            result["summary"][key] = int(content[key])
        # this check for one test case in xml file 
        status_map = {"error":"errored", "failure":"failed", "skipped":"skipped"}
        if content.get("testcase"):
            if not isinstance (content['testcase'], list):
                content['testcase'] = [content['testcase']]
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
        else:
            result["testcases"] = list()
        return result

    def generate_html(self, result, embed=False):
        template = self._envrionment.from_string(self._template)
        html = template.render(embed=embed, **result)
        return html

    def _export_html(self, html, path="."):
        with open(path, "w") as f:
            f.write(html)
        print("File saved to {}".format(path))

    def convert(self, path, dest):
        result = self.parse(path)
        html = self.generate_html(result)
        self._export_html(html, dest)
