#!/usr/bin/env python3
"""
seed.py — Clears and repopulates the database with sample data.
Run with: python seed.py (from inside the server/ directory)
"""

from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    # ------------------------------------------------------------------
    # Step 1: Clear existing data (order matters due to foreign keys)
    # ------------------------------------------------------------------
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()

    # ------------------------------------------------------------------
    # Step 2: Create exercises
    # ------------------------------------------------------------------
    print("Seeding exercises...")

    push_up = Exercise(name='Push Up', category='strength', equipment_needed=False)
    pull_up = Exercise(name='Pull Up', category='strength', equipment_needed=True)
    running = Exercise(name='Running', category='cardio', equipment_needed=False)
    cycling = Exercise(name='Cycling', category='cardio', equipment_needed=True)
    yoga_stretch = Exercise(name='Yoga Stretch', category='flexibility', equipment_needed=False)
    plank = Exercise(name='Plank', category='balance', equipment_needed=False)

    db.session.add_all([push_up, pull_up, running, cycling, yoga_stretch, plank])
    db.session.commit()

    # ------------------------------------------------------------------
    # Step 3: Create workouts
    # ------------------------------------------------------------------
    print("Seeding workouts...")

    morning_strength = Workout(
        date=date(2024, 1, 10),
        duration_minutes=45,
        notes='Upper body strength day'
    )
    evening_cardio = Workout(
        date=date(2024, 1, 12),
        duration_minutes=30,
        notes='Light evening run to finish the week'
    )
    full_body = Workout(
        date=date(2024, 1, 15),
        duration_minutes=60,
        notes='Full body session — mix of strength and flexibility'
    )

    db.session.add_all([morning_strength, evening_cardio, full_body])
    db.session.commit()

    # ------------------------------------------------------------------
    # Step 4: Link exercises to workouts via WorkoutExercise
    # ------------------------------------------------------------------
    print("Seeding workout exercises...")

    # morning strength: push ups + pull ups + plank hold
    we1 = WorkoutExercise(workout_id=morning_strength.id, exercise_id=push_up.id, sets=3, reps=15)
    we2 = WorkoutExercise(workout_id=morning_strength.id, exercise_id=pull_up.id, sets=3, reps=8)
    we3 = WorkoutExercise(workout_id=morning_strength.id, exercise_id=plank.id, duration_seconds=60)

    # evening cardio: running + cycling
    we4 = WorkoutExercise(workout_id=evening_cardio.id, exercise_id=running.id, duration_seconds=1200)
    we5 = WorkoutExercise(workout_id=evening_cardio.id, exercise_id=cycling.id, duration_seconds=900)

    # full body: push ups + yoga stretch + plank hold
    we6 = WorkoutExercise(workout_id=full_body.id, exercise_id=push_up.id, sets=4, reps=12)
    we7 = WorkoutExercise(workout_id=full_body.id, exercise_id=yoga_stretch.id, duration_seconds=300)
    we8 = WorkoutExercise(workout_id=full_body.id, exercise_id=plank.id, duration_seconds=90)

    db.session.add_all([we1, we2, we3, we4, we5, we6, we7, we8])
    db.session.commit()

    print(" Database seeded successfully!")
    print(f"   Exercises:        {Exercise.query.count()}")
    print(f"   Workouts:         {Workout.query.count()}")
    print(f"   WorkoutExercises: {WorkoutExercise.query.count()}")