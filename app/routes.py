from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from app.models import Idea, db
from app.forms import IdeaForm
from datetime import datetime
import logging

main = Blueprint('main', __name__)

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    ideas = Idea.query.order_by(Idea.created_at.desc()).paginate(page=page, per_page=9)
    return render_template('index.html', ideas=ideas)

@main.route('/submit', methods=['GET', 'POST'])
def submit():
    form = IdeaForm()
    if form.validate_on_submit():
        try:
            current_app.logger.info('Form validated, creating new idea...')
            idea = Idea(
                title=form.title.data.strip(),
                description=form.description.data.strip(),
                problem=form.problem.data.strip(),
                student_name=form.student_name.data.strip(),
                category=form.category.data.strip() if form.category.data else None,
                created_at=datetime.utcnow()
            )
            
            db.session.add(idea)
            db.session.commit()
            current_app.logger.info(f'Successfully saved idea: {idea.title}')
            
            # Redirect to index with success parameter
            return redirect(url_for('main.index', submitted='true'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error saving idea: {str(e)}')
            flash('An error occurred while saving your idea. Please try again.', 'error')
    elif request.method == 'POST':
        current_app.logger.warning('Form validation failed')
        for field, errors in form.errors.items():
            for error in errors:
                current_app.logger.warning(f'Error in {field}: {error}')
                flash(f'Error in {field}: {error}', 'error')
        
    # If there are form errors, they'll be displayed automatically by the template
    return render_template('submit.html', form=form)
