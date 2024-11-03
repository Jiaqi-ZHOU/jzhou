#!/usr/bin/env python
"""Command to plot figures."""
import click

from .root import cmd_root


@cmd_root.command("plotvaspwanbands")
@click.argument(
        "dirname",
        default="./",
        type=str,
        # help="The bands xml file, default is aiida.xml",
    )
@click.argument(
        "wanfile",
        default="aiida_band.dat",
        type=str,
        # help="The Wannier dat file, default is aiida_band.dat",
    )
@click.option(
    "--wanfile2",
    "-w2",
    type=str,
    help="The 2nd Wannier dat file."
)
@click.option(
    "--fakefermi",
    "-f",
    type=float,
    help="Fermi energy for plotting. If given, eigenvalues will be shifted by this value."
)

def cmd_plotvaspwanbands(dirname, wanfile, wanfile2, fakefermi):
    """Compare VASP bands and Wannier bands.

    VASP bands are provided by a dirname including EIGENVAL, KPOINTS, POSCAR, OUTCAR.
    Wannier bands are given by aiida_band.dat or bulkek.dat.
    """
    from ..plot_vaspwanbands import plot_vasp_wan_bands

    # file = "aiida.xml"
    print("DFT bands is given by the dirname providing EIGENVAL, KPOINTS, POSCAR, OUTCAR : ", dirname)
    print("Wan bands is given by : ", wanfile)
    if wanfile2:
        print("Another wan bands is given by", wanfile2)

    if fakefermi:
        if wanfile2:
            print("Fermi energy is given as: ", fakefermi)
            # find_occ_nbnd(xmlfile, wanfile)
            plot_vasp_wan_bands(dirname, wanfile, wanfile2, fakefermi)
        else:
            print("Fail. The function of fake fermi & none wanfile2 is unable.")
        #     print("Fermi energy is given as: ", fakefermi)
        #     plot_xml_wan_bands(xmlfile, wanfile, wanfile2=None, fakefermi)
    else:
        if wanfile:
            print("Fermi energy is given by OUTCAR file. ")
            # find_occ_nbnd(xmlfile, wanfile)
            plot_vasp_wan_bands(dirname, wanfile, wanfile2, fakefermi=None)
        else:
            print("Fermi energy is given by OUTCAR file. ")
            # find_occ_nbnd(xmlfile, wanfile)
            plot_vasp_wan_bands(dirname, wanfile, wanfile2=None, fakefermi=None)
