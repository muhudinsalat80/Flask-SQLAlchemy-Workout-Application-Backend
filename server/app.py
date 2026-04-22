

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)



class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.String)

    exercises = db.relationship(
        "WorkoutExercise",
        backref="workout",
        cascade="all, delete-orphan"
    )


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.String)

    workouts = db.relationship(
        "WorkoutExercise",
        backref="exercise",
        cascade="all, delete-orphan"
    )


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id")
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id")
    )

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)



class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)


class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)


class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)



@app.route("/")
def home():
    return "Workout API Running"


@app.route("/workouts", methods=["GET"])
def get_workouts():
    data = Workout.query.all()
    return jsonify(workouts_schema.dump(data))


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    workout = Workout(
        date=data["date"],
        duration_minutes=data["duration_minutes"],
        notes=data.get("notes")
    )

    db.session.add(workout)
    db.session.commit()

    return jsonify(workout_schema.dump(workout)), 201


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "deleted"})


@app.route("/exercises", methods=["GET"])
def get_exercises():
    data = Exercise.query.all()
    return jsonify(exercises_schema.dump(data))


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    exercise = Exercise(
        name=data["name"],
        category=data["category"],
        equipment_needed=data.get("equipment_needed")
    )

    db.session.add(exercise)
    db.session.commit()

    return jsonify(exercise_schema.dump(exercise)), 201


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({"message": "deleted"})


@app.route("/add-workout-exercise", methods=["POST"])
def add_workout_exercise():
    data = request.get_json()

    item = WorkoutExercise(
        workout_id=data["workout_id"],
        exercise_id=data["exercise_id"],
        reps=data.get("reps"),
        sets=data.get("sets"),
        duration_seconds=data.get("duration_seconds")
    )

    db.session.add(item)
    db.session.commit()

    return jsonify(workout_exercise_schema.dump(item)), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)