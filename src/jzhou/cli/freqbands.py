#!/usr/bin/env python
"""Command to plot figures."""
import click
from .root import cmd_root


@cmd_root.command("plotfreqbands")
@click.argument(
    "file",
    default="aiida.freq.gp",
    type=str,
)


def cmd_plotfreqbands(file):
    """Plot QE phonon bands using freq file.

    freq.gp is mandatory, default is aiida.freq.gp.
    """
    from ..plot_freqbands import plot_freq_bands

    # file = "aiida.xml"
    print("QE freq bands is given by", file)
    plot_freq_bands(filename=file)
