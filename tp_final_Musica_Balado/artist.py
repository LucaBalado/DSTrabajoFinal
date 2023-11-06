from flask import (
Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from tp_final_Musica_Balado.db import get_db

bp = Blueprint('artist', __name__, url_prefix="/artist")

@bp.route('/')
def index():
    db = get_db()
    canciones = db.execute(
        """SELECT t.name AS Canciones, title AS Disco, ar.name AS Artista, g.name AS Genero
        FROM tracks t JOIN albums a ON t.AlbumId = a.AlbumId
        JOIN artists ar ON ar.ArtistId = a.ArtistId
        JOIN genres g ON g.GenreId = t.GenreId
        ORDER BY t.name DESC"""
    ).fetchall()
    return render_template('artist/index.html', canciones=canciones)


@bp.route('/<int:id>')
def detalle(id):
    db = get_db()
    artista = db.execute(
        """SELECT Name AS Nombre
         FROM artists
         WHERE Artistid = ?""",
        (id,)
    ).fetchone()

    album = db.execute(
        """SELECT a.Title AS Disco, sum(t.milliseconds) AS Duracion, count(t.AlbumId) AS Canciones, g.genres AS Genero
         FROM album a JOIN artist ar On ar.ArtistId = a.ArtistID
         JOIN genres g ON t.GenresID = g.GenresId
         WHERE ar.ArtistId = ?
         GROUP BY album
         ORDER BY album""",
        (id,)
    ).fetchone()

    return render_template('artist/index.html', artista=artista, album=album)

