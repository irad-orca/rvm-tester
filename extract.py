def parse_java_verbose_log(log_file: str) -> list[str]:
    # parse the log file to get the jars loaded
    # [Loaded java.util.Collections$UnmodifiableSortedMap from /usr/lib/jvm/java-1.8-openjdk/jre/lib/rt.jar]
    # return distinct jars /usr/lib/jvm/java-1.8-openjdk/jre/lib/rt.jar

    loaded_jars = set()

    with open(log_file) as f:
        for line in f:
            # Skip non-class-load lines
            if "[info][class,load]" not in line:
                continue

            line = line.strip()

            # Extract the jar file path after "source: "
            if "source: " not in line:
                continue

            jar_file = line.split("source: ", 1)[1]

            # Skip non-jar files and special sources like jrt:/
            if not jar_file.startswith("file:") and not jar_file.endswith(".jar"):
                continue

            # normalize nested jars and file: prefix
            jar_file = jar_file.removeprefix("file:")

            loaded_jars.add(jar_file)

    return list(loaded_jars)


def parse_python_verbose_log(log_file: str) -> list[str]:
    # Parse Python verbose import logs
    # import time # installing zipimport hook
    # import zipimport # loaded from /usr/lib/python3.9/zipimport.py
    loaded_modules = set()

    with open(log_file) as f:
        for line in f:
            if "# code object from" not in line:
                continue

            parts = line.split("# code object from", 1)
            if len(parts) != 2:
                continue

            module_path = parts[1].strip()
            loaded_modules.add(module_path)

    return list(loaded_modules)


def parse_node_verbose_log(log_file: str) -> list[str]:
    # Parse Node.js module debug logs
    # MODULE X: load "/path/to/module.js" for module "/path/to/module.js"
    loaded_modules = set()

    with open(log_file) as f:
        for line in f:
            # Change from specific "MODULE 1:" to any MODULE number
            if not line.strip().startswith("MODULE ") or ": load " not in line:
                continue

            # Extract the module path between quotes after "load"
            parts = line.split("load ", 1)
            if len(parts) != 2:
                continue

            # Find the first quoted path
            start_quote = parts[1].find('"')
            if start_quote == -1:
                continue

            end_quote = parts[1].find('"', start_quote + 1)
            if end_quote == -1:
                continue

            module_path = parts[1][start_quote + 1 : end_quote]

            # Skip built-in modules
            if (
                module_path.startswith("node:")
                or module_path == "fs"
                or module_path == "path"
            ):
                continue

            loaded_modules.add(module_path)

    return list(loaded_modules)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Parse verbose logs from Java, Python, or Node.js"
    )
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument(
        "--type",
        choices=["java", "python", "node"],
        required=True,
        help="Type of log file (java, python, or node)",
    )

    args = parser.parse_args()

    if args.type == "java":
        files = parse_java_verbose_log(args.log_file)
    elif args.type == "python":
        files = parse_python_verbose_log(args.log_file)
    elif args.type == "node":
        files = parse_node_verbose_log(args.log_file)
    else:
        raise ValueError(f"Unknown log type: {args.type}")

    for file in sorted(files):
        print(file)
