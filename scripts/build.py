"""教材のファイル名・本文から静的サイトを生成する（Python標準ライブラリのみ）。"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {".py", ".js", ".ts", ".html", ".css", ".txt", ".json", ".md", ".csv", ".java", ".c", ".cpp", ".h", ".sql", ".sh", ".rb", ".xml", ".yaml", ".yml", ".svg"}

def sort_key(path):
    return tuple((0, int(s)) if s.isdigit() else (1, s.casefold()) for s in re.split(r"(\d+)", path.name))

def collect(root):
    lessons = []
    for number in range(1, 7):
        folder = root / "codes" / f"{number:02}"
        codes = []
        for path in sorted(folder.iterdir() if folder.exists() else [], key=sort_key):
            if path.name.startswith("."):
                continue
            if path.is_symlink():
                raise ValueError(f"シンボリックリンクは使えません: {path}")
            if path.is_dir():
                raise ValueError(f"教材は各回の直下に置いてください: {path}")
            if path.suffix.lower() not in EXTENSIONS:
                raise ValueError(f"未対応の拡張子です: {path}")
            if path.stat().st_size > 1_000_000:
                raise ValueError(f"教材は1ファイル1MB以下にしてください: {path}")
            # 改行（CRLFを含む）をそのまま保持する。
            content = path.read_bytes().decode("utf-8-sig")
            if "\x00" in content:
                raise ValueError(f"テキストではありません: {path}")
            name = re.sub(r"^\d+[_-]", "", path.stem) or path.stem
            codes.append({"name": name, "filename": path.name, "content": content})
        lessons.append({"number": number, "title": f"第{number}回", "codes": codes})
    return {"lessons": lessons}

def build(root=ROOT):
    data = collect(root)
    output = root / "_site"
    if output.exists():
        shutil.rmtree(output)
    (output / "assets").mkdir(parents=True)
    shutil.copy2(root / "index.html", output / "index.html")
    for filename in ("style.css", "app.js"):
        shutil.copy2(root / "assets" / filename, output / "assets" / filename)
    # ASCIIエスケープでUnicode改行も含めて安全な外部JavaScriptデータにする。
    (output / "assets" / "materials.js").write_text(
        "window.CODE_LIBRARY = " + json.dumps(data, ensure_ascii=True) + ";\n", encoding="utf-8")
    (output / ".nojekyll").touch()
    print(f"Generated {output}: {sum(len(x['codes']) for x in data['lessons'])} materials")

if __name__ == "__main__":
    build()
