import sys

from extractor import extract_fingerprint
from parser import parse_fingerprint
from api_client import search_by_hash
from utils import print_result


def main():

    if len(sys.argv) < 2:
        print("Usage: python main.py <file>")
        return

    file_path = sys.argv[1]

    print("Analyzing file:", file_path)

    # 1. Extract
    raw = extract_fingerprint(file_path)

    if not raw:
        print("No fingerprint found")
        return

    # 2. Parse
    fp = parse_fingerprint(raw)

    if not fp:
        print("Invalid fingerprint format")
        return

    # 3. Search
    result = search_by_hash(fp["hash"])

    # 4. Show result
    print_result(fp, result)


if __name__ == "__main__":
    main()
