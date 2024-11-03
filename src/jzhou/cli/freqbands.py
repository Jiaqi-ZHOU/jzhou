#!/usr/bin/env python
"""Command to plot figures."""
import click

from .root import cmd_root


@cmd_root.command("plotfreqbands")
@click.argument(
    "freqfile",
    default="aiida.freq",
    type=str,
)
@click.option(
    "-m", "--matdyn", type=str, help="The file to provide qpoints and labels.",
)
def cmd_plotfreqbands(freqfile, matdyn):
    """Plot QE phonon bands using freq file.

    freq file is mandatory, default is aiida.freq.

    Formatted matdyn.in is optinal.
    """
    from ..plot_freqbands import plot_freq_bands, plot_freq_bands_matdyn

    # file = "aiida.xml"
    print("QE freq bands is given by", freqfile)
    if matdyn:
        print("matdyn.in is given by", matdyn)
        plot_freq_bands_matdyn(filename=freqfile, matdyn=matdyn)
    else:
        plot_freq_bands(filename=freqfile)
