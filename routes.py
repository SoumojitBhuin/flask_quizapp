from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Required to save plots to memory
import base64
import matplotlib.pyplot as plt
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, current_app, session
from appfile.models import db, User, Subject, Chapter, Quiz, Question,Score
from datetime import datetime 
current_utc_time = datetime.utcnow()
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from urllib.parse import unquote

admin = {"name": "admin", "password": "admin1234"}

# global variable for Admin_dashboard
subname=""
chapname=""
quizno=""

#global variable for User_dashboard
subjectname=""
chaptername=""
quiznum=""


level="subjects"


app = Flask(__name__)


# 🔹 Store session in a server-side file (prevents cookies from persisting)
app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_PERMANENT'] = False  # Should clear on browser close
app.config['SESSION_USE_SIGNER'] = True  # Secure sessions
app.config['SESSION_FILE_DIR'] = './flask_sessions'

Session(app)



def register_routes(app):
    
       
    @app.route('/')  # Home Page
    def index():
  
            
       
       return render_template('index.html')


    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            print(username,password)
            # Admin Login
            if username == admin["name"] and password == admin["password"]:
                session['user_id'] = "admin"  # Store a unique identifier
                session['role'] = "admin"  # Store admin role
                session.permanent = False 
                print(session)
                return redirect(url_for('admin_dashboard', level=admin["name"]))

            # User Login
            user = User.query.filter_by(Username=username).first()
            if user and user.check_password(password):  # Ensure password is correct
            
                session['user_id'] = user.id  # Store user ID in session
                session['role'] = "user"  # Store user role
                flash('Login successful!', 'success')
                return redirect(url_for('user_dashboard'))

            flash('Invalid username or password.', 'danger')

        return render_template('login.html')


    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        username=None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            fullname = request.form['fullname']
            qualification=request.form['qualification']
            dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()  
            new_user = User(Username=username, FullName=fullname,  Password=generate_password_hash(password),Qualification=qualification,DOB=dob)
            
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        if User.query.filter_by(Username=username).first() is not None:
            flash('User with the specified username already exists!', 'danger')
        return render_template('register.html')
    

    @app.route('/navigation')
    def navigation():
        return render_template('navigation.html')
    

    @app.route('/admin_dashboard/<level>',methods=['GET', 'POST'])
    def admin_dashboard(level):
        print("Subject: ",level)
        
        if session['user_id']=='admin':
               subject_list=Subject.query.all()
               
               return render_template('admindashboard.html',level="subjects",data=subject_list, search_query="None")
        else:
            flash('Admin not in session','warning')
            return redirect(url_for('login'))
        
    

        
    @app.route('/admin_dashboard/<sub_name>/<level>',methods=['GET', 'POST'])
    def admin_dashboard_chapter(level,sub_name):
        print("Chapter: ",level)
        
        global subname
        subname=sub_name
        if session['user_id']=='admin':
            
            curr_sub=Subject.query.filter_by(Name=subname).first()
            chapter_list=curr_sub.chaps
           
            
            return render_template('admindashboard.html',level=level, data=chapter_list)
        else:
            flash('Admin not in session','warning')
            return redirect(url_for('login'))
        
        
    @app.route('/admin_dashboard/<subject>/<chap_name>/<level>',methods=['GET', 'POST'])
    def admin_dashboard_quiz(level,chap_name,subject):
        print("Quiz: ",level)
        global subname
        global chapname
        chapname=chap_name
        print(subname)
        if session['user_id']=='admin':
            curr_chap=Chapter.query.filter_by(Name=chapname).first()
            quiz_list=curr_chap.Quizzes
            return render_template('admindashboard.html',level=level, data=quiz_list)
        else:
            flash('Admin not in session','warning')
            return redirect(url_for('login'))
        
    @app.route('/admin_dashboard/<subject>/<chapter>/<quiz_no>/<level>',methods=['GET', 'POST'])
    def admin_dashboard_questions(level,quiz_no,chapter,subject):
        print("Questions: ",level)
        global subname
        global chapname
        global quizno
        quizno=quiz_no
        print(subname)
        if session['user_id']=='admin':
        
            curr_quiz=Quiz.query.filter_by(id=quizno).first()
            ques_list=curr_quiz.Questions
            
            return render_template('admindashboard.html',level=level, data=ques_list)
        else:
            flash('Admin not in session','warning')
            return redirect(url_for('login'))

    @app.route('/add_item/<level>', methods=['POST'])
    def add_item(level):
        global subname
        global chapname
        global quizno
        print("level: ",level)
        print("subName: ",subname)
        print("chapName: ",chapname)
        print("quizNo: ",quizno)
        if(level=="subjects"):
            
            new_item = request.form['new_item']
            desc=request.form['Description']
            print(new_item,desc)
            new_sub=Subject(Name=new_item, Description=desc)
            db.session.add(new_sub)
            db.session.commit()
            return redirect(url_for('admin_dashboard', level=level))

            
        elif(level=="chapter"):
            
            new_item = request.form['new_item']
            desc=request.form['Description']
            print(new_item,desc,subname)
            old_subject=Subject.query.filter_by(Name=subname).first()
            print(old_subject.Name)
            new_chap=Chapter(Name=new_item, Description=desc, sub_id=old_subject.id)
            db.session.add(new_chap)
            db.session.commit()
            return redirect(url_for('admin_dashboard_chapter', level=level, sub_name=subname))


        elif(level=="quizzes"):
            new_item = request.form['new_item']
            date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            time = request.form['time']
            print(new_item)
            curr_chap=Chapter.query.filter_by(Name=chapname).first()
            curr_sub=Subject.query.filter_by(Name=subname).first()
            new_quiz=Quiz(quiz_no=new_item,date_of_quiz=date,time_duration=time,sub_id=curr_sub.id, chap_id=curr_chap.id)
            db.session.add(new_quiz)
            db.session.commit()
            return redirect(url_for('admin_dashboard_quiz', level=level, chap_name=chapname, subject='subjects'))

        elif(level=="questions"):
            question = request.form['question']
            opt1 = request.form['option 1']
            opt2 = request.form['option 2']
            opt3 = request.form['option 3']
            opt4 = request.form['option 4']
            corr_op = request.form['correct_option']
            print(question,"\n",opt1,"\n",opt2,"\n",opt3,"\n",opt4, "\n",corr_op)
            
            curr_quiz=Quiz.query.filter_by(id=quizno).first()
            curr_chap=Chapter.query.filter_by(Name=chapname).first()
            curr_sub=Subject.query.filter_by(Name=subname).first()
            
            new_ques=Question(Question_Statement=question, Option1=opt1, Option2=opt2, Option3=opt3, Option4=opt4, quiz_id=curr_quiz.id, chap_id=curr_chap.id, sub_id=curr_sub.id, correct_option=corr_op)
            db.session.add(new_ques)
            db.session.commit()
                        
            return redirect(url_for('admin_dashboard_questions', level=level, chapter='chapter', subject='subjects',quiz_no=quizno))
        return redirect(url_for('admin_dashboard', level=level))


    @app.route('/update_item/<level>/<name>', methods=['POST'])
    def update_item(level, name):
        global subname
        global chapname
        global quizno
        print("level: ",level)
        print("subName: ",subname)
        print("chapName: ",chapname)
        print("quizNo: ",quizno)
        if level == "subjects":
            subject = Subject.query.filter_by(Name=name).first()
            
            if subject:
                # Add debug prints
                print("Updating subject:", name)
                print("Form data:", request.form)
                subject.Name = request.form.get('subname')
                subject.Description = request.form.get('description')
                try:
                    db.session.commit()
                    print("Update successful")
                    flash('Subject updated successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    print("Update failed:", str(e))
                    flash('Error updating subject.', 'error')
            return redirect(url_for('admin_dashboard', level=level))

        elif level == "chapter":
            chapter = Chapter.query.filter_by(Name=name).first()
            if chapter:
                chapter.Name = request.form.get('chapname')
                chapter.Description = request.form.get('description')
                try:
                    db.session.commit()
                    flash('Chapter updated successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash('Error updating chapter.', 'error')
            return redirect(url_for('admin_dashboard_chapter', level=level, sub_name=subname))

        elif level == "quizzes":
            quiz = Quiz.query.filter_by(id=name).first()
            print(quiz.quiz_no)
            if quiz:
                quiz.quiz_no = request.form.get('quizno')
                quiz.time_duration = request.form.get('time')
                quiz.date_of_quiz = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
                try:
                    db.session.commit()
                    flash('Quiz updated successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash('Error updating quiz.', 'error')
            return redirect(url_for('admin_dashboard_quiz', level=level, chap_name=chapname, subject='subjects'))

        

        elif level == "questions":
            decoded_name = unquote(name)  # Decode the URL-encoded name
            decoded_name = decoded_name.replace('%2F', '/')  # Manually handle slashes
            print(decoded_name)
            question = Question.query.filter_by(Question_Statement=decoded_name).first()
            if question:
                question.Question_Statement = request.form.get('question')
                question.Option1 = request.form.get('option 1')  # Remove space in field names
                question.Option2 = request.form.get('option 2')
                question.Option3 = request.form.get('option 3')
                question.Option4 = request.form.get('option 4')
                question.correct_option = request.form.get('correct_option')
                try:
                    db.session.commit()
                    flash('Question updated successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash('Error updating question.', 'error')
            return redirect(url_for('admin_dashboard_questions', level=level, subject='subject', chapter='chapter', quiz_no=quizno))



    @app.route('/delete_item/<level>/<name>', methods=['POST'])
    def delete_item(level, name):
        global subname
        global chapname
        global quizno

        print(f"Delete attempt - Level: {level}, Name: {name}")  # Debug log

        try:
            if level == "subjects":
                subject = Subject.query.filter_by(Name=name).first()
                if subject:
                    print(f"Found subject: {subject.Name}")  # Debug log
                    db.session.delete(subject)
                    db.session.commit()
                    flash('Subject deleted successfully!', 'success')
                else:
                    flash('Subject not found.', 'error')
                return redirect(url_for('admin_dashboard', level=level))

            elif level == "chapter":
                chapter = Chapter.query.filter_by(Name=name).first()
                if chapter:
                    print(f"Found chapter: {chapter.Name}")  # Debug log
                    db.session.delete(chapter)
                    db.session.commit()
                    flash('Chapter deleted successfully!', 'success')
                else:
                    flash('Chapter not found.', 'error')
                return redirect(url_for('admin_dashboard_chapter', level=level, sub_name=subname))

            elif level == "quizzes":
                quiz = Quiz.query.filter_by(id=name).first()
                if quiz:
                    print(f"Found quiz: {quiz.quiz_no}")  # Debug log
                    db.session.delete(quiz)
                    db.session.commit()
                    flash('Quiz deleted successfully!', 'success')
                else:
                    flash('Quiz not found.', 'error')
                return redirect(url_for('admin_dashboard_quiz', level=level, chap_name=chapname, subject='subjects'))

            elif level == "questions":
                decoded_name = unquote(name)
                print(decoded_name)
                print(f"Searching for question with statement: {name}")  # Debug log
                question = Question.query.filter_by(Question_Statement=decoded_name).first()
                if question:
                    print(f"Found question: {question.Question_Statement}")  # Debug log
                    db.session.delete(question)
                    db.session.commit()
                    flash('Question deleted successfully!', 'success')
                else:
                    print("Question not found in database")  # Debug log
                    flash('Question not found.', 'error')
                return redirect(url_for('admin_dashboard_questions', level=level, quiz_no=quizno, chapter=chapname, subject=subname))

        except Exception as e:
            print(f"Error during deletion: {str(e)}")  # Debug log
            db.session.rollback()
            flash(f'Error deleting item: {str(e)}', 'error')
            return redirect(url_for('admin_dashboard', level=level))

        return redirect(url_for('admin_dashboard', level=level))
    
    
    @app.route('/search/<level>', methods=['POST'])
    def search(level):
        search_query = request.form.get('search', '').strip()
        print(f"Search query for {level}: {search_query}")  # Debug log

        try:
            if level == "subjects":
                results = Subject.query.filter(Subject.Name.ilike(f'%{search_query}%')).all()
                return render_template('admindashboard.html', level=level, data=results, search_query=search_query)

            elif level == "chapter":
                results = Chapter.query.filter(
                    Chapter.Name.ilike(f'%{search_query}%'),
                    Chapter.sub_id == Subject.query.filter_by(Name=subname).first().id
                ).all()
                return render_template('admindashboard.html', level=level, data=results, search_query=search_query)

            elif level == "quizzes":
                chapter = Chapter.query.filter_by(Name=chapname).first()
                results = Quiz.query.filter(
                    Quiz.quiz_no.ilike(f'%{search_query}%'),
                    Quiz.chap_id == chapter.id
                ).all()
                return render_template('admindashboard.html', level=level, data=results, search_query=search_query)

        except Exception as e:
            print(f"Search error: {str(e)}")  # Debug log
            flash('Error performing search.', 'error')
            return redirect(url_for('admin_dashboard', level=level))



    @app.route('/logout')
    def logout():
        session.clear()  # ✅ Completely clear session
        flash('You have been logged out.', 'success')
        return redirect(url_for('login'))


    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if 'user_id' not in session:
            flash('Please log in to access your profile.', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found.', 'danger')
            session.clear()
            return redirect(url_for('login'))

        if request.method == 'POST':
            username = request.form.get('username')
            name = request.form.get('name')
            old_password = request.form.get('opassword')
            new_password = request.form.get('npassword')
            
            print(f"Update attempt - Username: {username}, Name: {name}")  # Debug print

            # Verify old password
            if not check_password_hash(user.Password, old_password):
                flash('Current password is incorrect.', 'danger')
                return render_template('profile.html', user=user)

            try:
                # Update user information
                user.Username = username
                user.FullName = name
                
                # Only update password if a new one is provided
                if new_password:
                    user.Password = generate_password_hash(new_password)
                
                db.session.commit()
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('user_dashboard'))
                
            except Exception as e:
                db.session.rollback()
                print(f"Error updating profile: {e}")
                flash('An error occurred while updating your profile.', 'danger')
                return render_template('profile.html', user=user)

        return render_template('profile.html', user=user)


    @app.route('/user_dashboard', methods=['GET', 'POST'])
    def user_dashboard():
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user:
                #Get user's scores ordered by date
                scores = Score.query.filter_by(user_id=user.id).order_by(Score.Time.desc()).all()
                
                dates = []
                percentages = []
                total_questions = []  
                
                for score in scores:
                    dates.append(score.Time.strftime('%Y-%m-%d %H:%M'))
                    quiz = Quiz.query.get(score.quiz_id)
                    subject = Subject.query.get(score.sub_id)
                    chapter = Chapter.query.get(score.chap_id)
                    
                    # Calculate total questions and percentage
                    if quiz and hasattr(quiz, 'Questions'):
                        questions_count = len(quiz.Questions)
                        percentage = (score.Total_Scored / questions_count) * 100
                    else:
                        questions_count = 0
                        percentage = 0
                    
                    total_questions.append(questions_count)  # Add to list
                    percentages.append(percentage)

                    score.subject = subject
                    score.chapter = chapter
                    score.quiz = quiz
                
                subjects = Subject.query.all()  # Fetch all subjects
                selected_subject = None
                
                
                        
                if request.method == 'POST':
                    subject_id = request.form.get('subject_id')
                    if subject_id:
                        selected_subject = Subject.query.get(subject_id)

                        print(selected_subject)
                
                        scores1=Score.query.filter_by(sub_id=selected_subject.id , user_id=session['user_id']).all()
                        print(scores1)
                        store={}
                
                        for score1 in scores1:
                            print(score1.Chapter.Name)
                            if score1.Chapter.Name not in store.keys():
                                store[score1.Chapter.Name]={}
                                print(store)
                            #for adding none to the the scores of chapters for which the current quiz doesnot exists
                            for i in store.keys():
                                if i!=score1.Chapter.Name:
                                    if score1.Quiz.quiz_no not in store[i].keys():
                                        store[i][score1.Quiz.quiz_no]=None
                                else:
                                    
                                    store[score1.Chapter.Name][score1.Quiz.quiz_no]=score1.Total_Scored
                                    
                            
                            
                        print(store)
                        
                    plt.figure(figsize=(10, 6))
                    for chapter, quiz_data in store.items():
                        quiz_numbers = sorted(quiz_data.keys())  # Sorting quiz numbers
                        scores_list = [quiz_data[q] if quiz_data[q] is not None else 0 for q in quiz_numbers]  # Handling None values

                        plt.plot(quiz_numbers, scores_list, marker='o', label=chapter)  # Line for each chapter

                    plt.xlabel("Quiz Number")
                    plt.ylabel("Score")
                    plt.title(f"Performance in {selected_subject.Name}")
                    plt.legend(title="Chapters")  # Show legend
                    plt.grid(True)  # Add grid lines

                    
                    

                    # Save plot as image
                    buffer = BytesIO()
                    plt.savefig(buffer, format="png")
                    buffer.seek(0)
                    plot_url = base64.b64encode(buffer.getvalue()).decode()
                    plt.close()

                    # ✅ Ensure `scores` is still passed correctly
                    return render_template(
                        'user_dashboard.html',
                        user=user,
                        subjects=subjects,
                        selected_subject=selected_subject,
                        scores=scores,  # Keep original scores
                        total_questions=total_questions,
                        percentages=percentages,
                        plot_url=plot_url
                    )
                
                    
                                               
                #Generate plot
                
                plot_url = None

                return render_template('user_dashboard.html',
                                   user=user,
                                   subjects=subjects,
                                   selected_subject=selected_subject,
                                   scores=scores,
                                   total_questions=total_questions,
                                   percentages=percentages,
                                   plot_url=plot_url)
            flash('User not found', 'error')
            return redirect(url_for('login'))
        
        flash('Please login first', 'warning')
        return redirect(url_for('login'))

    @app.route('/quiz')
    def quiz_home():
        if 'user_id' not in session:
            flash('Please log in to access quizzes.', 'warning')
            return redirect(url_for('login'))
        
        subjects = Subject.query.all()
        for subject in subjects:
           print("Subject: ", subject.Name) 
        return render_template('quiz.html', level='subjects', data=subjects)

    @app.route('/quiz/<subject_name>')
    def quiz_chapters(subject_name):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        global subjectname
        subjectname=subject_name
        print("Subject in chapter_userdashboard: ",subjectname)
        
        curr_sub= Subject.query.filter_by(Name=subject_name).first()
        chapter_list=curr_sub.chaps
        for chap in chapter_list:
            print("chapter: ",chap.Name)  
        
        return render_template('quiz.html', 
                             level='chapters', 
                             data=chapter_list)

    @app.route('/quiz/<subject_name>/<chapter_name>')
    def quiz_quizzes(subject_name, chapter_name):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        global subjectname
        global chaptername
        chaptername=chapter_name
        
        print("Chapter in quiz_userdashboard: ",chaptername)
        
        curr_chap = Chapter.query.filter_by(
            Name=chapter_name).first() 
        
        quizzes_list=curr_chap.Quizzes
        
        for quiz in quizzes_list:
            print("Quiz: ",quiz.quiz_no) 
        
        return render_template('quiz.html', 
                             level='quizzes', 
                             data=quizzes_list)

    @app.route('/quiz/<subject_name>/<chapter_name>/<quiz_id>', methods=['GET', 'POST'])
    def quiz_questions(subject_name, chapter_name, quiz_id):
        global quiznum
        quiznum=quiz_id
        if 'user_id' not in session:
            return redirect(url_for('login'))

        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return "Quiz not found", 404

        question_list = quiz.Questions
        time_duration = (quiz.time_duration) if quiz.time_duration else 10
        print(time_duration)
        if request.method == 'POST':
            print("Successfully posted")
            answers = {key: value for key, value in request.form.items()}
            print(answers)

        return render_template('quiz.html', level='questions', data=question_list,time=time_duration, quiz_id=quiz_id)

    
    

    @app.route('/submit_quiz', methods=['POST'])
    def submit_quiz():
        global subjectname
        global chaptername
        global quiznum
        
        score=0
        
        quiz = Quiz.query.filter_by(id=quiznum).first()
        print(quiz.quiz_no)
        
        if not quiz:
            flash('Quiz not found.', 'danger')
            return redirect(url_for('quiz_home'))
        curr_chap = Chapter.query.filter_by(Name=chaptername).first()
        if not curr_chap:
            flash('Chapter not found.', 'danger')
            return redirect(url_for('quiz_home'))
        
        print(curr_chap.id)
        curr_sub = Subject.query.filter_by(Name=subjectname).first()
        if not curr_sub:
            flash('Subject not found.', 'danger')
            return redirect(url_for('quiz_home'))
        
        questions=quiz.Questions
        total_questions=len(questions)
        print("Total Questions: ",total_questions)
        
        # Add debugging for form data
        print("Form data received:", request.form)
        user_answers={}
        #For calculating Score
        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            correct_answer = question.correct_option
            
            # Detailed debug output
            print("\n--- Question Details ---")
            print(f"Question ID: {question.id}")
            print(f"Question: {question.Question_Statement}")
            print(f"User answer (raw): '{user_answer}'")
            print(f"Correct answer (raw): '{correct_answer}'")
            
            # Clean and compare answers
            user_answer = str(user_answer).strip() if user_answer else ''
            correct_answer = str(correct_answer).strip()
            
            print(f"User answer (cleaned): '{user_answer}'")
            print(f"Correct answer (cleaned): '{correct_answer}'")
            print(f"Match?: {user_answer == correct_answer}")

            if user_answer == correct_answer:
                score += 1
                print(f"✓ Correct! Score increased to: {score}")
            else:
                print("✗ Incorrect")

        print(f"\nFinal Score: {score}/{total_questions}")

        # Generate the charts
        try:
            # Create figure with two subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            # Bar Chart (Left)
            categories = ['Correct', 'Incorrect']
            scores = [score, total_questions - score]
            colors = ['#2ecc71', '#e74c3c']
            ax1.bar(categories, scores, color=colors)
            ax1.set_title('Score Distribution')
            ax1.set_ylabel('Number of Questions')

            # Pie Chart (Right)
            correct_percentage = (score / total_questions) * 100
            incorrect_percentage = ((total_questions - score) / total_questions) * 100
            sizes = [correct_percentage, incorrect_percentage]
            labels = [f'Correct\n({score})', f'Incorrect\n({total_questions - score})']
            ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
            ax2.set_title('Score Percentage')
            ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Force integer y-axis

            # Adjust layout and convert to base64
            plt.tight_layout()
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            plot_url = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()

            print("Charts generated successfully")
        except Exception as e:
            print(f"Error generating charts: {e}")
            plot_url = None
        
        try:
            #Storing the score in the database
            quiz_score = Score(user_id=session['user_id'], Total_Scored=score, chap_id=curr_chap.id, sub_id=curr_sub.id, quiz_id=quiznum, Time=datetime.now())
            db.session.add(quiz_score)
            db.session.commit()
        except Exception as e:
            print(f"Error saving score: {e}")
            db.session.rollback()
            flash('Error saving your score', 'error')

    
    
        return render_template('scores.html',
                              Total_Scored=score,
                              total_questions=total_questions,
                              plot_url=plot_url,
                              quiz=quiz)

    @app.route('/user_management')
    def user_management():
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))

        # Get search parameters
        name_search = request.args.get('name', '').strip()
        username_search = request.args.get('username', '').strip()
        
        # Build base query
        query = User.query
        
        # Apply filters if search parameters exist
        if name_search:
            query = query.filter(User.FullName.ilike(f'%{name_search}%'))
        if username_search:
            query = query.filter(User.Username.ilike(f'%{username_search}%'))
        
        users = query.all()
        
        # Process each user's data
        for user in users:
            # Get scores ordered by date
            scores = Score.query.filter_by(user_id=user.id)\
                            .order_by(Score.Time.desc())\
                            .all()
            
            user.scores = []
            total_percentage = 0
            score_count = 0
            dates = []
            percentages = []
            
            for score in scores:
                # Get related data
                quiz = Quiz.query.get(score.quiz_id)
                subject = Subject.query.get(score.sub_id)
                chapter = Chapter.query.get(score.chap_id)
                
                if quiz and hasattr(quiz, 'Questions'):
                    questions_count = len(quiz.Questions)
                    percentage = (score.Total_Scored / questions_count) * 100
                    
                    # Add computed values to score object
                    score.total_questions = questions_count
                    score.percentage = percentage
                    score.quiz = quiz
                    score.subject = subject
                    score.chapter = chapter
                    
                    total_percentage += percentage
                    score_count += 1
                    
                    # Collect data for chart
                    dates.append(score.Time)
                    percentages.append(percentage)
                
                user.scores.append(score)
            
            # Calculate user statistics
            user.average_score = total_percentage / score_count if score_count > 0 else 0
            user.last_activity = scores[0].Time if scores else None
            
            # Generate progress chart
            if dates and percentages:
                plt.figure(figsize=(10, 5))
                plt.clf()  # Clear previous plots
                
                # Create line plot
                plt.plot(dates, percentages, marker='o', color='#007bff', 
                        linewidth=2, markersize=8)
                
                # Customize plot
                plt.title(f'Progress Chart - {user.FullName}', pad=20, fontsize=12)
                plt.ylabel('Score Percentage')
                plt.xlabel('Quiz Date')
                plt.grid(True, linestyle='--', alpha=0.3)
                
                
                # Rotate date labels
                plt.xticks(rotation=45, ha='right')
                
                # Adjust layout
                plt.tight_layout()
                
                # Convert plot to base64 string
                buffer = BytesIO()
                plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
                buffer.seek(0)
                user.plot_url = base64.b64encode(buffer.getvalue()).decode('utf-8')
                plt.close('all')  # Close all figures
            else:
                user.plot_url = None

        return render_template('user_management.html', users=users)