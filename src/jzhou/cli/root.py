"""Command line interface."""
import click

@click.group(
    "jzhou",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def cmd_root():
    """CLI for the `jzhou` plugin."""