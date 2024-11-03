#!/usr/bin/env python
"""Command to plot figures."""
import click

from .root import cmd_root


@cmd_root.command("plotvaspbands")
@click.argument(
    "dirname",
    default="./",
    type=str
)
@click.option(
    "-f",
    "--fakefermi",
    type=float,
    default=None,
    help="Fermi energy for plotting. If given, eigenvalues will be shifted by this value."
)
def cmd_plotvaspbands(dirname, fakefermi):
    """Plot VASP bands.

    VASP bands are provided by a dirname including EIGENVAL, KPOINTS, POSCAR, and OUTCAR.
    """
    from ..plot_vaspbands import plot_bands

    if fakefermi:
        print("Fermi energy =", fakefermi)
        plot_bands(dirname=dirname, fakefermi=fakefermi)
    else:
        print("Fermi energy is given by bands OUTCAR")
        plot_bands(dirname=dirname, fakefermi=None)
