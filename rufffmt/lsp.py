# Copyright Amethyst Reese
# Licensed under the MIT license

from pathlib import Path

from lsprotocol.types import (
    DocumentFormattingParams,
    MessageType,
    Position,
    Range,
    TEXT_DOCUMENT_FORMATTING,
    TextEdit,
)
from pygls.server import LanguageServer
from pygls.workspace import TextDocument

from .__version__ import __version__
from .core import rufffmt_text


def rufffmt_lsp() -> LanguageServer:
    """
    Initialize a minimal formatting LSP.
    """
    server = LanguageServer("rufffmt-lsp", __version__)

    @server.feature(TEXT_DOCUMENT_FORMATTING)
    def lsp_format_document(
        ls: LanguageServer, params: DocumentFormattingParams
    ) -> list[TextEdit] | None:
        document: TextDocument = ls.workspace.get_text_document(
            params.text_document.uri
        )
        path = Path(document.path).resolve()

        try:
            content = rufffmt_text(path, document.source)
            return [
                TextEdit(
                    Range(
                        Position(0, 0),
                        Position(len(document.lines), 0),
                    ),
                    content,
                ),
            ]
        except Exception as e:
            ls.show_message(f"Formatting failed: {str(e)}", MessageType.Error)
            return []

    return server
