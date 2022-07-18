from typing import Optional
from todo import ERRORS, __app_name__, __version__, config, database
from pathlib import Path
import typer

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help = "Show the application's version and exit",
        callback = _version_callback,
        is_eager = True,
    )
) -> None:
    return

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_PATH),
        "--db-path",
        "-db",
    )
) -> None:
    """
    Initialize to-do database with default PATH\n
    If --db-path or -db is used, PATH given as an argument will be used
    """
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f"Creating config file failed with {ERRORS[app_init_error]}",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f"Creating database file failed with {ERRORS[db_init_error]}",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    typer.secho(f"The to-do database is {db_path}", fg = typer.colors.GREEN)