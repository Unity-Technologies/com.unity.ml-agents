import os


def main():
    asset_paths = [
        "./",
    ]
    meta_suffix = ".meta"
    python_suffix = ".py"
    allow_list = frozenset(
        [
            "./.editorconfig",
            "./.gitignore",
            "./.npmignore",
            "./Tests/.tests.json",
            "./.pre-commit-config.yaml",
            "./.pre-commit-search-and-replace.yaml",
            "./.git"
        ]
    )
    ignored_dirs = {"Documentation~", ".git", ".yamato", ".github"}

    num_matched = 0

    unmatched = set()

    for asset_path in asset_paths:
        for root, dirs, files in os.walk(asset_path):
            # Modifying the dirs list with topdown=True (the default) will prevent us from recursing those directories
            for ignored in ignored_dirs:
                try:
                    dirs.remove(ignored)
                except ValueError:
                    pass

            dirs = set(dirs)
            files = set(files)

            combined = dirs | files
            for f in combined:

                if f.endswith(python_suffix):
                    # Probably this script; skip it
                    continue

                full_path = os.path.join(root, f)
                if full_path in allow_list:
                    continue

                # We expect each non-.meta file to have a .meta file, and each .meta file to have a non-.meta file
                if f.endswith(meta_suffix):
                    expected = f.replace(meta_suffix, "")
                else:
                    expected = f + meta_suffix

                if expected not in combined:
                    unmatched.add(full_path)
                else:
                    num_matched += 1

    if unmatched:
        raise Exception(
            f"Mismatch between expected files and their .meta files: {sorted(unmatched)}"
        )

    print(f"Found {num_matched} correctly matched files")


if __name__ == "__main__":
    main()
