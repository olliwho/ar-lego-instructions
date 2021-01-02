import sys
import time

from fileParser import *
from fileWriter import *


def main():
    """
    main, reads an  instruction file from the command line and creates .obj
    files out of it
    """

    lds_file_path = sys.argv[1]

    if not os.path.isfile(lds_file_path):
        print(lds_file_path + " is not a valid input file!")
        return

    model_name = os.path.split(lds_file_path)[-1].replace(".ldr", "").replace(".mpd", "")
    asset_path = os.path.join("..\ARLI\Assets\Models", model_name)

    # asset_path = os.path.join(os.path.curdir, "..", "test")
    if not os.path.isdir(asset_path):
        os.mkdir(asset_path)

    if lds_file_path.endswith(".mpd"):
        lds_file_path = split_mpd_file(lds_file_path)

    bricks_per_step = parse_manual(lds_file_path)
    # if there are no steps (just one) we split it and make every brick an extra step
    if len(bricks_per_step) == 1:
        bricks_per_step = [[bricks_per_step[0][i]] for i in range(len(bricks_per_step[0]))]

    # add model name to models lists
    with open(os.path.join(os.path.dirname(asset_path), "models.txt"), "r+") as models_file:
        content = models_file.read()
        if content.find(model_name) == -1:
            models_file.writelines(["\n", model_name])
    printed_bricks = []

    def get_steps(original_list):
        rec_bps = []
        for step in original_list:
            temp = []
            for br in step:
                if len(br.steps) != 0:
                    temp.append(get_steps(br.steps))
                else:
                    temp.append(br)
            rec_bps.append(temp)

        return rec_bps

    bps_new = get_steps(bricks_per_step)

    print(bricks_per_step)
    print(bps_new)
    print(unnest(bps_new))

    bricks_per_step = unnest(bps_new)

    for step_num, bricks in enumerate(bricks_per_step):
        output_file_name = model_name + "_step" + str(step_num) + ".obj"
        lines, triangles, quads = [], [], []

        for brick in bricks:
            all_bricks = simplify(brick.get_bricks_rec())
            # print(all_bricks)
            for b in all_bricks:
                # print(b.position)
                lines.append(b.lines)
                triangles.append(b.triangles)
                quads.append(b.quads)

            # if brick.file not in printed_bricks:
            #     printed_bricks.append(brick.file)

        write_step_file(output_file_name, asset_path, simplify(lines), simplify(triangles), simplify(quads))
        # print('-----------')
        del lines, triangles, quads

    write_color_mtl(asset_path)
    write_file(model_name, asset_path)


    # for showing bricks per step, maybe in the future
    # for brick_name in printed_bricks:
    #     brick = Brick(Color(0), Point(0.0, 0.0, 0.0), rotate(Matrix4x4.identity()), brick_name)
    #     all_bricks = simplify(brick.get_bricks_rec())
    #     lines, triangles, quads = [], [], []
    #     for b in all_bricks:
    #         lines.append(b.lines)
    #         triangles.append(b.triangles)
    #         quads.append(b.quads)
    #     write_step_file(brick_name.replace(".dat", ".obj"), asset_path, simplify(lines), simplify(triangles), simplify(quads))
    #     del lines, triangles, quads

    # # write step info file
    # step_bricks = []
    # for step in bricks_per_step:
    #     bricks = []
    #     for b in step:
    #         if b.file not in bricks:
    #             bricks.append(b.file)
    #     step_bricks.append(bricks)
    #     del bricks
    # print(step_bricks)
    # write_step_info(model_name + "_step_info.txt", asset_path, step_bricks)
    # del bricks_per_step[:]


def split_mpd_file(mdp_file_path):
    """
    splits the mdp file in individual model files
    @param mdp_file_path: path of the original mpd file
    @return: path of the first file to start with
    """

    start_file = ""
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
                filename = " ".join(line.split(" ")[2:]).replace("\n", "").lower()
                if not start_file:
                    start_file = "../models/" + filename
            lines += line
            line = f.readline()

        with open("../models/" + filename, "w") as of:
            of.write(lines)
            of.flush()

    return start_file


def simplify(lists):
    """
    simplifies a nested list of lists
    @param lists: the list that has to be simplified
    @return: the simplified list
    """
    items = []
    ty = type(lists)
    if ty == Brick or ty == Line or ty == Triangle or ty == Quad:
        return [lists]
    for i in lists:
        items += simplify(i)
    return items


def unnest(olist):
    """
    unnests an recursive list of bricks_per_step
    @param olist: original list to unnest
    @return: list containing lists sontaining bricks for this step
    """
    flat = []
    step = []
    for item in olist:
        if isinstance(item, list) and not any(isinstance(i, list) for i in item):
            flat.append(item)
        else:
            # print(flat)
            # print(item)
            if type(item) == Brick:
                step.append(item)
            else:
                if len(step) > 0:
                    flat.append(step)
                    step = []
                flat += unnest(item)
    if len(step) > 0:
        flat.append(step)
    return flat


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Elapsed time: " + str(round((end-start)/60.0, 3)) + " minutes (" + str(round((end-start), 3)) + " seconds)")
