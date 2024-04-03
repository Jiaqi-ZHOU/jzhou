#!/usr/bin/env python
"""Command to plot figures."""
import click

from .root import cmd_root


@cmd_root.command("plotshc")
@click.argument(
    "file",
    default="aiida-shc-fermiscan.dat",
    type=str,
)
@click.option(
    "-w",
    "--win",
    default="aiida.win",
    type=str,
    help="The win input, default is aiida.win",
)
@click.option("--fermi", type=float, help="The Fermi energy")
@click.option("--clength", type=float, help="The cell c length in ang")
@click.option("--cbm", type=float, help="The cbm of semiconductor")
def cmd_plotshc(file, win, fermi, clength, cbm):
    """Plot shc vs energy. 
    
    shc.dat is mandatory, default is aiida-shc-fermiscan.dat.
    win is alternative, default is aiida.win. 
    """
    from ..plot_shc import read_file, read_win, plot
    
    data = read_file(file)
    print("shc.dat file is given by", file)

    if win:
        print("win file is given by", win)
        VBM, cbm, c = read_win(win)
        fermi = VBM
        clength = c
        plot(data, clength, fermi, cbm=cbm)

    else:
        fermi = fermi
        clength = clength
        if cbm:
            plot(data, clength, fermi, cbm=cbm)
        else:
            plot(data, clength, fermi, cbm=None)
