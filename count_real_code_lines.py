import os

EXCLUDE_DIRS = {".venv", "__pycache__", "migrations"}
EXTENSIONS = {".py"}  # poți adăuga .js, .ts etc


def count_lines(root_dir):
    total = 0

    for root, dirs, files in os.walk(root_dir):
        # elimină directoare nedorite
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        total += len(lines)
                except Exception:
                    pass

    return total


if __name__ == "__main__":
    total = count_lines("backend/app")
    print(f"Total lines of code: {total}")