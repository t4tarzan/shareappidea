from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort, jsonify, flash
from flask_login import login_required, current_user
from .models import db, Idea, NewsletterSubscriber
from .forms import IdeaForm, NewsletterSignupForm
from datetime import datetime
import logging
from sqlalchemy import or_, func

main = Blueprint('main', __name__)

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    # Get featured ideas (limit to 3)
    featured_ideas = Idea.query.filter_by(featured=True).order_by(Idea.created_at.desc()).limit(3).all()
    # Get trending ideas (most viewed, limit to 4)
    trending_ideas = Idea.query.order_by(Idea.views.desc()).limit(4).all()
    # Get all ideas for the main grid
    ideas = Idea.query.order_by(Idea.created_at.desc()).paginate(page=page, per_page=9)
    return render_template('index.html', 
                         ideas=ideas,
                         featured_ideas=featured_ideas,
                         trending_ideas=trending_ideas)

@main.route('/idea/<int:idea_id>')
def view_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    # Increment view count
    idea.views += 1
    db.session.commit()
    return render_template('idea_detail.html', idea=idea)

@main.route('/category/<category>')
def browse_category(category):
    # List of valid categories to prevent SQL injection
    valid_categories = [
        'Technology', 'Education', 'Healthcare', 
        'Finance', 'Sustainability', 'Social Impact'
    ]
    
    if category not in valid_categories:
        abort(404)
    
    page = request.args.get('page', 1, type=int)
    ideas = Idea.query.filter_by(category=category)\
                     .order_by(Idea.created_at.desc())\
                     .paginate(page=page, per_page=9)
    
    # Get featured ideas (limit to 3)
    featured_ideas = Idea.query.filter_by(featured=True, category=category)\
                             .order_by(Idea.created_at.desc())\
                             .limit(3).all()
    
    return render_template('category.html',
                         category=category,
                         ideas=ideas,
                         featured_ideas=featured_ideas)

@main.route('/search')
def search_ideas():
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', 'newest')
    page = request.args.get('page', 1, type=int)
    
    # Start building the query
    search_query = Idea.query
    
    # Apply search term filter if provided
    if query:
        search_query = search_query.filter(
            or_(
                Idea.title.ilike(f'%{query}%'),
                Idea.description.ilike(f'%{query}%'),
                Idea.problem.ilike(f'%{query}%'),
                Idea.student_name.ilike(f'%{query}%')
            )
        )
    
    # Apply category filter if provided
    if category and category != 'all':
        search_query = search_query.filter(Idea.category == category)
    
    # Apply sorting
    if sort_by == 'newest':
        search_query = search_query.order_by(Idea.created_at.desc())
    elif sort_by == 'oldest':
        search_query = search_query.order_by(Idea.created_at.asc())
    elif sort_by == 'views':
        search_query = search_query.order_by(Idea.views.desc())
    elif sort_by == 'title':
        search_query = search_query.order_by(Idea.title.asc())
    else:
        # Default to newest first
        search_query = search_query.order_by(Idea.created_at.desc())
    
    # Paginate the results
    ideas = search_query.paginate(page=page, per_page=9)
    
    # If it's an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'html': render_template('_idea_list.html', ideas=ideas.items),
            'has_next': ideas.has_next,
            'next_page': ideas.next_num if ideas.has_next else None
        })
    
    # For regular page load, render the full template
    return render_template('search_results.html',
                         query=query,
                         selected_category=category,
                         sort_by=sort_by,
                         ideas=ideas)

@main.route('/newsletter/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Handle newsletter subscription"""
    form = NewsletterSignupForm()
    
    if form.validate_on_submit():
        try:
            # Check if email already exists
            existing_subscriber = NewsletterSubscriber.query.filter_by(
                email=form.email.data.lower()
            ).first()
            
            if existing_subscriber:
                if existing_subscriber.is_active:
                    flash('This email is already subscribed to our newsletter!', 'info')
                else:
                    # Resubscribe existing user
                    existing_subscriber.is_active = True
                    existing_subscriber.unsubscribed_at = None
                    db.session.commit()
                    flash('Thanks for resubscribing to our newsletter!', 'success')
            else:
                # Create new subscriber
                subscriber = NewsletterSubscriber(
                    email=form.email.data.lower(),
                    name=form.name.data if form.name.data else None
                )
                db.session.add(subscriber)
                db.session.commit()
                flash('Thank you for subscribing to our newsletter!', 'success')
                
            return jsonify({
                'success': True,
                'message': 'Subscription successful!'
            })
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error subscribing to newsletter: {str(e)}')
            return jsonify({
                'success': False,
                'message': 'An error occurred. Please try again.'
            }), 500
    
    # If form validation fails
    errors = {field.name: field.errors for field in form if field.errors}
    return jsonify({
        'success': False,
        'message': 'Please correct the errors in the form.',
        'errors': errors
    }), 400


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
