#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from ase.units import Bohr
from ase.units import Ha
from ase.units import Ry
from lxml import etree
import argparse


from .constant import fontsizes, colors
from .plot_vaspbands import get_kpath_bands, get_fermi, xticks 


def get_wan_data(wannier_dat):
    # fig, ax = plt.subplots(figsize=(4, 3), dpi=300)

    # To plot Wannier lines plt.plot
    file = open(wannier_dat)

    # The output of open() is seperated string for every line
    seperated_str = file.readlines()

    seperated_str = [line for line in seperated_str if not line.strip().startswith('#')]

    # Combine all string to be one long string
    combined_long_str = "".join(seperated_str)

    # For QE Grbands.dat.gnu: '\n \n' is a marker to split different blocks (one blank)
    # split_block = combined_long_str.split('\n \n')

    # For wannier: '\n  \n' is a marker to split different blocks (two blanks)
    split_block = combined_long_str.split("\n  \n")
    # Every block is a band
    # Note split_block is a list consisting of strings, and
    # The length of split_block is nbnd(nwann) + 1, 1 is due to the last blank
    # The length of every element of split_block, i.e., a string, is MEANINGLESS, NOT the number of values, since it is a STR type.

    # Convert every string into an array to obtain the value
    # '_' is a name to denote a quanlity I don't want to name it since the name is useless anymore
    # 'if _' is to delete the last blank.
    # If not none (a block of band), do it. If none (a blank), not do.

    split_block_list_of_array = [np.fromstring(_, sep=" ") for _ in split_block if _]

    # Wannier90 generate prefix_band.dat including 2 columns. 
    # WannierTools generate bulkek.dat including 3 columns. 
    # I need to tell the code which is the case. 
    WT=None
    with open(wannier_dat, "r") as file:
        lines = file.readlines()
        # ['#', 'klen', 'E', '|', 'projection', '|group', '1:', 'A', '|group']
        if len(lines[0].split()) == 9:
            n = 3
            WT=True
        else:
            n = 2
            WT=False

    # Convert the list to array by adding one dimension (the number of nbnd(nwann))
    nbnd_kpt_energy = np.array(split_block_list_of_array)
    # The shape of nbnd_kpt_energy is (nbnd, nkpt_coor+nenergy)
    # Note nbnd(nwann) is useless information
    # The kpt_coor is the even line of the 2nd dimension
    # The energy is the odd line of the 2nd dimension


    wan_kpt = nbnd_kpt_energy[0, 0::n]
    wan_eig = nbnd_kpt_energy[:, 1::n]

    wan_eig = wan_eig.T  # For plotting

    return wan_kpt, wan_eig, WT

def plot_vasp_wan_bands(dirname, wanfile, wanfile2, fakefermi=None):

    realfermi = get_fermi(dirname)
    kpath, bands = get_kpath_bands(dirname)
    print("Fermi energy is {:.4f}".format(realfermi) + " eV.")
    print("kpath_len = ", len(kpath))
    print("bands.shape = ", bands.shape)
    plt.subplots(figsize=(4, 3), dpi=300)

    # If a fakefermi is not given, we use the real fermi to plot bands,
    # and the realfermi is extracted from eigenvales.
    if fakefermi == None:
        fermi = realfermi
        plt.ylabel(r"$\mathregular{E - {E}_{F}}$ (eV)", fontsize=fontsizes.label)
        plt.hlines(
            0, min(kpath), max(kpath), color="gray", linestyle="-", linewidth=0.5
        )
        plt.ylim(-1.6, 1.6)
        plt.ylim(-2, 2)

    # If a fakefermi is given (probably as 0), I will want to
    # mark the position of real fermi.
    else:
        fermi = fakefermi
        plt.ylabel(r"Energy (eV)", fontsize=fontsizes.label)
        plt.hlines(
            realfermi,
            min(kpath),
            max(kpath),
            color="gray",
            linestyle="-",
            linewidth=0.5,
        )
        plt.ylim(realfermi - 3, realfermi + 3)

    nbnd = bands.shape[1]
    plt.xlim(min(kpath), max(kpath))
    DFTs = 10
    for i in range(nbnd):
        if i == 0:
            plt.scatter(
                kpath,
                bands[:, i] - fermi,
                s=DFTs,
                facecolors="none",
                edgecolors=colors.green,
                label=r"DFT",
            )
        else:
            plt.scatter(
                kpath,
                bands[:, i] - fermi,
                s=DFTs,
                facecolors="none",
                edgecolors=colors.green,
            )
    print("nbnd = " + str(nbnd))
    print("kpt_len = " + str(kpath.shape[0]))
    tick_locs_list, tick_labels_list = xticks(dirname)
    print("High-symm kpoints are ", tick_labels_list )
    for n in range(1, len(tick_locs_list)):
        plt.plot(
            [tick_locs_list[n], tick_locs_list[n]],
            [plt.ylim()[0], plt.ylim()[1]],
            color="gray",
            linestyle="-",
            linewidth=0.5,
        )
    plt.xticks(tick_locs_list, tick_labels_list)

    def plot_wan_bands(fermi, wanfile, color, linestyle):
        wan_kpt, wan_eig, WT = get_wan_data(wanfile)
        plt.plot(wan_kpt, wan_eig - fermi, color=color, linestyle = linestyle, linewidth=1)

        if WT == False:
            plt.plot(1e8, 1e8, color=color, linestyle = linestyle,  linewidth=1, label=r"W90")
        elif WT == True:
            plt.plot(1e8, 1e8, color=color, linestyle = linestyle,  linewidth=1, label=r"WTools")

    if wanfile2 != None:
        plot_wan_bands(fermi=fermi, wanfile=wanfile, color=colors.blue, linestyle="-")
        plot_wan_bands(fermi=fermi, wanfile=wanfile2, color=colors.red, linestyle=":")
    else:
        plot_wan_bands(fermi=fermi, wanfile=wanfile, color=colors.blue, linestyle="-")

    plt.tick_params(axis="x", which="both", direction="in")
    plt.tick_params(axis="y", which="both", direction="in")

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc="upper right")
    # ax.legend(handles[::-1], labels[::-1], loc="upper right")
    plt.tight_layout()
    # plt.savefig("xmlwanbands.png")
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Compare vasp bands (dirname providing EIGENVAL, KPOINTS, POSCAR, OUTCAR) and Wannier bands (dat). \
    The fakefermi is alternative (to set EF=0). "
    )
    parser.add_argument(
        "--dirname",
        default="./",
        type=str,
        help="The dirname providing EIGENVAL, KPOINTS, POSCAR, OUTCAR, default is './'"
    )
    parser.add_argument(
        "--wanfile",
        default="aiida_band.dat",
        type=str,
        help="The Wannier dat file, default is aiida_band.dat",
    )
    parser.add_argument(
        "--wanfile2",
        default="bulkek.dat",
        type=str,
        help="The Wannier dat file, default is bulkek.dat",
    )
    parser.add_argument(
        "--fakefermi", type=float, help="The fake Fermi energy value given in command"
    )
    args = parser.parse_args()
    print("DFT bands is given by the dirname", args.dirname)
    print("Wan bands is given by", args.wanfile)
    print("Another wan bands is given by", args.wanfile2)

    if args.fakefermi:
        print("A given Fermi energy =", args.fakefermi)
        plot_vasp_wan_bands(filename=args.file, fakefermi=args.fakefermi)
        # find_occ_nbnd(filename=args.file)
    else:
        print("Fermi energy is given by bands OUTCAR file. ")
        plot_vasp_wan_bands(filename=args.file, fakefermi=None)
        # find_occ_nbnd(filename=args.file)
