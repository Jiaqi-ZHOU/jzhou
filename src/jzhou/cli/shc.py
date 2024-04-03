#!/usr/bin/env python
"""Command to plot figures."""
import click

from .root import cmd_root


@cmd_root.command("plotshc")
@click.argument(
    "file",
    default="aiida-shc-fermiscan.dat",
    type=str,
    help="The shc dat file, default is aiida-shc-fermiscan.dat",
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
@click.option("--CBM", type=float, help="The CBM of semiconductor")
def cmd_plot_shc(file, win, fermi, clength, CBM):
    """Plot shc v.s. energy. shc.dat is mandatory. win is alternative."""
    from ..plot_shc import read_file, read_win, plot
    
    data = read_file(file)
    print("shc.dat file is given by", file)

    if win:
        print("win file is given by", win)
        VBM, CBM, c = read_win(win)
        fermi = VBM
        clength = c
        plot(data, clength, fermi, CBM=CBM)

    else:
        fermi = fermi
        clength = clength
        if CBM:
            plot(data, clength, fermi, CBM=CBM)
        else:
            plot(data, clength, fermi, CBM=None)
