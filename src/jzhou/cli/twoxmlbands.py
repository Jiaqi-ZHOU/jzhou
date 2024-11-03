#!/usr/bin/env python
"""Command to plot figures."""
import click

from .root import cmd_root


@cmd_root.command("plottwoxmlbands")
@click.argument(
    "xmlfile1",
    type=str,
)
@click.option(
    "--label1",
    "-l1",
    default="label1",
    type=str,
    help="Legend for the 1st xml file"
)
@click.argument(
    "xmlfile2",
    type=str,
)
@click.option(
    "--label2",
    "-l2",
    default="label2",
    type=str,
    help="Legend for the 2nd xml file"
)
@click.option(
    "--fakefermi", "-f", default=None, type=float, help="Fermi energy for plotting. If given, eigenvalues will be shifted by this value."
)
def cmd_plottwoxmlbands(xmlfile1, xmlfile2, label1, label2, fakefermi):
    """Compare two DFT bands using two xml files."""
    from ..plot_twoxmlbands import plot_two_DFT_bands

    # TODO revise README.md.

    print("The 1st xml file is given by", xmlfile1)
    print("The 2nd xml file is given by", xmlfile2)

    if fakefermi:
        print("Fermi energy is given as", fakefermi)
        plot_two_DFT_bands(
            xmlfile1=xmlfile1,
            label1=label1,
            xmlfile2=xmlfile2,
            label2=label2,
            fakefermi=fakefermi,
        )
    else:
        print("Fermi energy is given by xml file")
        plot_two_DFT_bands(
            xmlfile1=xmlfile1,
            label1=label1,
            xmlfile2=xmlfile2,
            label2=label2,
            fakefermi=None,
        )
