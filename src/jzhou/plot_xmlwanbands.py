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
from .plot_xmlbands import extract_band_weight_xml


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

def find_occ_nbnd(xmlfile, wanfile):
    wan_kpt, wan_eig, WT = get_wan_data(wanfile)
    kpt_frac, kpath, bands, realfermi = extract_band_weight_xml(xmlfile)
    nbnd = wan_eig.shape[1]
    ib = []
    for i in range(nbnd):
        # print(wan_eig[:, i].all())
        if np.all(wan_eig[:, i] < realfermi + 0.025):
           ib.append(i)
    occ_nbnd = int(max(ib)) + 1
    print(f"{occ_nbnd=}")

def plot_xml_wan_bands(xmlfile, wanfile, wanfile2, fakefermi=None):

    kpt_frac, kpath, bands, realfermi = extract_band_weight_xml(xmlfile)
    print("Fermi energy in xml is {:.4f}".format(realfermi) + " eV.")

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

    nbnd = bands.shape[0]
    plt.xlim(min(kpath), max(kpath))
    DFTs = 10
    for i in range(nbnd):
        if i == 0:
            plt.scatter(
                kpath,
                bands[i, :] - fermi,
                s=DFTs,
                facecolors="none",
                edgecolors=colors.green,
                label=r"DFT",
            )
        else:
            plt.scatter(
                kpath,
                bands[i, :] - fermi,
                s=DFTs,
                facecolors="none",
                edgecolors=colors.green,
            )

    nk = kpt_frac.shape[1]
    tick_locs_list = []
    tick_labels_list = []
    thr = 1e-2/2
    ky = 0.57735027 
    for i in range(nk):
        if np.linalg.norm(kpt_frac[:, i]) < thr:
            G_loc = kpath[i]
            tick_locs_list.append(G_loc)
            tick_labels_list.append(r"$\mathregular{\Gamma}$")
        if np.linalg.norm(kpt_frac[:, i] - np.array([0.5, ky/2, 0])) < thr or np.linalg.norm(kpt_frac[:, i] - np.array([0, ky, 0])) < thr:
            M_loc = kpath[i]
            tick_locs_list.append(M_loc)
            tick_labels_list.append("M")
        if np.linalg.norm(kpt_frac[:, i] - np.array([1 / 3, ky, 0])) < thr  or  np.linalg.norm(kpt_frac[:, i] - np.array([2/ 3, 0, 0])) < thr:
            K_loc = kpath[i]
            tick_locs_list.append(K_loc)
            tick_labels_list.append("K")
    # For alphaBi
    # nk = kpt_frac.shape[1]
    # tick_locs_list = []
    # tick_labels_list = []
    # thr = 5e-3
    # kx = 0.5
    # ky = 4.664826304030108E-001
    # for i in range(nk):
    #     if np.linalg.norm(kpt_frac[:, i]) < thr:
    #         G_loc = kpath[i]
    #         tick_locs_list.append(G_loc)
    #         tick_labels_list.append(r"$\mathregular{\Gamma}$")
    #     if np.linalg.norm(kpt_frac[:, i] - np.array([kx, 0, 0])) < thr or np.linalg.norm(kpt_frac[:, i] - np.array([kx, 0, 0])) < thr:
    #         X_loc = kpath[i]
    #         tick_locs_list.append(X_loc)
    #         tick_labels_list.append("X")
    #     if np.linalg.norm(kpt_frac[:, i] - np.array([0, ky, 0])) < thr or np.linalg.norm(kpt_frac[:, i] - np.array([0, ky, 0])) < thr:
    #         Y_loc = kpath[i]
    #         tick_locs_list.append(Y_loc)
    #         tick_labels_list.append("Y")
    #     if np.linalg.norm(kpt_frac[:, i] - np.array([kx, ky, 0])) < thr:
    #         M_loc = kpath[i]
    #         tick_locs_list.append(M_loc)
    #         tick_labels_list.append("M")

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
    plt.savefig("xmlwanbands.png")
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Compare QE bands (xml) and Wannier bands (dat). \
    xml and dat files are mandatory. \
    The fakefermi is alternative (to set EF=0). "
    )
    parser.add_argument(
        "--xmlfile",
        default="aiida.xml",
        type=str,
        help="The bands xml file, default is aiida.xml",
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
    print("DFT bands is given by", args.xmlfile)
    print("Wan bands is given by", args.wanfile)
    print("Another wan bands is given by", args.wanfile2)

    if args.fakefermi:
        print("A given Fermi energy =", args.fakefermi)
        plot_xml_wan_bands(filename=args.file, fakefermi=args.fakefermi)
        # find_occ_nbnd(filename=args.file)
    else:
        print("Fermi energy is given by xml file. ")
        plot_xml_wan_bands(filename=args.file, fakefermi=None)
        # find_occ_nbnd(filename=args.file)
