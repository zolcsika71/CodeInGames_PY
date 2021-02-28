import sys
import pathlib

if len(sys.argv) < 2:
    print(f'Error, expected which file to build', file=sys.stderr, flush=True)
    exit()

output_file = "cg.py"
input_file = sys.argv[1]
path = str(pathlib.Path().absolute()) + '\\'


def parse_import(line):
    f_loc = ''
    line_args = line.strip().split()
    for i, w in enumerate(line_args):
        if w == 'from':
            f_loc = line_args[i + 1]
            break
    f_loc = [t for t in f_loc.split('.') if len(t) > 0]
    f_loc = '/'.join(f_loc) + '.py'
    f_loc = '../' + f_loc
    return f_loc


def flush_imports(o_stream, import_files):
    for file in import_files:
        main.is_importing = False
        with open(file, 'r') as f_in:
            for line in f_in:
                line_args = line.split()
                # Ignore imports in sub_files
                if len(line_args) > 0 and (line_args[0] == 'from' or line_args[0] == 'import'):
                    pass
                elif line.strip() == "# IMPORT":
                    # Start import
                    main.is_importing = True
                elif line.strip() == "# END_IMPORT":
                    # Stop import
                    main.is_importing = False
                else:
                    o_stream.write(line)


def main():
    is_importing = False
    imported_files = []
    with open(path + output_file, 'w') as f_out:
        with open(path + input_file, 'r') as f_in:
            for line in f_in:
                if line.strip() == "# IMPORT":
                    # Start import
                    is_importing = True
                elif line.strip() == "# END_IMPORT":
                    # Stop import
                    is_importing = False
                    flush_imports(f_out, imported_files)
                    f_out.write('\n')
                elif is_importing:
                    line_args = line.split()
                    if len(line_args) > 0 and (line_args[0] == 'from' or line_args[0] == 'import'):
                        imported_files.append(parse_import(line))
                else:
                    f_out.write(line)


main()
