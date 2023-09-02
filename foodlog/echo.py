import click


def line(text: str = "") -> None:
    click.echo(text)


def title(text: str = "") -> None:
    click.echo(click.style(text=text, bold=True))


def error(text: str = "") -> None:
    click.echo(click.style(text=text, fg="red"))


def warning(text: str = "") -> None:
    click.echo(click.style(text=text, fg="yellow"))


def success(text: str = "") -> None:
    click.echo(click.style(text=text, fg="green"))


def comment(text: str = "") -> None:
    click.echo(click.style(text=text, fg="bright_black"))
