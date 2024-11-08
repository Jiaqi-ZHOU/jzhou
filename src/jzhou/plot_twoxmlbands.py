#!/usr/bin/env python3
import argparse
import math
import xml.etree.ElementTree as ET

from ase.units import Bohr, Ha, Ry
from lxml import etree
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import numpy as np

from .constant import colors, fontsizes


def extract_band_weight_xml(filename: str = "aiida.xml"):

    def getXmlElement(tree, tag, parent="band_structure"):
        path = f"/qes:espresso/output/{parent}"
        if tag != "":
            path += f"/{tag}"
        elem = tree.xpath(
            path, namespaces={"qes": "http://www.quantum-espresso.org/ns/qes/qes-1.0"}
        )
        return elem

    def eigStr2Float(str_list_eig):
        # AUTOEV = 27.211383860484776  # from pwuc.x ls
        AUTOEV = 27.211386245988034  # update Oct 25 2022
        mat_eig = np.array([float(i) * AUTOEV for i in str_list_eig])
        return mat_eig

    def compLen(listfrac, b1, b2, b3):
        mat_frac2cart = np.diag([1, 1, 1])
        listlen = np.zeros(listfrac.shape[1])
        frac_prev = listfrac[:, 0]
        dlen = np.linalg.norm(
            np.matmul(mat_frac2cart, (listfrac[:, 1] - frac_prev).reshape(3, 1))
        )
        for i in range(1, len(listlen)):
            dlen_i = np.linalg.norm(
                np.matmul(mat_frac2cart, (listfrac[:, i] - frac_prev).reshape(3, 1))
            )
            # If too large, might be a discontinuous jump, skip it
            # if dlen_i >= 5 * dlen:
            #     dlen_i = 0
            listlen[i] = listlen[i - 1] + dlen_i
            frac_prev = listfrac[:, i]
        return listlen

    tree = etree.parse(filename)
    alat = float(getXmlElement(tree, "", parent="atomic_structure")[0].attrib["alat"])

    alat *= Bohr
    nks = int(getXmlElement(tree, "nks")[0].text)
    # only for SOC case, no need to consider spin up and spin down
    nbnd = int(getXmlElement(tree, "nbnd")[0].text)
    fermi = eigStr2Float([getXmlElement(tree, "fermi_energy")[0].text])[0]
    b1 = np.array(
        [
            float(i)
            for i in getXmlElement(tree, "../basis_set/reciprocal_lattice/b1")[
                0
            ].text.split()
        ]
    )
    b2 = np.array(
        [
            float(i)
            for i in getXmlElement(tree, "../basis_set/reciprocal_lattice/b2")[
                0
            ].text.split()
        ]
    )
    b3 = np.array(
        [
            float(i)
            for i in getXmlElement(tree, "../basis_set/reciprocal_lattice/b3")[
                0
            ].text.split()
        ]
    )
    b1 *= 2 * np.pi / alat
    b2 *= 2 * np.pi / alat
    b3 *= 2 * np.pi / alat

    bands = np.zeros([nbnd, nks])
    kpt_cart = np.zeros([3, nks])
    weight_qe = np.zeros(nks)

    list_eig = getXmlElement(tree, "ks_energies")
    for kpt in range(nks):
        # idxkpt = getkptidx(list_eig[kpt], recz, nks)
        # print(idxkpt)
        # band_qe[:, idxkpt] = band2float(list_eig[kpt])
        weight = list_eig[kpt].find("k_point").attrib["weight"]
        weight_qe[kpt] = weight
        str_list_eig = list_eig[kpt].find("eigenvalues").text.split()
        bands[:, kpt] = eigStr2Float(str_list_eig)
        kpt_cart[:, kpt] = np.array(
            [float(istr) for istr in list_eig[kpt].find("k_point").text.split()]
        )
    kpt_frac = kpt_cart

    # to 1/angstrom
    kpt_cart = kpt_frac * 2 * np.pi / alat
    kpath = compLen(kpt_cart, b1, b2, b3)

    return kpt_frac, kpath, bands, fermi


