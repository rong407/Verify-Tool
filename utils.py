def print_result(fp, result):

    print("\n=== FILE FINGERPRINT ===")
    for k, v in fp.items():
        print(f"{k}: {v}")

    print("\n=== TRACE RESULT ===")

    if result and "status" not in result:
        print("✔ SOURCE FOUND")
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        print("✖ NOT FOUND IN LOG")
