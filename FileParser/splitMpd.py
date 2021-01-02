import sys

def main():
    """
    main, reads an  instruction file from the command line and creates .obj
    files out of the instruction
    """
    mdp_file_path = sys.argv[1]

    with open(mdp_file_path) as f:
        lines = ""
        filename = ""
        line = f.readline()
        while line:
            if line.startswith("0 FILE"):
                if lines:
                    with open("../models/"+filename, "w") as of:
                        of.write(lines)
                        of.flush()
                lines = ""
                filename = " ".join(line.split(" ")[2:]).replace("\n", "")
            lines += line
            line = f.readline()

        with open("../models/" + filename, "w") as of:
            of.write(lines)
            of.flush()


if __name__ == '__main__':
    main()
