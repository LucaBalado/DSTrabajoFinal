from flask import (
Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from tp_final_Musica_Balado.db import get_db

bp = Blueprint('track', __name__, url_prefix="/track")

@bp.route('/')
def index():
    db = get_db()
    canciones = db.execute(
        """SELECT t.name AS Canciones, title AS Disco, ar.name AS Artista, g.name AS Genero,
        t.TrackId
        FROM tracks t JOIN albums a ON t.AlbumId = a.AlbumId
        JOIN artists ar ON ar.ArtistId = a.ArtistId
        JOIN genres g ON g.GenreId = t.GenreId
        ORDER BY t.name DESC"""
    ).fetchall()
    return render_template('track/index.html', canciones=canciones)

@bp.route('/<int:id>')
def detalle(id):
    db = get_db()
    tema= db.execute(
        """SELECT t.Name AS Cancion, a.Title AS Disco, t.Milliseconds AS Duración, g.name AS genero
        t.TrackId
         FROM albums a JOIN tracks t ON a.AlbumId = t.AlbumId
         JOIN genres g ON t.GenreId = g.GenreId
		 WHERE t.TrackId = ?""",
        (id,)
    ).fetchone()
    return  render_template('track/detalle.html', tema=tema)