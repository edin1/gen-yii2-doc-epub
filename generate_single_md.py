from optparse import OptionParser
import re
import urllib.request
import os

def main():
    cli_parser = OptionParser(
        usage='usage: %prog [options] [README.md] [output.md]'
        )
    (options, args) = cli_parser.parse_args()

    try:
        readme_fname = args[0]
    except IndexError:
        readme_fname = "README.md"

    try:
        outfname = args[1]
    except IndexError:
        outfname = "output.md"

    # outfname = os.path.abspath(outfname)
    basename = os.path.basename(readme_fname)
    basedir = os.path.dirname(readme_fname)
    os.chdir(basedir)
    with open(basename, newline=None) as readme_file:
        toc = readme_file.read()

    out = ""
    pattern = "[*] \[(.*?)\]\((.*?)\)"
    for line in toc.split("\n"):
        if line.startswith("* "):
            if line.find("**TBD**") != -1:
                out += line + "\n"
            else:
                m = re.match(pattern, line)
                title = m.groups()[0]
                url = m.groups()[1]
                print("Parsing %s"%url)
                out += title + "\n"
                out += "*"*len(title) + "\n\n"
                ISURL = False
                for scheme in ("http://", "https://"):
                    if url.startswith(scheme):
                        ISURL = True
                        # response = urllib.request.urlopen(url)
                        # data = response.read()      # a `bytes` object
                        # text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
                        out += "[%s](%s)\n"%(title, url)
                        break
                if not ISURL:
                    with open(url, newline=None, encoding="utf-8") as tempf:
                        text = tempf.read()
                    out += text + "\n"
        else:
            out += line + "\n"

    with open(outfname, "w", encoding="utf-8") as outfile:
        outfile.write(out)

if __name__ == "__main__":
    main()