#!/usr/bin/env python
"""Command to plot figures."""
import click

from .root import cmd_root


@cmd_root.command("plotshc")
@click.argument(
    "file",
    default="aiida-shc-fermiscan.dat",
    type=str,
    # help="The shc data. Default is aiida-shc-fermiscan.dat. ",
)
@click.argument(
    "win",
    default="aiida.win",
    type=str,
    # help="The Wannier input. Default is aiida.win. ",
)
def cmd_plotshc(file, win):
    """Plot spin Hall conductivity v.s. energy.

    SHC is given by aiida-shc-fermiscan.dat, the unit conversion requires aiida.win.
    """
    from ..plot_shc import plot, read_file, read_win

    data = read_file(file)
    print("shc.dat file is given by", file)
    print("win file is given by", win)
    fermi, vbm, cbm, clength = read_win(win)
    if cbm - vbm > 1e-6:  # This is an insulator
        fermi = vbm
        print("The material is an insulator")
        print(f"{cbm=}")
        print(f"{vbm=}")
        print("Bandgap=", cbm - vbm)
    else:
        fermi = fermi
        print("The material is a metal")
        print(f"{fermi=}")
    # clength = c
    plot(data, clength, fermi, vbm, cbm=cbm)
