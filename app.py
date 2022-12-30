from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import date


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/dbrecords"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class registration_list(db.Model):
    carnet = db.Column(db.String(6), primary_key=True)
    username = db.Column(db.String(70), nullable=False)
    direction = db.Column(db.String(70), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=False)
    student_career = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(
        db.DateTime(), nullable=False, default=db.func.current_timestamp()
    )

    def __init__(
        self,
        carnet,
        username,
        direction,
        gender,
        telephone,
        date_of_birth,
        student_career,
        genre,
    ):
        self.carnet = carnet
        self.username = username
        self.direction = direction
        self.gender = gender
        self.telephone = telephone
        self.date_of_birth = date_of_birth
        self.student_career = student_career
        self.genre = genre


class RecordsSchema(ma.Schema):
    class Meta:
        fields = (
            "carnet",
            "username",
            "direction",
            "gender",
            "telephone",
            "date_of_birth",
            "student_career",
            "genre",
            "registration_date",
        )


record_schema = RecordsSchema()
records_schema = RecordsSchema(many=True)


def calcular_edad(fecha_nacimiento):
    fecha_actual = date.today()
    resultado = fecha_actual.year - fecha_nacimiento.year
    resultado -= (fecha_actual.month, fecha_actual.day) < (
        fecha_nacimiento.month,
        fecha_nacimiento.day,
    )
    return resultado


@app.route("/newregister", methods=["POST"])  # AGREGAR
def create_list():
    carnet = request.json["carnet"]
    username = request.json["username"]
    direction = request.json["direction"]
    gender = request.json["gender"]
    telephone = request.json["telephone"]
    date_of_birth = request.json["date_of_birth"]
    student_career = request.json["student_career"]
    genre = request.json["genre"]

    if len(carnet) <= 6:

        carnet2 = []

        for i in carnet:
            carnet2 = carnet2 + [i]
            if i == "0":
                return jsonify({"message": "EL CARNET CONTIENE CEROS"})
                break
        carnet2 = list(map(str.upper, carnet2))

        if (
            carnet2[0] == "A"
            and carnet2[2] == "5"
            and carnet2[5] == "1"
            or carnet2[5] == "3"
            or carnet2[5] == "9"
        ):

            new_record = registration_list(
                carnet,
                username,
                direction,
                gender,
                telephone,
                date_of_birth,
                student_career,
                genre,
            )

            db.session.add(new_record)
            db.session.commit()

            return jsonify({"message": "SE AGREGARON CORRECTAMENTE LOS DATOS"})
            # return record_schema.jsonify(new_record)

        else:
            return jsonify({"message": "EL CARNET NO CUMPLE CON LOS REQUISITOS"})

    #

    else:
        return jsonify({"message": "NOSE AGREGARON DATOS"})


@app.route("/records", methods=["GET"])  #mostrar registros
def get_movies():
    all_tasks = registration_list.query.all()
    result = records_schema.dump(all_tasks)
    return jsonify(result)


@app.route("/", methods=["GET"])
def index():

    return jsonify({"message": "Welcome to my API"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
