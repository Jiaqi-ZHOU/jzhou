#!/usr/bin/env python
"""Command to plot figures."""
import click
from .root import cmd_root


@cmd_root.command("plotwanbands")
@click.option(
        "--wanfile",
        type=str,
        # help="The Wannier dat file, default is aiida_band.dat",
    )
@click.option(
    "--wanfile2",                
    # "-w2",
    type=str,
    # help="The fake Fermi energy value given in command"
)
@click.option(
    "-f",
    "--fakefermi",
    type=float,
    # help="The fake Fermi energy value given in command"
)

def cmd_plotwanbands(wanfile, wanfile2, fakefermi):
    """Plot Wannier bands (dat). 
    
    The fakefermi is alternative (to set EF=0). "
    """
    from ..plot_wanbands import plot_wan_bands

    print("Wan bands is given by", wanfile)
    if wanfile2:
        print("Another wan bands is given by", wanfile2)

    if fakefermi:
        if wanfile2:
            print("Fermi energy is given as: ", fakefermi)  
            plot_wan_bands(wanfile, wanfile2, fakefermi)
        else:
            plot_wan_bands(wanfile=wanfile, wanfile2=None, fakefermi=fakefermi)
            # print("Fail. The function of fake fermi & none wanfile2 is unable.")
        #     print("Fermi energy is given as: ", fakefermi)
        #     plot_xml_wan_bands(xmlfile, wanfile, wanfile2=None, fakefermi)
    else:
        if wanfile:  
            plot_wan_bands(wanfile, wanfile2, fakefermi=0)
        else: 
            plot_wan_bands(wanfile, wanfile2=None, fakefermi=0)