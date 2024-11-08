#!/usr/bin/env python3
import argparse

from ase.units import Bohr, Ha, Ry
from lxml import etree
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import numpy as np

from .constant import colors, fontsizes
from .plot_xmlwanbands import get_wan_data


def plot_wan_bands(wanfile, wanfile2, fakefermi=0):

    plt.subplots(figsize=(4, 3), dpi=144)

    # If a fakefermi has to be given, fakefermi=0 is also okay.

    def plot_wan_bands_single(fermi, wanfile, color, linestyle):
        wan_kpt, wan_eig, WT = get_wan_data(wanfile)
        plt.plot(
            wan_kpt, wan_eig - fermi, color=color, linestyle=linestyle, linewidth=1
        )
        plt.plot(
            0,
            0,
            color=color,
            linestyle=linestyle,
            linewidth=1,
            label=r"WTools" if WT else r"W90",
        )

        if fermi != 0:
            plt.ylabel(r"$\mathregular{E - {E}_{F}}$ (eV)", fontsize=fontsizes.label)
            plt.hlines(
                0,
                min(wan_kpt),
                max(wan_kpt),
                color="gray",
                linestyle="-",
                linewidth=0.5,
            )
            plt.ylim(-3, 3)
        else:
            plt.ylabel(r"Energy (eV)", fontsize=fontsizes.label)
        plt.xlim(min(wan_kpt), max(wan_kpt))

    plot_wan_bands_single(
        fermi=fakefermi, wanfile=wanfile, color=colors.blue, linestyle="-"
    )
    if wanfile2:
        plot_wan_bands_single(
            fermi=fakefermi, wanfile=wanfile2, color=colors.red, linestyle=":"
        )

    plt.tick_params(axis="x", which="both", direction="in")
    plt.tick_params(axis="y", which="both", direction="in")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()
