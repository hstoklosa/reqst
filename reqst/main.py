import sys
import json
import yaml
from functools import partial
from requests.api import request
from lxml import etree, html
from .utils import bout, out, err, by_key_lower


STDOUT_STAYS_ON_TERMINAL = sys.stdout.isatty()
STDERR_STAYS_ON_TERMINAL = sys.stderr.isatty()

# Use colors only on terminal and NOT on file
# i.e. don't import if both are redirected to files
if STDOUT_STAYS_ON_TERMINAL or STDERR_STAYS_ON_TERMINAL:
    from pygments import highlight
    from pygments.lexers.data import JsonLexer, YamlLexer
    from pygments.lexers.html import HtmlLexer, XmlLexer
    from pygments.formatters.terminal256 import TerminalTrueColorFormatter
    from pygments.formatters.terminal import TerminalFormatter


def send_request(req): return request(**req)


def output_formatted(res):
    handle_metadata_output(res)
    
    content_type = res.headers.get("content-type", "")
    if content_type.startswith("application/json"):
        handle_json_output(res.text)
    elif content_type.startswith("text/xml"):
        handle_xml_output(res.text)
    elif content_type.startswith("text/html"):
        handle_html_output(res.text)
    elif content_type.startswith("text"):
        handle_plain_output(res.text)
    else:
        handle_binary_output(res.content)


def handle_metadata_output(res):
    metadata = []
    metadata.append(f"Status: {res.status_code}")
    for k, v in sorted(res.headers.items(), key=by_key_lower):
        metadata.append(f"{k}: {v}")
    text = "\n".join(metadata)

    if STDOUT_STAYS_ON_TERMINAL:
        text = highlight(text, YamlLexer(), TerminalTrueColorFormatter())
    err(text)


def handle_json_output(text):
    text = json.dumps(json.loads(text), indent=4)
    if STDOUT_STAYS_ON_TERMINAL:
        text = highlight(text, JsonLexer(), TerminalFormatter())
    out(text)


def handle_xml_output(text):
    data = etree.fromstring(text)
    etree.indent(data, space=" "*2)
    text = etree.tostring(data, encoding="unicode")
    if STDOUT_STAYS_ON_TERMINAL:
        text = highlight(text, XmlLexer(), TerminalFormatter())
    out(text)


def handle_html_output(text):
    data = html.fromstring(text)
    etree.indent(data, space=" "*2)
    text = html.tostring(data, encoding="unicode")
    if STDOUT_STAYS_ON_TERMINAL:
        text = highlight(text, HtmlLexer(), TerminalFormatter())
    out(text)


def handle_plain_output(text):
    out(text)


def handle_binary_output(content):
    bout(content)


def read_file(filepath):
    if filepath.endswith(".yml") or filepath.endswith(".yaml"):
        loader = partial(yaml.load, Loader=yaml.FullLoader)
    elif filepath.endswith(".json"):
        loader = json.load
    else:
        raise Exception("Unsupported file type")

    with open(filepath, "r") as f:
        file_data = loader(f)

    return file_data