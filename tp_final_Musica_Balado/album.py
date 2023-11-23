from flask import (
Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from tp_final_Musica_Balado.db import get_db

bp = Blueprint('album', __name__, url_prefix="/album")

@bp.route('/')
def index():
    db = get_db()
    canciones = db.execute(
        """SELECT t.name AS Canciones, title AS Disco, sum(t.milliseconds) AS Duracion, ar.name AS Artista, g.name AS Genero
        FROM tracks t JOIN albums a ON t.AlbumId = a.AlbumId
        JOIN artists ar ON ar.ArtistId = a.ArtistId
        JOIN genres g ON g.GenreId = t.GenreId
        GROUP BY t.name"""
    ).fetchall()
    return render_template('album/index.html', canciones=canciones)

def detalle(id):
    albums = get_db().execute(
        """SELECT


        """,
        (id,)
    ).fetchone()
    return render_template('album/detalle.html', albums=albums)
