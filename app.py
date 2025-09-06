from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

# 确保上传文件夹存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 百业玩家数据模型
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(200), nullable=True)
    video_filename = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Player {self.name}>'

# 初始化数据库
with app.app_context():
    db.create_all()
    
    # 添加示例数据（如果数据库为空）
    if not Player.query.first():
        sample_players = [
            Player(
                name='李大厨',
                school='厨师',
                description='燕云十六声中最著名的厨师，擅长制作各种珍馐美味，尤其精通红烧肉和清蒸鱼。他的餐馆总是顾客盈门，想要品尝他的手艺需要提前三天预约。'
            ),
            Player(
                name='王铁匠',
                school='铁匠',
                description='技艺精湛的铁匠，能够打造出锋利无比的武器和坚固耐用的防具。他打造的装备在游戏中备受玩家青睐，被称为"兵器之王"。'
            ),
            Player(
                name='张裁缝',
                school='裁缝',
                description='心灵手巧的裁缝，设计和制作的服装不仅美观大方，还能提供额外的属性加成。许多玩家都以拥有一件他制作的衣服为荣。'
            )
        ]
        db.session.add_all(sample_players)
        db.session.commit()

@app.route('/')
def index():
    players = Player.query.all()
    return render_template('index.html', players=players)

@app.route('/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        name = request.form['name']
        school = request.form['school']
        description = request.form['description']
        
        # 处理文件上传
        image_filename = None
        if 'image' in request.files and request.files['image'].filename:
            image = request.files['image']
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        # 处理视频上传
        video_filename = None
        if 'video' in request.files and request.files['video'].filename:
            video = request.files['video']
            video_filename = video.filename
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))
        
        new_player = Player(
            name=name,
            school=school,
            description=description,
            image_filename=image_filename,
            video_filename=video_filename
        )
        
        db.session.add(new_player)
        db.session.commit()
        flash('百业玩家添加成功！')
        return redirect(url_for('index'))
    
    return render_template('add_player.html')

@app.route('/player/<int:player_id>')
def player_detail(player_id):
    player = Player.query.get_or_404(player_id)
    return render_template('player_detail.html', player=player)

@app.route('/delete/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    
    # 删除相关文件（如果有）
    if player.image_filename:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], player.image_filename))
        except:
            pass
    if player.video_filename:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], player.video_filename))
        except:
            pass
    
    db.session.delete(player)
    db.session.commit()
    flash('玩家信息已成功删除！')
    return redirect(url_for('index'))

@app.route('/edit/<int:player_id>', methods=['GET', 'POST'])
def edit_player(player_id):
    player = Player.query.get_or_404(player_id)
    
    if request.method == 'POST':
        player.name = request.form['name']
        player.school = request.form['school']
        player.description = request.form['description']
        
        # 处理图片上传
        if 'image' in request.files and request.files['image'].filename:
            # 删除旧图片
            if player.image_filename:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], player.image_filename))
                except:
                    pass
            # 保存新图片
            image = request.files['image']
            player.image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], player.image_filename))
        
        # 处理视频上传
        if 'video' in request.files and request.files['video'].filename:
            # 删除旧视频
            if player.video_filename:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], player.video_filename))
                except:
                    pass
            # 保存新视频
            video = request.files['video']
            player.video_filename = video.filename
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], player.video_filename))
        
        db.session.commit()
        flash('玩家信息已成功更新！')
        return redirect(url_for('player_detail', player_id=player.id))
    
    return render_template('edit_player.html', player=player)

if __name__ == '__main__':
    # 修改为监听所有网络接口，这样可以通过域名访问
    app.run(debug=True, host='0.0.0.0')