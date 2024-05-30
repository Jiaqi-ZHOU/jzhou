#!/usr/bin/env python
"""Command to plot figures."""
import click
from .root import cmd_root


@cmd_root.command("plotvaspbands")
@click.argument(
    "dirname",
    default="./",
    type=str,
)
@click.option(
    "-f",
    "--fakefermi",
    type=float,
    help="The fake Fermi energy value given in command"
)
def cmd_plotvaspbands(dirname, fakefermi):
    """Plot vasp bands using the dirname providing EIGENVAL, KPOINTS, POSCAR, OUTCAR. 
    
    fakefermi is alternative (to set EF=0). """
    from ..plot_vaspbands import plot_bands

    if fakefermi:
        print("Fermi energy =", fakefermi)
        plot_bands(dirname=dirname, fakefermi=fakefermi)
    else:
        print("Fermi energy is given by bands OUTCAR")
        plot_bands(dirname=dirname, fakefermi=None)
