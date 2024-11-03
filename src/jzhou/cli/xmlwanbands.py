#!/usr/bin/env python
"""Command to plot figures."""
import click

from .root import cmd_root


@cmd_root.command("plotxmlwanbands")
@click.argument(
        "xmlfile",
        default="aiida.xml",
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
    "-f",
    "--fakefermi",
    type=float,
    help="Fermi energy for plotting. If given, eigenvalues will be shifted by this value."
)

def cmd_plotxmlwanbands(xmlfile, wanfile, wanfile2, fakefermi):
    """Compare QE bands and Wannier bands.

    QE bands are given by xml file, and Wannier bands are given dat files.
    """
    from ..plot_xmlwanbands import find_occ_nbnd, plot_xml_wan_bands

    # file = "aiida.xml"
    print("DFT bands is given by", xmlfile)
    print("Wan bands is given by", wanfile)
    if wanfile2:
        print("Another wan bands is given by", wanfile2)

    if fakefermi:
        if wanfile2:
            print("Fermi energy is given as: ", fakefermi)
            # find_occ_nbnd(xmlfile, wanfile)
            plot_xml_wan_bands(xmlfile, wanfile, wanfile2, fakefermi)
        else:
            print("Fail. The function of fake fermi & none wanfile2 is unable.")
        #     print("Fermi energy is given as: ", fakefermi)
        #     plot_xml_wan_bands(xmlfile, wanfile, wanfile2=None, fakefermi)
    else:
        if wanfile:
            print("Fermi energy is given by xml file. ")
            # find_occ_nbnd(xmlfile, wanfile)
            plot_xml_wan_bands(xmlfile, wanfile, wanfile2, fakefermi=None)
        else:
            print("Fermi energy is given by xml file. ")
            # find_occ_nbnd(xmlfile, wanfile)
            plot_xml_wan_bands(xmlfile, wanfile, wanfile2=None, fakefermi=None)
