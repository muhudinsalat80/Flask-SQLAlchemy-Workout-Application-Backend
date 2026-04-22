from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Exercise(db.Model):
    """Represents a reusable exercise that can be added to many workouts."""

    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)

    # name must exist and be unique across all exercises
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # one exercise can appear in many workout_exercises
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )

    # lets us access workouts directly from an exercise instance
    workouts = association_proxy('workout_exercises', 'workout')

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters.")
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        allowed = ['strength', 'cardio', 'flexibility', 'balance']
        if value.lower() not in allowed:
            raise ValueError(f"Category must be one of: {allowed}")
        return value.lower()

    def __repr__(self):
        return f"<Exercise id={self.id} name='{self.name}' category='{self.category}'>"


class Workout(db.Model):
    """Represents a single training session containing one or more exercises."""

    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)

    # date and duration are required fields
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # one workout can have many workout_exercises
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )

    # lets us access exercises directly from a workout instance
    exercises = association_proxy('workout_exercises', 'exercise')

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Duration must be greater than 0 minutes.")
        return value

    def __repr__(self):
        return f"<Workout id={self.id} date='{self.date}' duration={self.duration_minutes}min>"


class WorkoutExercise(db.Model):
    """
    Join table between Workout and Exercise.
    Tracks how an exercise was performed in a specific workout
    (sets, reps, and/or duration).
    """

    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)

    # both foreign keys are required — a WorkoutExercise must belong to both
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    # performance data — at least one should be provided
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('sets')
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Sets must be greater than 0.")
        return value

    @validates('reps')
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Reps must be greater than 0.")
        return value

    def __repr__(self):
        return (
            f"<WorkoutExercise id={self.id} "
            f"workout_id={self.workout_id} exercise_id={self.exercise_id}>"
        )