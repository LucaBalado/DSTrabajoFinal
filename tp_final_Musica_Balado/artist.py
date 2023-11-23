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
        """SELECT DISTINCT(ar.name) AS Artista, t.name AS Canciones, count(title) AS Disco, 
        g.name AS Genero, ar.ArtistId
        FROM tracks t JOIN albums a ON t.AlbumId = a.AlbumId
        JOIN artists ar ON ar.ArtistId = a.ArtistId
        JOIN genres g ON g.GenreId = t.GenreId
        GROUP BY ar.name"""
    ).fetchall()
    return render_template('artist/index.html', canciones=canciones)


@bp.route('/<int:id>')
def detalle(id):
    db = get_db()
    artista = db.execute(
        """SELECT Name AS Nombre, artistId
         FROM artists
         WHERE Artistid = ?""",
        (id,)
    ).fetchone()

    album = db.execute(
        """SELECT a.Title AS Disco, sum(t.milliseconds) AS Duracion, count(t.AlbumId) AS Canciones, g.name AS Genero
         FROM albums a JOIN artists ar On ar.ArtistId = a.ArtistID
		 JOIN tracks t ON a.AlbumId=t.AlbumId
         JOIN genres g ON t.genreID = g.GenreId
         WHERE ar.ArtistId= ?
         GROUP BY disco
""",
        (id,)
    ).fetchall()

    return render_template('artist/detalle.html', artista=artista, album=album)

