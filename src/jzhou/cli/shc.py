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
    """Plot shc vs energy.

    shc.dat is mandatory, default is aiida-shc-fermiscan.dat. 
    
    win is mandatory, default is aiida.win.
    """
    from ..plot_shc import read_file, read_win, plot

    data = read_file(file)
    print("shc.dat file is given by", file)
    print("win file is given by", win)
    fermi, vbm, cbm, c = read_win(win)
    if cbm - vbm > 1e-6:  # This is an insulator
        fermi = vbm
        print("This is a insulator")
        print(f"{cbm=}")
        print(f"{vbm=}")
        print("Bandgap=", cbm - vbm)
    else:
        fermi = fermi
        print("This is a metal")
        print(f"{fermi=}")
    clength = c
    plot(data, clength, fermi, vbm, cbm=cbm)
