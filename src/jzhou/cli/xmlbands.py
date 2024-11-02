#!/usr/bin/env python
"""Command to plot figures."""
import click
from .root import cmd_root


@cmd_root.command("plotxmlbands")
@click.argument(
    "file",
    default="aiida.xml",
    type=str,
)
@click.option(
    "-f", "--fakefermi", type=float, help="The fake Fermi energy value given in command"
)
def cmd_plotxmlbands(file, fakefermi):
    """Plot QE bands using xml file.

    shc.dat is mandatory, default is aiida.xml.
    """
    from ..plot_xmlbands import plot_bands

    # file = "aiida.xml"
    print("QE bands is given by", file)

    if fakefermi:
        print("Fermi energy is given as ", fakefermi, " eV.")
        plot_bands(filename=file, fakefermi=fakefermi)
    else:
        print("Fermi energy is given by xml file.")
        plot_bands(filename=file, fakefermi=None)
