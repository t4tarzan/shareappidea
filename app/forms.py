from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Optional, Email

class IdeaForm(FlaskForm):
    title = StringField('Idea Title', validators=[
        DataRequired(),
        Length(min=5, max=100, message='Title must be between 5 and 100 characters')
    ])
    
    problem = TextAreaField('Problem Statement', validators=[
        DataRequired(),
        Length(min=20, message='Please provide a detailed problem statement (at least 20 characters)')
    ])
    
    description = TextAreaField('Your Solution', validators=[
        DataRequired(),
        Length(min=50, message='Please provide a detailed description (at least 50 characters)')
    ])
    
    student_name = StringField('Your Name', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    category = SelectField('Category (Optional)', choices=[
        ('', 'Select a category'),
        ('Technology', 'Technology'),
        ('Education', 'Education'),
        ('Healthcare', 'Healthcare'),
        ('Finance', 'Finance'),
        ('Sustainability', 'Sustainability'),
        ('Other', 'Other')
    ])
    
    submit = SubmitField('Submit Idea')

class NewsletterSignupForm(FlaskForm):
    """Form for newsletter signup"""
    name = StringField('Your Name', validators=[
        Length(max=100, message='Name must be less than 100 characters'),
        Optional()
    ], render_kw={
        'placeholder': 'Your name (optional)',
        'class': 'form-control'
    })
    
    email = StringField('Email Address', validators=[
        DataRequired('Please enter your email address'),
        Email('Please enter a valid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ], render_kw={
        'placeholder': 'Your email address',
        'class': 'form-control',
        'aria-describedby': 'emailHelp'
    })
    
    submit = SubmitField('Subscribe', render_kw={
        'class': 'button primary'
    })
