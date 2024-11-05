from flask import Flask, redirect, render_template, url_for, send_from_directory, request, session, flash
from functools import wraps
import dataaccess
import traceback
from forms import EditContentForm, PROGRAMMING_LANGUAGES, update_about_page_content_form, insert_skill_form, insert_about_skill_form, insert_teacher_comment_form, teacher_comment_form
from models import Skill, TeacherComment
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = {
    'pdfs': 'static/pdfs',
    'images': 'static/images',
    'presentations': 'static/presentations'
}
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'ppt', 'pptx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] != 'teacher':
            flash('Teacher access required.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    name = dataaccess.get_home_content(1)
    subtitle = dataaccess.get_home_content(2)
    intro = dataaccess.get_home_content(3)
    project_desc = dataaccess.get_home_content(4)  
    collab_text = dataaccess.get_home_content(5)   
    skill1 = dataaccess.get_skill(1)
    skill2 = dataaccess.get_skill(2)
    skill3 = dataaccess.get_skill(3)
    skill4 = dataaccess.get_skill(4)
    skill5 = dataaccess.get_skill(5)
    skills = [skill1, skill2, skill3, skill4, skill5]
    skill_icons = [PROGRAMMING_LANGUAGES.get(skill.lower(), 'fas fa-question') 
                for skill in skills]
    is_teacher = session.get('user_role') == 'teacher'
    is_admin = session.get('user_role') == 'admin'
    teacher_comments = dataaccess.get_all_teacher_comments()
    
    comment_form = teacher_comment_form() if is_teacher else None
    
    return render_template(
        'index.html', 
        name=name, 
        subtitle=subtitle, 
        intro=intro,
        project_desc=project_desc,  
        collab_text=collab_text,   
        skill1=skill1, 
        skill2=skill2, 
        skill3=skill3, 
        skill4=skill4, 
        skill5=skill5,
        skill_icons=skill_icons,
        is_teacher=is_teacher,
        is_admin=is_admin,
        teacher_comments=teacher_comments,
        form=comment_form,
        logged_in=session.get('logged_in', False)
    )

@app.route('/project')
def project():
    return render_template('project.html',
                            is_admin=session.get('user_role') == 'admin',
                            is_teacher=session.get('user_role') == 'teacher',
                            logged_in=session.get('logged_in', False))

@app.route('/github')
def github():
    print("github")
    return redirect("https://github.com/jacksen-ng")


@app.route('/about')
def about():
    print("about")
    about_me = dataaccess.get_about_page_content(1)
    who_i_am = dataaccess.get_about_page_content(2)
    education1 = dataaccess.get_about_page_content(3)
    education2 = dataaccess.get_about_page_content(4)
    education3 = dataaccess.get_about_page_content(5)
    interests1 = dataaccess.get_about_page_content(6)
    interests2 = dataaccess.get_about_page_content(7)
    connect = dataaccess.get_about_page_content(8)
    internship = dataaccess.get_about_page_content(9)
    parttime_job = dataaccess.get_about_page_content(10)
    
    skills_dict = {}
    all_skills = dataaccess.get_all_skills()  
    for skill in all_skills:
        if skill:  
            skills_dict[f'skill{skill[0]}'] = skill[1]  
    
    form = insert_about_skill_form()
    
    return render_template('about.html', 
                            about_me=about_me, 
                            who_i_am=who_i_am, 
                            education1=education1, 
                            education2=education2, 
                            education3=education3, 
                            interests1=interests1, 
                            interests2=interests2, 
                            connect=connect, 
                            internship=internship, 
                            parttime_job=parttime_job, 
                            skills_dict=skills_dict, 
                            form=form, 
                            is_admin=session.get('user_role') == 'admin',
                            is_teacher=session.get('user_role') == 'teacher',
                            logged_in=session.get('logged_in', False))

@app.route('/contact')
def contact():
    return render_template('contact.html',
                            is_admin=session.get('user_role') == 'admin',
                            is_teacher=session.get('user_role') == 'teacher',
                            logged_in=session.get('logged_in', False))

@app.route('/static/pdfs/<path:path>')
def serve_pdf(path):
    return send_from_directory('static/pdfs', path)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user_data = dataaccess.verify_user(username, password)
            if user_data:
                session['user'] = username
                session['user_role'] = user_data['role']  
                session['logged_in'] = True
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials', 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            print(traceback.format_exc())
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('home'))


