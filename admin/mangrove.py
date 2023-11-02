from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from admin.auth import login_required
from admin.db import get_db

bp = Blueprint("mangroves", __name__)


def get_mangrove(id):
    mangrove = (
        get_db()
        .execute(
            "SELECT id, title, body, created_at, data_id, banner_path"
            " FROM mangroves"
            " WHERE id = ?",
            (id,),
        )
        .fetchone()
    )

    if mangrove is None:
        abort(404, f"Mangrove data id {id} doesn't exist.")

    return mangrove


def get_mangrove_by_dataid(dataid):
    mangrove = (
        get_db()
        .execute(
            "SELECT id, title, body, created_at, data_id, banner_path"
            " FROM mangroves"
            " WHERE data_id = ?",
            (dataid,),
        )
        .fetchone()
    )

    if mangrove is None:
        abort(404, f"Mangrove data id {dataid} doesn't exist.")

    return mangrove


@bp.route("/")
def index():
    db = get_db()
    mangroves = db.execute(
        "SELECT id, title, body, created_at, data_id, banner_path"
        " FROM mangroves"
        " ORDER BY created_at DESC"
    ).fetchall()

    formatted_data = []
    for mangrove in mangroves:
        formatted_data.append(
            {
                "id": mangrove["id"],
                "title": mangrove["title"],
                "data_id": mangrove["data_id"],
                "banner_path": mangrove["banner_path"],
                "body": mangrove["body"][: 300 - 3] + "...",
                "created_at": mangrove["created_at"],
            }
        )

    return render_template("mangroves/index.html", mangroves=formatted_data)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        data_id = request.form["data_id"]
        banner_path = request.form["banner_path"]
        error = None

        if not title:
            error = "Title is required."

        if not data_id:
            error = "Data ID is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO mangroves (title, body, data_id, banner_path)"
                " VALUES (?, ?, ?, ?)",
                (title, body, data_id, banner_path),
            )
            db.commit()
            return redirect(url_for("mangroves.index"))

    return render_template("mangroves/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    mangrove = get_mangrove(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        data_id = request.form["data_id"]
        banner_path = request.form["banner_path"]
        error = None

        if not title:
            error = "Title is required."

        if not data_id:
            error = "Data ID is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE mangroves SET title = ?, body = ?, data_id = ?, banner_path = ?"
                " WHERE id = ?",
                (title, body, data_id, banner_path, id),
            )
            db.commit()
            return redirect(url_for("mangroves.index"))

    return render_template("mangroves/update.html", mangrove=mangrove)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_mangrove(id)
    db = get_db()
    db.execute("DELETE FROM mangroves WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("mangroves.index"))
