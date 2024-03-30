from flask import Flask, render_template, redirect, url_for, request, Response
from surveillance_system.camera import generate_frames
from surveillance_system.user import login, add_user, manage_user, toggle_admin, delete_user
from surveillance_system.person import upload_picture, admin_dashboard, logs, user_dashboard, delete_person
from surveillance_system.database import view_individual_log

app = Flask(__name__)

# Routes
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/add_user', 'add_user', add_user, methods=['GET', 'POST'])
app.add_url_rule('/manage_user', 'manage_user', manage_user)
app.add_url_rule('/toggle_admin/<int:user_id>', 'toggle_admin', toggle_admin, methods=['POST'])
app.add_url_rule('/delete_user/<int:user_id>', 'delete_user', delete_user, methods=['POST'])
app.add_url_rule('/view_individual_log/<int:id>', 'view_individual_log', view_individual_log, methods=['POST'])
app.add_url_rule('/delete_person/<int:id>', 'delete_person', delete_person, methods=['POST'])
app.add_url_rule('/upload_picture', 'upload_picture', upload_picture, methods=['GET', 'POST'])
app.add_url_rule('/admin_dashboard', 'admin_dashboard', admin_dashboard)
app.add_url_rule('/user_dashboard', 'user_dashboard',user_dashboard)
app.add_url_rule('/logs', 'logs', logs)
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def root():
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