@app.route('/edit')
@login_required
def edit():
    return render_template('edit.html', logged_in=session.get('logged_in'))

@app.route('/update_content', methods=['POST'])
@login_required
@admin_required
def update_content():
    try:
        name = request.form.get('name')
        subtitle = request.form.get('subtitle')
        intro = request.form.get('intro')
        skill1 = request.form.get('skill1')
        skill2 = request.form.get('skill2')
        skill3 = request.form.get('skill3')
        skill4 = request.form.get('skill4')
        skill5 = request.form.get('skill5')

        success = all([
            dataaccess.update_home_content(1, name),
            dataaccess.update_home_content(2, subtitle),
            dataaccess.update_home_content(3, intro),
            dataaccess.update_skill(1, skill1),
            dataaccess.update_skill(2, skill2),
            dataaccess.update_skill(3, skill3),
            dataaccess.update_skill(4, skill4),
            dataaccess.update_skill(5, skill5)
        ])
        
        if success:
            flash('Content updated successfully!', 'success')
        else:
            flash('Some updates failed. Please try again.', 'error')
            
    except Exception as e:
        flash(f'Error updating content: {str(e)}', 'error')
        print(traceback.format_exc())
    
    return redirect(url_for('home'))

@app.route('/update_about_page_content', methods=['POST'])
@login_required
@admin_required
def update_about_page_content():
    try:
        about_me = request.form.get('about_me')
        who_i_am = request.form.get('who_i_am')
        education1 = request.form.get('education1')
        education2 = request.form.get('education2')
        education3 = request.form.get('education3')
        interests1 = request.form.get('interests1')
        interests2 = request.form.get('interests2')
        connect = request.form.get('connect')
        internship = request.form.get('internship')
        parttime_job = request.form.get('parttime_job')
        skill6 = request.form.get('skill6')
        skill7 = request.form.get('skill7')
        skill8 = request.form.get('skill8')
        skill9 = request.form.get('skill9')
        skill10 = request.form.get('skill10')
        skill11 = request.form.get('skill11')
        skill12 = request.form.get('skill12')
        skill13 = request.form.get('skill13')
        skill14 = request.form.get('skill14')
        skill15 = request.form.get('skill15')
        skill16 = request.form.get('skill16')
        if about_me:
            dataaccess.update_about_page_content(1, about_me)
        if who_i_am:
            dataaccess.update_about_page_content(2, who_i_am)
        if education1:
            dataaccess.update_about_page_content(3, education1)
        if education2:
            dataaccess.update_about_page_content(4, education2)
        if education3:
            dataaccess.update_about_page_content(5, education3)
        if interests1:
            dataaccess.update_about_page_content(6, interests1)
        if interests2:
            dataaccess.update_about_page_content(7, interests2)
        if connect:
            dataaccess.update_about_page_content(8, connect)
        if internship:
            dataaccess.update_about_page_content(9, internship)
        if parttime_job:
            dataaccess.update_about_page_content(10, parttime_job)
            
        if skill6:
            dataaccess.update_skill(6, skill6)
        if skill7:
            dataaccess.update_skill(7, skill7)
        if skill8:
            dataaccess.update_skill(8, skill8)
        if skill9:
            dataaccess.update_skill(9, skill9)
        if skill10:
            dataaccess.update_skill(10, skill10)
        if skill11:
            dataaccess.update_skill(11, skill11)
        if skill12:
            dataaccess.update_skill(12, skill12)
        if skill13:
            dataaccess.update_skill(13, skill13)
        if skill14:
            dataaccess.update_skill(14, skill14)
        if skill15:
            dataaccess.update_skill(15, skill15)
        if skill16:
            dataaccess.update_skill(16, skill16)
            
        flash('Content updated successfully!', 'success')
            
    except Exception as e:
        print(e)
        flash(f'Error updating content: {str(e)}', 'error')
        print(traceback.format_exc())
    
    return redirect(url_for('about'))

