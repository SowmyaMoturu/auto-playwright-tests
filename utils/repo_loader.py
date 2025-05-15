def load_all_files(repo_path):
    import os
    docs = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".ts") or file.endswith(".js"):
                with open(os.path.join(root, file), "r") as f:
                    docs.append(f.read())
    return docs