"""Module for constants."""


class DotDict:
    """Attribute dictionary, access property by dot."""

    def __init__(self, **kwargs):  # noqa: D107
        # """Initialize."""
        for key, value in kwargs.items():
            setattr(self, key, value)


fontsizes = DotDict(label=14, tick=12)


colors = DotDict(blue="royalblue", green="limegreen", red="tomato", grey="grey")

linestyles = DotDict(
    solid="solid",
    dotted="dotted",
    dashed="dashed",
    dashdot="dashdot",
)
