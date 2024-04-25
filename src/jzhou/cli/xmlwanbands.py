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
    "-f",
    "--fakefermi",
    type=float,
    # help="The fake Fermi energy value given in command"
)

def cmd_plotxmlwanbands(xmlfile, wanfile, fakefermi):
    """Compare QE bands (xml) and Wannier bands (dat). 
    
    xml and dat files are mandatory. 
    The fakefermi is alternative (to set EF=0). "
    """
    from ..plot_xmlwanbands import plot_xml_wan_bands

    # file = "aiida.xml"
    print("DFT bands is given by", xmlfile)
    print("Wan bands is given by", wanfile)

    if fakefermi:
        print("Fermi energy is given as: ", fakefermi)
        plot_xml_wan_bands(xmlfile, wanfile, fakefermi)
    else:
        print("Fermi energy is given by xml file. ")
        plot_xml_wan_bands(xmlfile, wanfile, fakefermi=None)
