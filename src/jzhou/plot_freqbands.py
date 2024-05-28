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

def plot_freq_bands(filename):

    plt.figure(figsize=(4,3),dpi=300)
    data = np.loadtxt(filename)
    path = data[:, 0]
    nband = data.shape[1] - 1
    for i in range(1,nband+1):
        plt.plot(path, data[:, i], color='k', linewidth = 1)
    emin = np.min(data[:, 1:])
    emax = np.max(data[:, 1:])
    fact = 1.1
    plt.xlim(min(path), max(path))
    plt.ylim(emin* fact, emax * fact)
    plt.ylabel(r"Freq (cm$^{-1}$)", fontsize=fontsizes.label)
    nq = 40
    xlabels = ["M", r"$\mathregular{\Gamma}$", "K", "M"]
    xlocs = [path[i * nq]  for i in range(len(xlabels))]
    plt.xticks(xlocs, xlabels, fontsize=fontsizes.tick)
    plt.yticks(fontsize=fontsizes.tick)
    plt.tick_params(axis="x", which="both", direction="in")
    plt.tick_params(axis="y", which="both", direction="in")
    for x in xlocs:
        plt.vlines(x, plt.ylim()[0], plt.ylim()[1], colors=colors.grey, linewidth=0.5, linestyles='-')
    plt.hlines(0, min(path), max(path), colors=colors.grey, linewidth=0.5, linestyles='-')
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Compare QE bands (xml) and Wannier bands (dat). \
    xml and dat files are mandatory. \
    The fakefermi is alternative (to set EF=0). "
    )
    parser.add_argument(
        "--freqfile",
        type=str,
        help="The QE freq.gp file, default is aiida.freq.gp. ",
    )

    args = parser.parse_args()
    print("QE freq bands is given by", args.freqfile)

    plot_freq_bands(filename=args.freqfile)