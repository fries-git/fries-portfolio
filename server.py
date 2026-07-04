from pathlib import Path
from flask import Flask, abort, send_from_directory
from waitress import serve

folder = Path(__file__).parent / "sites"
app = Flask(__name__, template_folder="sites")

def makefile(filetoprocess):
    with open(f"sites/{filetoprocess}", "a") as f:
        debug = 1
        for line in file.read_text().splitlines():
            processline (line)
            lines.append("\n")

def processline(line):
    debug = 1
    print(f"Processing line: {line} at number {debug}")
    debug += 1
    start = line.find("[") + 1
    end = line.find("]")
    if start > 0 and end > start:
        result = line[start:end]

    tag = result.lower()

    start = line.find("{") + 1
    end = line.rfind("}")
    if start > 0 and end > start:
        result = line[start:end]
    content = result
    print(result)

    # The block...
    if tag == "header":
        lines.append(f"<h1>{content}</h1>")
    elif tag == "body":
        lines.append(f"<p>{content}</p>")
    elif tag == "chapter":
        lines.append(f"<h2>{content}</h2>")
    elif tag == "section":
        lines.append(f"<h3>{content}</h3>")
    elif tag == "footer":
        lines.append(f"<footer><small>{content}</small></footer>")
    elif tag == "link":
        lines.append(f'<p><a href="{content}" target="_blank" rel="noopener noreferrer">{content}</a></p>')
    elif tag == "image":
        lines.append(f'<p><img src="{content}" alt="Description of the image"></p>')
    elif tag == "pagelink":
        lines.append(f'<nav><a href="/{content}">{content}</a></nav>')
    elif tag == "code":
        lines.append(f"<p><code>{content}</code></p>")
    elif tag == "small":
        lines.append(f"<p><small>{content}</small></p>")
    elif tag == "frame":
        lines.append(f"<p><iframe src={content}></iframe></p>")
    elif tag == "quote":
        lines.append(f"<blockquote> - {content}</blockquote>")
    elif tag == "dialog":
        lines.append(f"<dialog open>{content}</dialog>")
    elif tag == "underline":
        lines.append(f"<p><u>{content}</u></p>")
    elif tag == "bold":
        lines.append(f"<p><b>{content}</b></p>")

for file in folder.glob("*.sw"):
    lines = []
    print(f"Found file: {file.name}")
    fileedit = ((file.with_suffix(".html")).name)

    makefile(fileedit)

    with open(f"sites/{fileedit}", "w") as f:
        f.write("<html><body>")
        f.write('<link rel="stylesheet" href="/static/styles.css">')
        f.write("".join(lines))
        f.write("</body></html>")

@app.route("/")
def home():
    file_path = folder / 'home.html'
    if not file_path.exists():
        abort(404)
    return file_path.read_text()

@app.route("/source/<path:filename>")
def source(filename):
    return send_from_directory(folder, filename, mimetype="text/plain")

@app.route("/<page>")
def serve_page(page):
    file_path = folder / f"{page}.html"

    if not file_path.exists():
        abort(404)

    return file_path.read_text()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)