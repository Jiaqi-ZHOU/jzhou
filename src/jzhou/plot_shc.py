#!/usr/bin/env python3
import numpy as np
import os
import matplotlib.pyplot as plt
import argparse
from ase.units import Bohr
import matplotlib

matplotlib.rcParams["font.family"] = "STIXGeneral"
matplotlib.rcParams["font.serif"] = "STIXGeneral"
matplotlib.rcParams["mathtext.fontset"] = "stix"

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
    VBM = None
    CBM = None
    for i in range(len(lines)):
        line = lines[i].strip()
        _ = line.split()
        if "VBM " in line:
            VBM = float(_[-1])
        elif "CBM " in line:
            CBM = float(_[-1])
        elif "fermi_energy " in line:
            fermi = float(_[-1])
        # print(VBM, CBM)
        
        # _ = line.split()
        if len(_) == 2:
            if _[0].lower() == "begin" and _[1].lower() == "unit_cell_cart":
                unit_str = lines[i + 1].lower().replace("\n", "")
                # print( lines[i + 1].lower().replace("\n", "") == "bohr" )
                if unit_str == "bohr":
                    unit = Bohr
                    c = float(lines[i + 4].split()[-1]) * unit
                elif unit_str == "ang": 
                    unit = 1
                    c = float(lines[i + 4].split()[-1]) * unit
                else:   # No line for unit 
                    unit = 1
                    c = float(lines[i + 3].split()[-1]) * unit
    if VBM is None and CBM is None: 
        VBM = 0
        CBM = 0 

    return fermi, VBM, CBM, c


def plot(data, clength, fermi, vbm, cbm=None):
    factor = 8.2164718e-05 * clength * 2 * np.pi
    e = data[:, 1] - fermi
    shc_e2h = data[:, 2] * factor
    shc_max_idx = np.argmax(shc_e2h)
    print("max shc = ", str(shc_e2h[shc_max_idx]) + " at E = " + str(e[shc_max_idx]))

    fig = plt.figure(figsize=(1.7, 3), dpi=144)  # plt.figure  should be at this location
    plt.plot(shc_e2h, e, color="blue", linewidth=1.5)

    minshc = np.min(shc_e2h)
    maxshc = np.max(shc_e2h)
    # If abs(shc) is too small, I set [-2.2, 2.2] as xlim.
    # if minshc > -2:
    #     minshc = -2.2
    # if maxshc < 2:
    #     maxshc = 2.2
    # if minshc < -10:
    #     minshc = -5
    # if maxshc > 10:
    #     maxshc = 5
    factor = 1.1
    plt.xlim([minshc * factor, maxshc * factor])
    # plt.xlim(-0.2, 4.5)
    plt.ylim(-1.6, 1.6)
    plt.hlines(
        0, plt.xlim()[0], plt.xlim()[1], linestyles="--", linewidth=0.5, colors="grey"
    )
    if cbm:
        plt.hlines(
            cbm - fermi,
            plt.xlim()[0],
            plt.xlim()[1],
            linestyles="--",
            linewidth=0.5,
            colors="grey",
        )
    # plt.vlines(
    #     -1, plt.ylim()[0], plt.ylim()[1], linestyles="--", linewidth=0.5, colors="grey"
    # )
    plt.vlines(
        0, plt.ylim()[0], plt.ylim()[1], linestyles="--", linewidth=0.5, colors="grey"
    )
    # plt.vlines(
    #     4, plt.ylim()[0], plt.ylim()[1], linestyles="--", linewidth=0.5, colors="grey"
    # )
    # If this is a semiconductor:
    if cbm > vbm:
        plt.text(0, 0, "VBM", fontsize=labelfont)
        plt.text(0, cbm - vbm, "CBM", fontsize=labelfont)
    plt.ylabel(r"$\mathrm{E - {E}_{F}}$ (eV)", fontsize=labelfont)
    plt.xlabel(r"SHC [$(\hbar/2e){e^2}/h$]", fontsize=labelfont-1, labelpad=0.2)

    # plt.xticks([0, 4], [0, 4], fontsize=tickfont)
    plt.yticks(fontsize=tickfont)
    plt.tick_params(axis="x", which="both", direction="in")
    plt.tick_params(axis="y", which="both", direction="in")
    plt.tight_layout()
    # fig.subplots_adjust()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Plot shc v.s. energy. shc.dat is mandatory. win is mandatory. ")
    parser.add_argument(
        "--file",
        default="aiida-shc-fermiscan.dat",
        type=str,
        help="The shc data file, default is aiida-shc-fermiscan.dat",
    )
    parser.add_argument(
        "--win",
        default="aiida.win",
        type=str,
        help="The Wannier input, default is aiida.win.",
    )

    args = parser.parse_args()
    data = read_file(args.file)
    print("shc.dat file is given by", args.file)

    print("win file is given by", args.win)
    fermi, vbm, cbm, c = read_win(args.win)
    if vbm != 0:
        fermi = vbm
    else:
        fermi = fermi
    clength = c
    plot(data, clength, fermi, vbm, cbm=cbm)


if __name__ == "__main__":
    main()
