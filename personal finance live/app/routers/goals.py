# app/routers/goals.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Goal
from app.forms.forms import GoalForm

bp = Blueprint('goals', __name__, url_prefix='/goals')
goals_blueprint = bp
# -------------------------------------------------
# LIST / ADD
# -------------------------------------------------
@goals_blueprint.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    form = GoalForm() 
    if form.validate_on_submit():
        new_goal  = Goal(
        user_id       =current_user.id,
        title         =form.title.data,
        description   =form.description.data,
        target        =form.target.data,
        saved=0.0
        )
        db.session.add(new_goal)
        db.session.commit()
        flash('Goal created!', 'success')
        return redirect(url_for('goals.goals'))

    user_goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('goals.html', form=form, goals=user_goals)

# -------------------------------------------------
# EDIT
# -------------------------------------------------
@goals_blueprint.route('/<int:goal_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('goals.goals'))

    form = GoalForm(obj=goal)
    if form.validate_on_submit():
        goal.title = form.description.data
        goal.target = form.target_amount.data
        db.session.commit()
        flash('Goal updated!', 'info')
        return redirect(url_for('goals.goals'))

    user_goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('goals.html', form=form, goals=user_goals)

# -------------------------------------------------
# DELETE
# -------------------------------------------------
@goals_blueprint.route('/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('goals.goals'))

    db.session.delete(goal)
    db.session.commit()
    flash('Goal deleted!', 'info')
    return redirect(url_for('goals.goals'))