def gen_info(filename: str = "aiida.xml"):
    tree = ET.parse(filename)
    # alat = float(tree.find('input').find('atomic_structure').attrib['alat']) * Bohr
    # fermi = float(tree.find('output').find('band_structure').find('fermi_energy').text) * Ha
    nbnd = int(tree.find("output").find("band_structure").find("nbnd").text)
    nelec = int(float(tree.find("output").find("band_structure").find("nelec").text))
    # nk = int(tree.find('input').find('k_points_IBZ').find('nk').text)

    if tree.find("output").find("magnetization").find("spinorbit").text == "true":
        spinor = 1
    elif tree.find("output").find("magnetization").find("spinorbit").text == "false":
        spinor = 2

    a = extract_band_weight_xml(filename)  # This xml includes 28 valance bands and 2 CB
    kpt_frac = a[0]  # bands.shape = (nbnd, nk)
    kpath = a[1]  # bands.shape = (nbnd, nk)
    bands = a[2]  # bands.shape = (nbnd, nk)
    fermi = a[3]  # bands.shape = (nbnd, nk)
    VBM = np.max(bands[0 : nelec / spinor, :])  # num of valence bands=28
    CBM = np.min(bands[nelec / spinor : nbnd, :])  # num of conduction bands=2
    gap = CBM - VBM
    print(CBM)
    print(VBM)
    print(gap)
    if gap > 0.01:
        infofile = "gapinfo"
        with open(infofile, "w") as f:
            f.write("VBM =" + str(VBM) + "\n")
            f.write("CBM =" + str(CBM) + "\n")
            f.write("Energygap =" + str(CBM - VBM) + "\n")
            f.write("Fermi =" + str(fermi) + "\n")

    # return kpath, bands, nbnd, fermi


def plot_DFT_bands(xmlfile, label, color, linestyle, fakefermi=None):
    # plt.subplots(figsize=(4, 3), dpi=300)
    kpt_frac, kpath, bands, realfermi = extract_band_weight_xml(xmlfile)
    # kpt_frac2, kpath2, bands2, realfermi2 = extract_band_weight_xml(xmlfile2)
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
    for i in range(nbnd):
        if i == 0:
            plt.plot(
                kpath,
                bands[i, :] - fermi,
                color=color,
                linestyle=linestyle,
                linewidth=1,
                label=label,
            )
        else:
            plt.plot(
                kpath,
                bands[i, :] - fermi,
                color=color,
                linestyle=linestyle,
                linewidth=1,
            )
    plt.xlim(min(kpath), max(kpath))

    nk = kpt_frac.shape[1]
    tick_locs_list = []
    tick_labels_list = []
    thr = 2e-3
    ky = 0.5773502692
    for i in range(nk):
        if np.linalg.norm(kpt_frac[:, i]) < thr:
            G_loc = kpath[i]
            tick_locs_list.append(G_loc)
            tick_labels_list.append(r"$\mathregular{\Gamma}$")
        if (
            np.linalg.norm(kpt_frac[:, i] - np.array([0.5, ky / 2, 0])) < thr
            or np.linalg.norm(kpt_frac[:, i] - np.array([0, ky, 0])) < thr
        ):
            M_loc = kpath[i]
            tick_locs_list.append(M_loc)
            tick_labels_list.append("M")
        if np.linalg.norm(kpt_frac[:, i] - np.array([1 / 3, ky, 0])) < thr:
            K_loc = kpath[i]
            tick_locs_list.append(K_loc)
            tick_labels_list.append("K")

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

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc="upper right")


def plot_two_DFT_bands(xmlfile1, label1, xmlfile2, label2, fakefermi=None):
    plt.subplots(figsize=(4, 3), dpi=144)
    plot_DFT_bands(
        xmlfile1, label1, color=colors.blue, linestyle="-", fakefermi=fakefermi
    )
    plot_DFT_bands(
        xmlfile2, label2, color=colors.red, linestyle="--", fakefermi=fakefermi
    )
    plt.tight_layout()
    plt.show()
