class MyClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


fontsizes = MyClass(label=10, tick=8)


colors = MyClass(blue="royalblue", green="limegreen", red="tomato", grey="grey")

linestyles = MyClass(
    solid="solid",
    dotted="dotted",
    dashed="dashed",
    dashdot="dashdot",
)
