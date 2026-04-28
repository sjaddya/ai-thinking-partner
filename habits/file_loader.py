import re
from pathlib import Path


SPLIT_CATEGORY_RE = re.compile(r"\t+|\s{2,}")
RANGE_RE = re.compile(
    r"\(\s*[+-]?\d+\s*-\s*[+-]?\d+\s*\)|\b[+-]?\d+\s*(?:to|-)\s*[+-]?\d+\b",
    re.IGNORECASE,
)
TYPE_TAG_RE = re.compile(r"\[type:\s*(binary|scalar|count|event)\s*\]", re.IGNORECASE)
ALLOWED_TYPES = {"binary", "scalar", "count", "event"}


def _extract_type_tag(text):
    if not text:
        return None

    match = TYPE_TAG_RE.search(text)
    if match is None:
        return None
    return match.group(1).lower()


def _strip_type_tag(text):
    if not text:
        return ""
    return TYPE_TAG_RE.sub("", text).strip()


def _split_name_and_description(text):
    if " - " in text:
        return text.split(" - ", 1)

    spaced_match = re.search(r"\s-\s*", text)
    if spaced_match is not None:
        return text[:spaced_match.start()], text[spaced_match.end() :]

    loose_match = re.search(r"-\s+", text)
    if loose_match is not None:
        return text[:loose_match.start()], text[loose_match.end() :]

    return text, ""


def _infer_type(name, description):
    explicit_type = _extract_type_tag(description) or _extract_type_tag(name)
    if explicit_type is not None:
        return explicit_type

    text = f"{name} {description}".lower()

    if "yes/no" in text or "yes / no" in text:
        return "binary"

    if RANGE_RE.search(text):
        return "scalar"

    if "(mins)" in text or "minute" in text or "minutes" in text:
        return "count"

    if "how many" in text:
        return "count"

    return "binary"


def _parse_line(line):
    parts = SPLIT_CATEGORY_RE.split(line.strip(), maxsplit=1)
    if len(parts) < 2:
        return None

    category = parts[0].strip()
    remainder = parts[1].strip()
    if not category or not remainder:
        return None

    name_part, description_part = _split_name_and_description(remainder)

    name = name_part.strip()
    description_raw = description_part.strip().lstrip("-").strip()
    description = _strip_type_tag(description_raw)
    if not name:
        return None

    return {
        "category": category,
        "name": name,
        "type": _infer_type(name, description_raw),
        "description": description,
    }


def _is_header_line(line):
    lower_line = line.lower()
    return "activity category" in lower_line and "habit name" in lower_line


def load_habits_from_file(path: str) -> list[dict]:
    file_path = Path(path)
    habits = []

    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if _is_header_line(line):
            continue

        parsed = _parse_line(line)
        if parsed is None:
            continue
        habits.append(parsed)

    return habits


def update_habit_type_in_file(path: str, habit_name: str, habit_type: str) -> bool:
    normalized_name = (habit_name or "").strip().lower()
    normalized_type = (habit_type or "").strip().lower()

    if not normalized_name:
        raise ValueError("habit_name is required")

    if normalized_type not in ALLOWED_TYPES:
        raise ValueError("type must be one of: binary, scalar, count, event")

    file_path = Path(path)
    original_lines = file_path.read_text(encoding="utf-8").splitlines()
    updated_lines = []
    updated = False

    for raw_line in original_lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if not stripped or _is_header_line(stripped):
            updated_lines.append(line)
            continue

        parsed = _parse_line(line)
        if parsed is None or parsed["name"].strip().lower() != normalized_name:
            updated_lines.append(line)
            continue

        description = parsed["description"].strip()
        type_tag = f"[type: {normalized_type}]"
        if description:
            description = f"{description} {type_tag}"
        else:
            description = type_tag

        updated_lines.append(f"{parsed['category']}\t{parsed['name']} - {description}")
        updated = True

    if not updated:
        return False

    new_content = "\n".join(updated_lines)
    if original_lines:
        new_content += "\n"
    file_path.write_text(new_content, encoding="utf-8")
    return True
