#!/usr/bin/env python
"""Command to plot figures."""
import click
from .root import cmd_root


@cmd_root.command("plottwoxmlbands")
@click.argument(
    "xmlfile1",
    default="first.xml",
    type=str,
)
@click.argument(
    "label1",
    default="label1",
    type=str,
)
@click.argument(
    "xmlfile2",
    default="second.xml",
    type=str,
)
@click.argument(
    "label2",
    default="label2",
    type=str,
)
@click.option(
    "-f", "--fakefermi", type=float, help="The fake Fermi energy value given in command"
)
def cmd_plottwoxmlbands(xmlfile1, xmlfile2, label1, label2, fakefermi):
    """Compare two DFT bands using two xml. \
        Two xmls file is mandatory. \
        The Fake fermi energy is alternative (to set EF=0). """
    
    from ..plot_twoxmlbands import plot_two_DFT_bands

    print("The first xml file is given by", xmlfile1)
    print("The second xml file is given by", xmlfile2)

    if fakefermi:
        print("A given Fermi energy =", fakefermi)
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
