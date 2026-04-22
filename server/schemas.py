from marshmallow import Schema, fields, validate


# These two "slim" schemas are used inside WorkoutExerciseSchema
# to avoid circular nesting (e.g. Workout -> WorkoutExercise -> Workout -> ...)


class ExerciseSlimSchema(Schema):
    """Minimal exercise info — used when viewing from the workout side."""
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    category = fields.Str(dump_only=True)
    equipment_needed = fields.Bool(dump_only=True)


class WorkoutSlimSchema(Schema):
    """Minimal workout info — used when viewing from the exercise side."""
    id = fields.Int(dump_only=True)
    date = fields.Date(dump_only=True)
    duration_minutes = fields.Int(dump_only=True)
    notes = fields.Str(dump_only=True)


# WorkoutExercise has two versions depending on which side we're reading from:
#   - WorkoutExerciseSchema: used for POST and inside WorkoutSchema
#   - WorkoutExerciseForExerciseSchema: used inside ExerciseSchema


class WorkoutExerciseSchema(Schema):
    """
    Used when creating a WorkoutExercise (POST) and when serializing
    workout_exercises from inside a Workout.
    Includes nested exercise details so the client sees which exercise it is.
    """
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)

    # schema-level validations — each value must be at least 1 if provided
    reps = fields.Int(load_default=None, validate=validate.Range(min=1, error="Reps must be at least 1."))
    sets = fields.Int(load_default=None, validate=validate.Range(min=1, error="Sets must be at least 1."))
    duration_seconds = fields.Int(load_default=None, validate=validate.Range(min=1, error="Duration must be at least 1 second."))

    # nested exercise info — only included when serializing, not when loading
    exercise = fields.Nested(ExerciseSlimSchema, dump_only=True)


class WorkoutExerciseForExerciseSchema(Schema):
    """
    Used when serializing workout_exercises from inside an Exercise.
    Includes nested workout info so the client sees which workout it belongs to.
    """
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    reps = fields.Int(dump_only=True)
    sets = fields.Int(dump_only=True)
    duration_seconds = fields.Int(dump_only=True)

    # nested workout info
    workout = fields.Nested(WorkoutSlimSchema, dump_only=True)


class ExerciseSchema(Schema):
    """
    Full Exercise schema.
    Used for creating exercises and for GET /exercises/<id>.
    Includes nested workout_exercises so you can see every workout
    this exercise has been added to.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, error="Name must be at least 2 characters."))
    category = fields.Str(
        required=True,
        validate=validate.OneOf(
            ['strength', 'cardio', 'flexibility', 'balance'],
            error="Category must be one of: strength, cardio, flexibility, balance."
        )
    )
    equipment_needed = fields.Bool(load_default=False)

    # shows every workout this exercise appears in
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseForExerciseSchema),
        dump_only=True
    )


class WorkoutSchema(Schema):
    """
    Full Workout schema.
    Used for creating workouts and for GET /workouts/<id>.
    Includes nested workout_exercises with exercise details,
    sets, reps, and duration for each entry.
    """
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Duration must be at least 1 minute.")
    )
    notes = fields.Str(load_default=None)

    # shows every exercise in this workout with performance data
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema),
        dump_only=True
    )


# schema instances used throughout app.py
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()