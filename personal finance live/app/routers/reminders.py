from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Reminder
from app.forms.forms import ReminderForm

bp = Blueprint('reminders', __name__, url_prefix='/reminders')
reminders_blueprint = bp

@reminders_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def reminders():
    form = ReminderForm()
    if form.validate_on_submit():
        new_reminder = Reminder(
            user_id=current_user.id,
            description=form.description.data,
            due_date=form.due_date.data
        )
        db.session.add(new_reminder)
        db.session.commit()
        flash('Reminder added!', 'success')
        return redirect(url_for('reminders.reminders'))

    user_reminders = Reminder.query.filter_by(user_id=current_user.id).all()
    return render_template('reminders.html', form=form, reminders=user_reminders)

# Route to delete a reminder
@reminders_blueprint.route('/<int:reminder_id>/delete', methods=['POST'])
@login_required
def delete_reminder(reminder_id):
    r = Reminder.query.get_or_404(reminder_id)
    if r.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('reminders.reminders'))
    db.session.delete(r)
    db.session.commit()
    flash('Reminder deleted!', 'info')
    return redirect(url_for('reminders.reminders'))

# Route to mark a reminder as completed
@reminders_blueprint.route('/<int:reminder_id>/complete', methods=['POST'])
@login_required
def mark_as_completed(reminder_id):
    r = Reminder.query.get_or_404(reminder_id)
    if r.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('reminders.reminders'))
    r.completed = not r.completed
    db.session.commit()
    return jsonify({'success': True, 'completed': r.completed})

# Route to edit a reminder
@reminders_blueprint.route('/<int:reminder_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_reminder(reminder_id):
    r = Reminder.query.get_or_404(reminder_id)
    if r.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('reminders.reminders'))

    form = ReminderForm(obj=r)
    if form.validate_on_submit():
        r.description = form.description.data
        r.due_date = form.due_date.data
        db.session.commit()
        flash('Reminder updated!', 'success')
        return redirect(url_for('reminders.reminders'))

    return render_template('edit_reminder.html', form=form, reminder=r)