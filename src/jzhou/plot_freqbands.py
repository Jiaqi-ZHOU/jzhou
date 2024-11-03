#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from ase.units import Bohr
from ase.units import Ha
from ase.units import Ry
from lxml import etree
import argparse
import matplotlib

matplotlib.rcParams["font.family"] = "STIXGeneral"
matplotlib.rcParams["font.serif"] = "STIXGeneral"
matplotlib.rcParams["mathtext.fontset"] = "stix"


from .constant import fontsizes, colors


def get_freq_data(filename):
    file = open(filename)
    line_info = file.readline()
    nbnd = int(line_info.split()[2].split(",")[0])
    nks = int(line_info.split()[-2])
    kpts = np.zeros((nks, 3))
    freq = np.zeros((nks, nbnd))

    for i in range(nks):
        kpts[i, :] = np.fromstring(file.readline().strip(), sep=" ")
        freq_k = []
        # Check if enough freq data have been read
        # If not, read another line,
        # until nbnd freq data have been read
        while len(freq_k) < nbnd:
            line = file.readline()
            freq_k.extend(float(i) for i in line.strip().split())
        freq[i, :] = freq_k

    return kpts, freq


def gen_plot_data(filename):
    kpts, freq = get_freq_data(filename)

    distances = []
    for i in range(1, kpts.shape[0]):
        distance = np.linalg.norm(kpts[i, :] - kpts[i - 1, :])  # Euclidean distance
        distances.append(distance)
    path = [0]
    path.extend(np.cumsum(distances))

    # nk x nbnd + 1
    path_freq = np.zeros((kpts.shape[0], freq.shape[1] + 1))
    path_freq[:, 0] = path
    path_freq[:, 1:] = freq

    return path_freq


def plot_freq_bands(filename):

    path_freq = gen_plot_data(filename)
    path = path_freq[:, 0]
    nbnd = path_freq.shape[1] - 1

    plt.figure(figsize=(4, 3), dpi=144)
    for i in range(1, nbnd + 1):
        plt.plot(path, path_freq[:, i], color="k", linewidth=1)

    emin = np.min(path_freq[:, 1:])
    emax = np.max(path_freq[:, 1:])
    dist = 10
    plt.xlim(min(path), max(path))
    plt.ylim(emin - dist, emax + dist)
    plt.xlabel(r"q-path", fontsize=fontsizes.label)
    plt.ylabel(r"Frequency (cm$^{-1}$)", fontsize=fontsizes.label)
    if "phband.freq" in filename:
        plt.ylabel(r"$\omega$ (meV)", fontsize=fontsizes.label)
    plt.xticks([])
    plt.yticks(fontsize=fontsizes.tick)
    plt.tick_params(axis="x", which="both", direction="in")
    plt.tick_params(axis="y", which="both", direction="in")
    plt.hlines(
        0, min(path), max(path), colors=colors.grey, linewidth=0.5, linestyles="-"
    )
    plt.tight_layout()
    # plt.savefig("phonon.png")
    plt.show()


def parse_matdyn(matdyn):
    # matdyn = "matdyn.in"
    file = open(matdyn)
    # lines = file.readlines()
    while True:
        line = file.readline().strip()
        if line.isdigit():
            nq_highsym = int(line)
            break
    qpts = np.zeros((nq_highsym, 3))
    qlabels = []
    for i in range(nq_highsym):
        line = file.readline().strip().split()
        qpt = np.array(line[0:3], dtype=float)
        qpts[i, :] = qpt
        # Replace G by Gamma if found
        qlabels.append(line[-1].replace("G", r"$\mathregular{\Gamma}$"))

    return qpts, qlabels


def plot_freq_bands_matdyn(filename, matdyn):

    path_freq = gen_plot_data(filename)
    path = path_freq[:, 0]
    nbnd = path_freq.shape[1] - 1

    plt.figure(figsize=(4, 3), dpi=144)
    for i in range(1, nbnd + 1):
        plt.plot(path, path_freq[:, i], color="k", linewidth=1)

    emin = np.min(path_freq[:, 1:])
    emax = np.max(path_freq[:, 1:])
    dist = 10
    plt.xlim(min(path), max(path))
    plt.ylim(emin - dist, emax + dist)
    plt.ylabel(r"Frequency (cm$^{-1}$)", fontsize=fontsizes.label)

    qpts, qlabels = parse_matdyn(matdyn)
    xlabels = qlabels
    nqstep = int((path.shape[0] - 1) / (len(xlabels) - 1))
    # print(f"{nqstep}")
    xlocs = [path[i * nqstep] for i in range(len(xlabels))]
    plt.xticks(xlocs, xlabels, fontsize=fontsizes.tick)
    plt.yticks(fontsize=fontsizes.tick)
    plt.tick_params(axis="x", which="both", direction="in")
    plt.tick_params(axis="y", which="both", direction="in")
    for x in xlocs:
        plt.vlines(
            x,
            plt.ylim()[0],
            plt.ylim()[1],
            colors=colors.grey,
            linewidth=0.5,
            linestyles="-",
        )
    plt.hlines(
        0, min(path), max(path), colors=colors.grey, linewidth=0.5, linestyles="-"
    )
    plt.tight_layout()
    # plt.savefig("phonon.png")
    plt.show()

