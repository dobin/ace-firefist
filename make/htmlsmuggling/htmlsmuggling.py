import argparse
from jinja2 import Template
from pathlib import Path
from base64 import b64encode
from model import AceFile, PluginDecorator, disableOut


@PluginDecorator
def makeHtmlSmuggling(file) -> bytes:
    data = b64encode(file.data).decode()

    with open('make/htmlsmuggling/standard.html') as f:
        template = Template(f.read())
    
    out = template.render(
        data=data,
        filename=file.name,
    )
    return bytes(out, 'utf-8')


def main():
    disableOut()
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="")
    parser.add_argument("--payload_data", help="")
    parser.add_argument("--payload_name", help="")
    args = parser.parse_args()

    file = AceFile(
        args.payload_name,
        bytes(args.payload_data, 'utf-8')
    )
    htmlData = makeHtmlSmuggling(file)

    f = open(args.filename, 'w')
    f.write(htmlData)
    f.close()


if __name__ == "__main__":
    main()