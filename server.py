from pathlib import Path
from flask import Flask, abort, send_from_directory
from waitress import serve

folder = Path(__file__).parent / "sites"
app = Flask(__name__, template_folder="sites")

def makefile(filetoprocess):
    with open(f"sites/{filetoprocess}.sw", "a") as f:
        for line in file.read_text().splitlines():
            processline (line)
            lines.append("\n")

def processline(line):
    debug = 1
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
    print(f"Found file: {file.stem}")
    makefile(file.stem)

    with open(f"sites/{file.stem}.html", "w") as f:
        f.write("<html><body>")
        f.write('<link rel="stylesheet" href="/static/styles.css">')
        f.write("".join(lines))
        f.write("</body></html>")

@app.route("/")
def home():
    print(f"Rebuilding: home")
    makefile(f"home")
    return send_from_directory(folder, f"home.html")
    file_path = folder / 'home.html'
    if not file_path.exists():
        abort(404)
    return file_path.read_text()

@app.route("/<page>")
def serve_page(page):
    print(f"Rebuilding: {page}")
    makefile(f"{page}")
    return send_from_directory(folder, f"{page}.html")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)