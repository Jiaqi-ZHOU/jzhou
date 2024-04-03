#!/usr/bin/env python3
import numpy as np
import os
import matplotlib.pyplot as plt
import argparse
from ase.units import Bohr

labelfont = 10
tickfont = 8


def read_file(file_path):
    try:
        data = np.loadtxt(file_path)
        # with open(file_path, 'r') as file:
        #     file_contents = file.read()
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def read_win(winfile):
    with open(winfile, "r") as file:
        lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i]
        _ = line.split()
        if len(_) == 4:
            if _[1] == "VBM":
                VBM = float(_[-1])
            elif _[1] == "CBM":
                CBM = float(_[-1])
            # break
        elif len(_) == 2:
            if _[0] == "Begin" and _[1] == "Unit_Cell_Cart":
                unit = 1
                if lines[i + 1] == "bohr" or "Bohr":
                    unit = Bohr
                c = float(lines[i + 4].split()[-1]) * unit

                # break

    return VBM, CBM, c


def plot(data, clength, fermi, CBM=None):
    factor = 8.2164718e-05 * clength * 2 * np.pi
    e = data[:, 1] - fermi
    shc_e2h = data[:, 2] * factor

    plt.figure(figsize=(3, 6), dpi=300)  # plt.figure  should be at this location
    plt.plot(shc_e2h, e, color="royalblue", linewidth=1)

    minshc = np.min(shc_e2h)
    maxshc = np.max(shc_e2h)
    # If abs(shc) is too small, I set [-2.2, 2.2] as xlim.
    if minshc > -2:
        minshc = -2.2
    if maxshc < 2:
        maxshc = 2.2
    if minshc < -10:
        minshc = -5
    if maxshc > 10:
        maxshc = 5
    factor = 1.1
    plt.xlim([minshc * factor, maxshc * factor])
    plt.ylim(-2, 2)
    plt.hlines(
        0, plt.xlim()[0], plt.xlim()[1], linestyles="--", linewidth=0.5, colors="grey"
    )
    if CBM:
        plt.hlines(
            CBM - fermi,
            plt.xlim()[0],
            plt.xlim()[1],
            linestyles="--",
            linewidth=0.5,
            colors="grey",
        )
    plt.vlines(
        -1, plt.ylim()[0], plt.ylim()[1], linestyles="--", linewidth=0.5, colors="grey"
    )
    plt.vlines(
        0, plt.ylim()[0], plt.ylim()[1], linestyles="--", linewidth=0.5, colors="grey"
    )
    plt.vlines(
        1, plt.ylim()[0], plt.ylim()[1], linestyles="--", linewidth=0.5, colors="grey"
    )
    plt.text(plt.xlim()[0], 0, "VBM", fontsize=labelfont)
    plt.text(plt.xlim()[0], CBM - fermi, "CBM", fontsize=labelfont)
    plt.ylabel(r"$\mathrm{E - {E}_{F}}$ (eV)", fontsize=labelfont)
    plt.xlabel(r"SHC [$(\hbar/2e){e^2}/h$]", fontsize=labelfont, labelpad=0.2)

    plt.xticks(fontsize=tickfont)
    plt.yticks(fontsize=tickfont)
    plt.tick_params(axis="x", which="both", direction="in")
    plt.tick_params(axis="y", which="both", direction="in")

    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Plot shc v.s. energy. shc.dat is mandatory. win is alternative. ")
    parser.add_argument(
        "--file",
        default="aiida-shc-fermiscan.dat",
        type=str,
        help="The shc dat file, default is aiida-shc-fermiscan.dat",
    )
    parser.add_argument(
        "--win",
        default="aiida.win",
        type=str,
        help="The win input, default is aiida.win",
    )
    parser.add_argument("--fermi", type=float, help="The Fermi energy")
    parser.add_argument("--clength", type=float, help="The cell c length in ang")
    parser.add_argument("--CBM", type=float, help="The CBM of semiconductor")

    args = parser.parse_args()
    data = read_file(args.file)
    print("shc.dat file is given by", args.file)

    if args.win:
        print("win file is given by", args.win)
        VBM, CBM, c = read_win(args.win)
        fermi = VBM
        clength = c
        plot(data, clength, fermi, CBM=CBM)

    else:
        fermi = args.fermi
        clength = args.clength
        if args.CBM:
            plot(data, clength, fermi, CBM=args.CBM)
        else:
            plot(data, clength, fermi, CBM=None)

        # if file_contents:
        #     print(f"File contents of '{args.file}':")
        #     print(file_contents)


if __name__ == "__main__":
    main()