@app.route('/update_project_content', methods=['POST'])
@login_required
@admin_required
def update_project_content():
    try:
        project_desc = request.form.get('project_desc')
        collab_text = request.form.get('collab_text')

        success = all([
            dataaccess.update_home_content(4, project_desc),
            dataaccess.update_home_content(5, collab_text)
        ])
        
        if success:
            flash('Project content updated successfully!', 'success')
        else:
            flash('Update failed. Please try again.', 'error')
            
    except Exception as e:
        flash(f'Error updating project content: {str(e)}', 'error')
        print(traceback.format_exc())
    
    return redirect(url_for('home'))

@app.route('/add_skill', methods=['POST'])
@login_required
@admin_required
def add_skill():
    try:
        new_skill = request.form.get('new_skill', '').strip()
        print(f"Received new skill: {new_skill}")  # 调试信息
        
        if not new_skill:
            flash('Skill cannot be empty', 'danger')
            return redirect(url_for('about'))
        
        # 直接使用 Skill 模型插入
        skill = Skill(id=None, skill=new_skill)
        success = skill.insert_skill(new_skill)
        print(f"Insert result: {success}")  # 调试信息
        
        if success:
            flash(f'Skill "{new_skill}" added successfully', 'success')
        else:
            flash(f'Failed to add skill "{new_skill}"', 'danger')
            
    except Exception as e:
        print(f"Error in add_skill: {str(e)}")  # 调试信息
        flash(f'Error adding skill: {str(e)}', 'danger')
    
    return redirect(url_for('about'))

@app.route('/delete_skill/<int:skill_id>', methods=['POST'])
@login_required
@admin_required
def delete_skill(skill_id):
    skill = Skill(id=skill_id, skill=None)
    if skill.delete_skill():
        flash('Skill deleted successfully', 'success')
    else:
        flash('Failed to delete skill', 'danger')
    return redirect(url_for('about'))

@app.route('/add_project', methods=['POST'])
@login_required
@admin_required
def add_project():
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        project_type = request.form.get('project_type')
        website_url = request.form.get('website_url')
        
        # Handle file uploads
        files = request.files.getlist('files')
        saved_files = []
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                # Determine the appropriate folder based on file extension
                ext = filename.rsplit('.', 1)[1].lower()
                if ext == 'pdf':
                    folder = UPLOAD_FOLDER['pdfs']
                elif ext in ['png', 'jpg', 'jpeg']:
                    folder = UPLOAD_FOLDER['images']
                elif ext in ['ppt', 'pptx']:
                    folder = UPLOAD_FOLDER['presentations']
                
                # Create folder if it doesn't exist
                os.makedirs(folder, exist_ok=True)
                
                # Save the file
                file_path = os.path.join(folder, filename)
                file.save(file_path)
                saved_files.append({
                    'path': file_path,
                    'type': ext
                })

        flash('Project added successfully!', 'success')
        
    except Exception as e:
        flash(f'Error adding project: {str(e)}', 'error')
        print(traceback.format_exc())
    
    return redirect(url_for('project'))

@app.route('/insert_teacher_comment', methods=['POST'])
def insert_teacher_comment():
    if session.get('user_role') != 'teacher':
        flash('Only teachers can add comments', 'error')
        return redirect(url_for('home'))
        
    form = teacher_comment_form()
    if form.validate_on_submit():
        comment = form.comment.data
        try:
            TeacherComment.create_comment(comment)
            flash('Comment added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding comment: {str(e)}', 'error')
    else:
        flash('Invalid form submission', 'error')
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    dataaccess.ensure_skill_table() 
    app.run(host='0.0.0.0', port=3000, debug=True)
