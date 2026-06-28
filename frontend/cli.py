import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box
from rich.json import JSON
from sqlmodel import Session, select

from backend.orchestrator import process_file_offline
from backend.database import get_engine, ChronicleNote
from backend.exceptions import ChronicleBaseException

app = typer.Typer(
    name="chronicle",
    help="Chronicle.cpp: The Academic Archivist CLI. Offline Knowledge Distillation.",
    rich_markup_mode="markdown",
)
console = Console()


@app.command()
def ingest(
    filepath: Optional[str] = typer.Argument(
        None, help="The path to the file you want to ingest."
    ),
):
    """
    Ingest a file into the Chronicle database. Supports PDF, DOCX, PPTX, XLSX, TXT, MD, WAV, MP3, PNG, JPG.
    """
    if not filepath:
        filepath = typer.prompt("Please enter the path to the file you want to ingest")

    file_path = Path(filepath)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(
            description=f"Ingesting [bold cyan]{file_path.name}[/bold cyan]...",
            total=None,
        )

        try:
            result = process_file_offline(str(file_path))
        except ChronicleBaseException as e:
            console.print(
                Panel(
                    str(e),
                    title="[bold red]Ingestion Error[/bold red]",
                    border_style="red",
                )
            )
            raise typer.Exit(1)
        except Exception as e:
            console.print(
                Panel(
                    f"An unexpected fatal error occurred: {e}",
                    title="[bold red]Fatal System Error[/bold red]",
                    border_style="red",
                )
            )
            raise typer.Exit(1)

    # Success Render
    console.print(
        Panel(
            f"[bold green]Successfully Extracted from {file_path.name}![/bold green]\n\n"
            f"[bold]Summary:[/bold] {result.get('summary', 'N/A')}\n\n"
            f"[bold]Entities:[/bold] {', '.join(result.get('key_entities', []))}",
            title="[bold cyan]Archive Complete[/bold cyan]",
            border_style="green",
        )
    )


@app.command()
def list():
    """
    List all knowledge archived in the Chronicle database.
    """
    engine = get_engine()
    with Session(engine) as session:
        statement = select(ChronicleNote).order_by(ChronicleNote.created_at.desc())
        notes = session.exec(statement).all()

    if not notes:
        console.print("[yellow]No knowledge has been archived yet.[/yellow]")
        return

    table = Table(title="Chronicle Archive", box=box.ROUNDED, border_style="bold cyan")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Filename", style="magenta")
    table.add_column("Date Archived", style="dim")
    table.add_column("Summary Snippet")

    for note in notes:
        summary_snippet = (
            (note.summary[:60] + "...")
            if note.summary and len(note.summary) > 60
            else (note.summary or "")
        )
        table.add_row(
            str(note.id),
            note.filename,
            note.created_at.strftime("%Y-%m-%d %H:%M"),
            summary_snippet,
        )

    console.print(table)


@app.command()
def view(note_id: int = typer.Argument(..., help="The ID of the archive to view.")):
    """
    View the full JSON schema of a specific archive by its ID.
    """
    engine = get_engine()
    with Session(engine) as session:
        note = session.get(ChronicleNote, note_id)

    if not note:
        console.print(
            Panel(
                f"No archive found with ID {note_id}.",
                title="[bold red]Not Found[/bold red]",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    # Render syntax-highlighted JSON
    data = {
        "id": note.id,
        "filename": note.filename,
        "summary": note.summary,
        "action_items": note.action_items,
        "key_entities": note.key_entities,
        "created_at": note.created_at.isoformat(),
    }

    console.print(f"[bold cyan]Viewing Archive {note_id}: {note.filename}[/bold cyan]")
    console.print(JSON(json.dumps(data)))


@app.command()
def delete(note_id: int = typer.Argument(..., help="The ID of the archive to delete.")):
    """
    Delete a specific archive from the database.
    """
    typer.confirm(
        f"Are you sure you want to permanently delete archive ID {note_id}?", abort=True
    )

    engine = get_engine()
    with Session(engine) as session:
        note = session.get(ChronicleNote, note_id)
        if not note:
            console.print(
                Panel(
                    f"No archive found with ID {note_id}.",
                    title="[bold red]Not Found[/bold red]",
                    border_style="red",
                )
            )
            raise typer.Exit(1)

        session.delete(note)
        session.commit()

    console.print(
        f"[bold green]Archive ID {note_id} has been permanently deleted.[/bold green]"
    )


if __name__ == "__main__":
    app()
