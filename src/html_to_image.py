from dataclasses import dataclass


@dataclass
class Html:
    ...


@dataclass
class Image:
    ...


@dataclass
class HtmlImage(Image):
    html: Html
