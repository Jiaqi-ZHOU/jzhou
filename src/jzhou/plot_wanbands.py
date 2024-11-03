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
from .plot_xmlwanbands import get_wan_data


def plot_wan_bands(wanfile, wanfile2, fakefermi=0):


    plt.subplots(figsize=(4, 3), dpi=300)

    # If a fakefermi has to be given, fakefermi=0 is also okay. 

    def plot_wan_bands_single(fermi, wanfile, color, linestyle):
        wan_kpt, wan_eig, WT = get_wan_data(wanfile)
        plt.plot(wan_kpt, wan_eig - fermi, color=color, linestyle = linestyle, linewidth=1)

        if WT == False:
            plt.plot(0, 0, color=color, linestyle = linestyle,  linewidth=1, label=r"W90")
        elif WT == True:
            plt.plot(0, 0, color=color, linestyle = linestyle,  linewidth=1, label=r"WTools")

        if fermi != 0:
            plt.ylabel(r"$\mathregular{E - {E}_{F}}$ (eV)", fontsize=fontsizes.label)
            plt.hlines(
                0, min(wan_kpt), max(wan_kpt), color="gray", linestyle="-", linewidth=0.5
            )
            plt.ylim(-3, 3)
        else:
            plt.ylabel(r"Energy (eV)", fontsize=fontsizes.label)
            # plt.hlines(
            #     0,
            #     min(wan_kpt),
            #     max(wan_kpt),
            #     color="gray",
            #     linestyle="-",
            #     linewidth=0.5,
            # )
            # plt.ylim( - 3,  + 3)
        plt.xlim(min(wan_kpt)  , max(wan_kpt))


    if wanfile2 != None:
        plot_wan_bands_single(fermi=fakefermi, wanfile=wanfile, color=colors.blue, linestyle="-")
        plot_wan_bands_single(fermi=fakefermi, wanfile=wanfile2, color=colors.red, linestyle=":")
    else:
        plot_wan_bands_single(fermi=fakefermi, wanfile=wanfile, color=colors.blue, linestyle="-")

    plt.tick_params(axis="x", which="both", direction="in")
    plt.tick_params(axis="y", which="both", direction="in")

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc="upper right")
    # ax.legend(handles[::-1], labels[::-1], loc="upper right")
    plt.tight_layout()
    plt.show()
