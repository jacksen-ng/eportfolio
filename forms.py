from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import ValidationError

PROGRAMMING_LANGUAGES = {
    'python': 'fab fa-python',
    'javascript': 'fab fa-js-square',
    'java': 'fab fa-java',
    'html': 'fab fa-html5',
    'css': 'fab fa-css3-alt',
    'php': 'fab fa-php',
    'ruby': 'fab fa-ruby',
    'nodejs': 'fab fa-node-js',
    'react': 'fab fa-react',
    'angular': 'fab fa-angular',
    'vue': 'fab fa-vuejs',
    'swift': 'fab fa-swift',
    'android': 'fab fa-android',
    'git': 'fab fa-git-alt',
    'threejs': 'fab fa-threejs',
    'tensorflow': 'fas fa-brain',
    'tensor flow': 'fas fa-brain',
    'web development': 'fas fa-code',
    'cloud computing': 'fas fa-cloud',
    'machine learning': 'fas fa-brain',
    'deep learning': 'fas fa-brain',
    'artificial intelligence': 'fas fa-brain',
}

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class insert_content_form(FlaskForm):
    home_content = StringField('Home Content', validators=[DataRequired()])
    submit = SubmitField('Insert')
    
    def copy_from(self, home_content):
        self.home_content.data = home_content.content

class insert_skill_form(FlaskForm):
    skill = StringField('Skill', validators=[
        DataRequired(message="Skill name is required"),
    ])
    
    def validate(self):
        if not super().validate():
            return False
        
        skill = self.skill.data.lower()
        # 添加其他验证规则
        if len(skill) < 2:
            self.skill.errors.append('Skill name must be at least 2 characters long')
            return False
            
        return True
    
    def copy_from(self, skill):
        self.skill.data = skill.skill

class EditContentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    intro = TextAreaField('Introduction', validators=[DataRequired()])
    project_desc = TextAreaField('Project Description', validators=[DataRequired()])  # 新增
    collab_text = TextAreaField('Collaboration Text', validators=[DataRequired()])    # 新增
    skill1 = StringField('Skill 1', validators=[
        DataRequired(),
    ])
    skill2 = StringField('Skill 2', validators=[
        DataRequired(),
    ])
    skill3 = StringField('Skill 3', validators=[
        DataRequired(),
    ])
    skill4 = StringField('Skill 4', validators=[
        DataRequired(),
    ])
    skill5 = StringField('Skill 5', validators=[
        DataRequired(),
    ])
    submit = SubmitField('Save Changes')

    def get_data(self):
        return {
            'name': self.name.data,
            'subtitle': self.subtitle.data,
            'intro': self.intro.data,
            'skills': [
                self.skill1.data,
                self.skill2.data,
                self.skill3.data,
                self.skill4.data,
                self.skill5.data
            ]
        }

    def set_data(self, name, subtitle, intro, project_desc, collab_text, skills):  # 更新
        self.name.data = name
        self.subtitle.data = subtitle
        self.intro.data = intro
        self.project_desc.data = project_desc  
        self.collab_text.data = collab_text    
        self.skill1.data = skills[0]
        self.skill2.data = skills[1]
        self.skill3.data = skills[2]
        self.skill4.data = skills[3]
        self.skill5.data = skills[4]

class ProjectContentForm(FlaskForm):
    project_desc = TextAreaField('Project Description', validators=[DataRequired()])
    collab_text = TextAreaField('Collaboration Text', validators=[DataRequired()])
    submit = SubmitField('Save Project Changes')

    def set_data(self, project_desc, collab_text):
        self.project_desc.data = project_desc
        self.collab_text.data = collab_text
        

class update_about_page_content_form(FlaskForm):
    about_me = TextAreaField('About Me', validators=[DataRequired()])
    who_i_am = TextAreaField('Who I Am', validators=[DataRequired()])
    education1 = StringField('Education 1', validators=[DataRequired()])
    education2 = StringField('Education 2', validators=[DataRequired()])
    education3 = StringField('Education 3', validators=[DataRequired()])
    interests1 = StringField('Interests 1', validators=[DataRequired()])
    interests2 = StringField('Interests 2', validators=[DataRequired()])
    connect = TextAreaField('Lets Connect', validators=[DataRequired()])
    internship = StringField('Internship', validators=[DataRequired()])
    parttime_job = StringField('Part-time Job', validators=[DataRequired()])
    
    submit = SubmitField('Save Changes')
    
    def get_data(self):
        data = {
            'about_me': self.about_me.data,
            'who_i_am': self.who_i_am.data,
            'education1': self.education1.data,
            'education2': self.education2.data,
            'education3': self.education3.data,
            'internship': self.internship.data,
            'parttime_job': self.parttime_job.data,
            'interests1': self.interests1.data,
            'interests2': self.interests2.data,
            'connect': self.connect.data
        }
        return data
        
    def set_data(self, about_me, who_i_am, education1, education2, education3, 
                    interests1, interests2, connect, internship, parttime_job):
        self.about_me.data = about_me
        self.who_i_am.data = who_i_am
        self.education1.data = education1
        self.education2.data = education2
        self.education3.data = education3
        self.interests1.data = interests1
        self.interests2.data = interests2
        self.connect.data = connect
        self.internship.data = internship
        self.parttime_job.data = parttime_job
    
    
    

class insert_about_skill_form(FlaskForm):
    skill = StringField('Skill', validators=[
        DataRequired(message="Skill name is required")
    ])
    
    def validate(self):
        if not super().validate():
            return False
        
        skill = self.skill.data.strip()
        if len(skill) < 2:
            self.skill.errors.append('Skill name must be at least 2 characters long')
            return False
            
        return True
    
    
class teacher_comment_form(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class insert_teacher_comment_form(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def set_data(self, comment):
        self.comment.data = comment
        
    
