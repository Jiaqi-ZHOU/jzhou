#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.gridspec import GridSpec
from ase.units import Bohr
from ase.units import Ha
from ase.units import Ry
from lxml import etree
import argparse
import xml.etree.ElementTree as ET

from .constant import fontsizes, colors


def get_eigenval_info(dirname):
    eigenval_file = dirname + 'EIGENVAL'
    with open(eigenval_file, "r") as f:
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        numbers = f.readline().split()   

        nelec = int(numbers[0])
        nks = int(numbers[1])
        nbnd = int(numbers[2])
        # print(f"num_kpoints = {nks} num_bands = {nbnd}")
        bands = np.zeros((nks, nbnd), dtype=float)
        kpoints = np.zeros((nks, 3))
        f.readline()

        for ik in range(nks):
            line = f.readline()
            kpoints[ik, :] = np.fromstring(line, sep= " ")[0:3]
            count = 0
            while count < nbnd:
                line = f.readline()
                eig = float(line.split()[1])
                bands[ik, count] = eig
                count += 1
            assert count == nbnd
            f.readline()

    return kpoints, bands


def get_poscar_info(dirname):
    poscar = dirname + "POSCAR"

    with open(poscar) as f:
        lines = f.readlines()
    a1 = np.fromstring(lines[2], sep=" ")
    a2 = np.fromstring(lines[3], sep=" ")
    a3 = np.fromstring(lines[4], sep=" ")

    def calculate_reciprocal_lattice(a1, a2, a3):
        # Convert the input vectors to NumPy arrays
        a1 = np.array(a1)
        a2 = np.array(a2)
        a3 = np.array(a3)
        
        # Calculate the volume of the parallelepiped (scalar triple product)
        V = np.dot(a1, np.cross(a2, a3))
        
        # Calculate the reciprocal lattice vectors
        b1 = 2 * np.pi * np.cross(a2, a3) / V
        b2 = 2 * np.pi * np.cross(a3, a1) / V
        b3 = 2 * np.pi * np.cross(a1, a2) / V
        B = np.array([b1, b2, b3])
        return B

    B = calculate_reciprocal_lattice(a1, a2, a3)

    return B


def get_kpath_bands(dirname):
    kpoints, bands = get_eigenval_info(dirname)
    B = get_poscar_info(dirname)
    kpts_cart = kpoints @ B

    def get_kpath(kpts_cart):
        nk = kpts_cart.shape[0]
        kpath = np.zeros(nk)
        D = 0
        for i in range(nk-1):
            Dk = np.linalg.norm(kpts_cart[i+1, :] - kpts_cart[i, :])
            D = D + Dk
            kpath[i+1] = D
        return kpath 
    
    kpath =  get_kpath(kpts_cart)

    return kpath, bands


def get_fermi(dirname):
    outcar = dirname + "/OUTCAR"
    with open(outcar, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if len(line.split()) == 3 and line.split()[0] == 'Fermi':
            fermi = float(line.split()[-1])
            break
    return fermi 

def xticks(dirname):
    kpoints = dirname + "/KPOINTS"
    with open(kpoints, 'r') as f:
        line = f.readline()
        xlabels = line.split()[-1].split("-")
        line = f.readline() 
        nk = int(float(line))
    nlab = len(xlabels)
    _ = np.arange(0, nk * nlab, nk)
    # print(_)
    kpath, bands = get_kpath_bands(dirname)
    xtick_locs = np.zeros(nlab)
    for i in range(1, nlab):
        xtick_locs[i] = kpath[_[i]-1]

    replace_gamma = lambda tick_labels: list(_.replace("G", r"$\Gamma$") for _ in tick_labels)
    xlabels = replace_gamma(xlabels)
    # print(xtick_locs)
    
    return xtick_locs, xlabels 

def plot_bands(dirname, fakefermi=None):

    kpath, bands = get_kpath_bands(dirname)

    realfermi = get_fermi(dirname)

    plt.subplots(figsize=(4, 3), dpi=144)

    # If a fakefermi is not given, we use the real fermi to plot bands,
    # and the realfermi is extracted from eigenvales.
    if fakefermi == None:
        fermi = realfermi
        plt.ylabel(r"$\mathregular{E - {E}_{F}}$ (eV)", fontsize=fontsizes.label)
        plt.hlines(
            0, min(kpath), max(kpath), color="gray", linestyle="-", linewidth=0.5
        )
        plt.ylim(-3, 3)

    # If a fakefermi is given (probably as 0), I will want to 
        # mark the position of real fermi. 
    else:
        fermi = fakefermi
        plt.ylabel(r"$Energy (eV)", fontsize=fontsizes.label)
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
    print("nbnd = " + str(nbnd))
    print("kpt_len = " + str(kpath.shape[0]))
    for i in range(nbnd):
        plt.plot(kpath, bands[:, i] - fermi, color="k", linewidth=1)
    plt.xlim(min(kpath), max(kpath))

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
    plt.tick_params(axis="x", which="both", direction="in")
    plt.tick_params(axis="y", which="both", direction="in")
    plt.tight_layout()
    plt.show()
