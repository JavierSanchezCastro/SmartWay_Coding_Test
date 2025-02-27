from app.db.models.User import User
from pydantic import UUID4, EmailStr
from app.users import bp
from flask import render_template


@bp.route("/")
async def get_all():
    print("usersss", flush=True)
    users = User.query.all()
    return render_template("users/users.html", users=users)

@bp.route("/uuid/<uuid:uuid>")
async def get_by_uuid(uuid):
    user = User.query.filter_by(uuid=str(uuid)).first_or_404()
    return render_template("users/user_detail.html", user=user)

@bp.route("/email/<email>")
async def get_by_email(email):
    user = User.query.filter_by(email=email).first_or_404()
    return render_template("users/user_detail.html", user=user)
#
@bp.route("/uuid/<uuid:uuid>/loans")
async def get_loans_by_uuid(uuid):
    user = User.query.filter_by(uuid=str(uuid)).first_or_404()
    return render_template("loans/loan_history.html", user=user)
    return templates.TemplateResponse("loan_history.html", {"request": request, "user": user})
#
#@bp.route("/email/{uuid}/loans")
#async def get_loans_by_email(request: Request, email: EmailStr, db: SessionDB):
#    user = UserService.get_by_email(email=email, db=db)
#    return templates.TemplateResponse("loan_history.html", {"request": request, "user": user})
#
#