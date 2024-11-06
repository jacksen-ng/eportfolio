class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        
    def __repr__(self):
        return "<User %r>" % self.id

class HomeContent:
    def __init__(self, id, content):
        self.id = id
        self.content = content
        
    def update_content(self, new_content):
        from dataaccess import update_home_content
        success = update_home_content(self.id, new_content)
        if success:
            self.content = new_content
        return success
        
    def __repr__(self):
        return "<HomeContent %r>" % self.id

class Skill:
    def __init__(self, id, skill):
        self.id = id
        self.skill = skill
        
    def update_skill(self, new_skill):
        from dataaccess import update_skill
        success = update_skill(self.id, new_skill)
        if success:
            self.skill = new_skill
        return success
    
    def insert_skill(self, new_skill):
        from dataaccess import insert_skill
        try:
            result = insert_skill(new_skill)
            if result:  # result 是新插入的 ID
                self.id = result
                self.skill = new_skill
                return True
            return False
        except Exception as e:
            print(f"Error in Skill.insert_skill: {str(e)}")  # 调试信息
            return False
    
    def delete_skill(self):
        from dataaccess import delete_skill
        success = delete_skill(self.id)
        if success:
            self.id = None
        return success
        
    def __repr__(self):
        return "<Skill %r>" % self.id
    
    def validate(self):
        if not self.skill:
            return False
        return len(self.skill.strip()) >= 2
    
    
    
class AboutPageContent:
    def __init__(self, id, content):
        self.id = id
        self.content = content
        
    def update_content(self, new_content):
        from dataaccess import update_about_page_content
        success = update_about_page_content(self.id, new_content)
        if success:
            self.content = new_content
        return success

class TeacherComment:
    def __init__(self, id, comment):
        self.id = id
        self.comment = comment
        
    @staticmethod
    def create_comment(comment):
        from dataaccess import insert_teacher_comment
        return insert_teacher_comment(comment)