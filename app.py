
from model import User,db,app,Ystable,Jltable
from flask import Flask, render_template,request,redirect,g,session,make_response,send_file,Response,flash,url_for
import sqlite3
import pandas as pd
from typing import Any, Dict, Optional
import io
from datetime import datetime

app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'

db.create_all()  # 根据模型创建表


#每次路由之前
@app.before_request
def before_request():
    # if request.script_root == "/static":
    # return
    # if not request.path.endswith('/login'):  # 判断当前所在url是否是/cms/login/，不是代表不在后台登录界面
    # username = session.get('username')  # 登陆之后，获取登录时候记录的session中的user_id
    # if not username:  # 若没有user_id，说明登录不成功
    # return redirect('/login')

    # if 'logged_in' not in session and request.endpoint not in ('login', 'static'):
    # return redirect('/login')

    # if request.path == "/login":
    # print(request.path)
    # return None
    # 放行的url
    url = request.path
    pass_url = ['/login', '/register', '/modify_mm']
    if url in pass_url:
        pass
    else:
        if not session.get("username") and request.endpoint not in ('login', 'static'):
            return redirect("/login")


@app.route('/logout')
def logout():
    session.pop('username', None)   # 不需要检查用户是否已经登入，因为如果不存在则什么都不做
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/login',methods = ["GET","POST"])
def login():
    users = User.query.all()
    #判断是不是post请求
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username:
            if password:
                if not any(i.username == username for i in users):
                    return render_template('login.html',msg='用户名不存在！')
                else:
                    for j in users:
                        if j.username == username:
                            if j.mm == password:
                                #成功的话给一个session
                                session["username"] = username
                                return redirect('/home')
                            else:
                                return render_template('login.html',msg='密码错误!')
            else:
                return render_template('login.html', msg='请输入密码!')
        else:
            return render_template('login.html', msg='请输入用户名!')

    return render_template('login.html')


@app.route('/register',methods = ["GET","POST"])
def register():
    # 链接数据库看是不是有账号密码，正不正确
    users = User.query.all()

    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if username:
            if not any(i.username == username for i in users):
                if password1:
                    if password2:
                        if password1 == password2:
                            #全部符合条件，存入数据库，注册成功
                            conn1 = sqlite3.connect('flask.db')  # 连接数据库，没有的话会创建
                            cur1 = conn1.cursor()  # 创建游标
                            # 添加数据
                            # 添加一行数据
                            try:
                                a = User(username, password1)
                                db.session.add(a)
                                db.session.commit()
                                print('数据添加成功！')
                                return render_template('register.html',msg='注册成功!')
                            except Exception as e:
                                print(str(e))

                        else:
                            return render_template('register.html',msg='两次密码不一致!')
                    else:
                        return render_template('register.html', msg='请再次输入密码!')
                        #print('请再次输入密码！')
                else:
                    return render_template('register.html', msg='请输入密码!')
                    #print('请输入密码！')
            else:
                return render_template('register.html', msg='此用户名已存在!')
        else:
            return render_template('register.html', msg='请输入用户名!')
            #print('请输入用户名！')


    return render_template('register.html')
#修改密码
@app.route('/modify_mm',methods = ["GET","POST"])
def modify_mm():
    # 链接数据库看是不是有账号密码，正不正确
    users = User.query.all()

    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1') #旧密码
        password2 = request.form.get('password2') #新密码
        password3 = request.form.get('password3') #再次输入密码
        if username:
            if not any(i.username == username for i in users):
                return render_template('modify_mm.html', msg='用户名不存在!')
            else:
                if password1:
                    for j in users:
                        if j.username == username:
                            if j.mm == password1:
                                if password2:
                                    if password3:
                                        if password2 == password3:
                                            #全部符合条件，修改数据库数据
                                            j.mm = password2
                                            db.session.commit()
                                            return render_template('modify_mm.html', msg='密码修改成功!')

                                        else:
                                            return render_template('modify_mm.html', msg='两次密码不一致!')
                                    else:
                                        return render_template('modify_mm.html', msg='请再次输入新密码!')
                                else:
                                    return render_template('modify_mm.html', msg='请输入新密码!')
                            else:
                                return render_template('modify_mm.html', msg='旧密码错误!')
                else:
                    return render_template('modify_mm.html', msg='请输入旧密码!')


        else:
            return render_template('modify_mm.html', msg='请输入用户名!')




    return render_template('modify_mm.html')








#进入主页面
@app.route('/home')
def home():
    return render_template('home.html')

#原始记录页面
@app.route('/yuanshi/')
def yuanshi():

    page = request.args.get('page',1)
    page = int(page)
    info_yuanshi = Ystable.query.order_by(Ystable.id).paginate(page,18)
    #print(info_yuanshi)
    #info_yuanshi = Ystable.query.all()
    return render_template('yuanshi.html', **locals())
#记录页面
@app.route('/jilu/')
def jilu():
    page = request.args.get('page', 1)
    page = int(page)
    info_jilu = Jltable.query.order_by(Jltable.id).paginate(page, 18)
    # print(info_yuanshi)
    # info_yuanshi = Ystable.query.all()
    return render_template('jilu.html', **locals())



#作者页面
@app.route('/author')
def author():
    return render_template('author.html')

#增加原始记录
@app.route('/addyuanshi',methods = ["GET","POST"])
def addyuanshi():
    page = request.args.get('page', 1)
    page = int(page)
    info_yuanshi = Ystable.query.order_by(Ystable.id).paginate(page, 18)
    #获取总页数
    total_page = info_yuanshi.pages
    #print(total)
    if request.method == 'POST':
        date = request.form.get('date')
        name = request.form.get('name')
        weight = request.form.get('weight')
        site = request.form.get('site')

        # 全部符合条件，存入数据库
        try:
            a = Ystable(date, name,weight,site)
            db.session.add(a)
            db.session.commit()
            return redirect('/yuanshi/?page=%s'%total_page)
        except Exception as e:
            print(e)

    return render_template('addyuanshi.html')





#删除原始记录
@app.route('/deleinfoyuanshi')
def deleinfoyuanshi():
    yuanshi_id = int(request.args.get('id'))

    print(yuanshi_id)
    #根据余数获取当前页
    ys = yuanshi_id%18
    if ys == 0:
        page_now = yuanshi_id/18
    else:
        page_now = int(yuanshi_id / 18)+1
    print(page_now)
    del_ys = Ystable.query.filter_by(id=yuanshi_id).first()
    if del_ys is not None:
        db.session.delete(del_ys)
        db.session.commit()
    #重排id
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[-1])
    c = conn.cursor()
    q = 'update yuanshi set id=id-1 where id>' + str(yuanshi_id)
    c.execute(q)
    conn.commit()

    return redirect('/yuanshi/?page=%d'%page_now)


#修改原始记录
@app.route('/modifyinfoyuanshi',methods = ["GET","POST"])
def modifyinfoyuanshi():
    #获取id
    yuanshi_id = int(request.args.get('id'))

    #print(yuanshi_id)
    # 根据余数获取当前页
    ys = yuanshi_id % 18
    if ys == 0:
        page_now = yuanshi_id / 18
    else:
        page_now = int(yuanshi_id / 18) + 1
    #获取这个id所有的信息
    update_yuanshi = Ystable.query.get(yuanshi_id)
    # 下面是修改后的数据
    if request.method == 'POST':
        dateyuanshimodify = request.form.get('date')
        nameyuanshimodify = request.form.get('name')
        weightyuanshimodify = request.form.get('weight')
        siteyuanshimodify = request.form.get('site')
        #修改数据
        update_yuanshi.date = dateyuanshimodify
        update_yuanshi.name = nameyuanshimodify
        update_yuanshi.num = weightyuanshimodify
        update_yuanshi.site = siteyuanshimodify
        db.session.commit()
        return redirect('/yuanshi/?page=%d'%page_now)



    return render_template('modifyinfoyuanshi.html', dateyuanshi=update_yuanshi.date, nameyuanshi=update_yuanshi.name,
                           weightyuanshi=update_yuanshi.num, siteyuanshi=update_yuanshi.site)




############################################################################################################
#下面是对登记记录进行处理
#增加登记记录
@app.route('/addjilu',methods = ["GET","POST"])
def addjilu():
    page = request.args.get('page', 1)
    page = int(page)
    info_jilu = Jltable.query.order_by(Jltable.id).paginate(page, 18)
    # 获取总页数
    total_page = info_jilu.pages

    if request.method == 'POST':
        date = request.form.get('date')
        name = request.form.get('name')
        weight = request.form.get('weight')
        site = request.form.get('site')
        person = request.form.get('person')
        inout = request.form.get('inout')

        # 全部符合条件，存入数据库
        try:
            a = Jltable(date, name,weight,site,person,inout)
            db.session.add(a)
            db.session.commit()
            return redirect('/jilu/?page=%s'%total_page)
        except Exception as e:
            print(e)

    return render_template('addjilu.html')

#删除原始记录
@app.route('/deleinfojilu')
def deleinfojilu():
    jilu_id = int(request.args.get('id'))
    # 根据余数获取当前页
    jl = jilu_id % 18
    if jl == 0:
        page_now = jilu_id / 18
    else:
        page_now = int(jilu_id / 18) + 1
    del_ys = Jltable.query.filter_by(id=jilu_id).first()
    if del_ys is not None:
        db.session.delete(del_ys)
        db.session.commit()
    #重排id
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[-1])
    c = conn.cursor()
    q = 'update jilu set id=id-1 where id>' + str(jilu_id)
    c.execute(q)
    conn.commit()

    return redirect('/jilu/?page=%d'%page_now)


#修改原始记录
@app.route('/modifyinfojilu',methods = ["GET","POST"])
def modifyinfojilu():
    #获取id
    jilu_id = int(request.args.get('id'))
    # 根据余数获取当前页
    jl = jilu_id % 18
    if jl == 0:
        page_now = jilu_id / 18
    else:
        page_now = int(jilu_id / 18) + 1
    #获取这个id所有的信息
    update_jilu = Jltable.query.get(jilu_id)
    # 下面是修改后的数据
    if request.method == 'POST':
        datejilumodify = request.form.get('date')
        namejilumodify = request.form.get('name')
        weightjilumodify = request.form.get('weight')
        sitejilumodify = request.form.get('site')
        personjilumodify = request.form.get('person')
        inoutjilumodify = request.form.get('inout')
        #修改数据
        update_jilu.date = datejilumodify
        update_jilu.name = namejilumodify
        update_jilu.num = weightjilumodify
        update_jilu.site = sitejilumodify
        update_jilu.people = personjilumodify
        update_jilu.in_out = inoutjilumodify
        db.session.commit()
        return redirect('/jilu/?page=%d'%page_now)



    return render_template('modifyinfojilu.html', datejilu=update_jilu.date, namejilu=update_jilu.name,
                           weightjilu=update_jilu.num, sitejilu=update_jilu.site,personjilu = update_jilu.people)


#通过物品名查询原始记录信息
@app.route("/serchyuanshi",methods = ["GET","POST"])
def serchserchyuanshi():
    if request.method == 'POST':
        name = request.form.get('word')
        print(name)
        # 精确查找
        #get_yuanshi = Ystable.query.filter_by(name=name).all()
        #模糊查找
        page = request.args.get('page', 1)
        page = int(page)
        info_yuanshi = Ystable.query.filter(Ystable.name.like("%%%%%s%%%%"%name)).paginate(page, 18)

        #print(get_yuanshi)
        return render_template('/yuanshi.html',**locals())

#通过物品名查询登记记录信息
@app.route("/serchjilu",methods = ["GET","POST"])
def serchjilu():
    if request.method == 'POST':
        name = request.form.get('word')
        #print(name)
        #精确查找
        #get_jilu = Jltable.query.filter_by(name=name).all()
        # 模糊查找
        page = request.args.get('page', 1)
        page = int(page)
        info_jilu = Jltable.query.filter(Jltable.name.like("%%%%%s%%%%" % name)).paginate(page, 18)

        return render_template('/jilu.html',**locals())




#下载的写法Ctrl+C/Ctrl+V

# 关闭Flask的ASCII编码
# 防止中文转换成ASCII编码
app.config["JSON_AS_ASCII"] = False

# 写一个函数，设置响应头配置以及生成文件名
def generate_download_headers(
        extension: str, filename: Optional[str] = None
) -> Dict[str, Any]:
    filename = filename if filename else datetime.now().strftime("%Y%m%d_%H%M%S")
    content_disp = f"attachment; filename={filename}.{extension}"
    headers = {"Content-Disposition": content_disp}
    return headers



#原始记录保存
@app.route('/download_yuanshi')
def download_file():
    info_yuanshi = Ystable.query.all()
    yuanshi_data = []
    for i in info_yuanshi:
        xh = i.id  #序号
        date = i.date
        name = i.name
        num = i.num
        site = i.site
        yuanshi_data.append([xh,date,name,num,site])
    df = pd.DataFrame(yuanshi_data)
    df.columns=['序号','日期','物品名','重量','位置']

    byte_file = io.BytesIO()  # BytesIO实现了在内存中读写bytes，创建一个BytesIO，写入df数据流
    writer = pd.ExcelWriter(byte_file, engine='xlsxwriter')  # ExcelWriter这个函数需要传一个路径参数，我们使用BytesIO类接收

    df.to_excel(excel_writer=writer, index=False, encoding="utf-8", sheet_name='sheet1')
    writer.save()
    writer.close()
    excel_bin_data = byte_file.getvalue()

    return Response(
        excel_bin_data,
        status=200,
        headers=generate_download_headers("xlsx"),
        mimetype="application/x-xls",
    )

#登记记录保存
@app.route('/download_jilu')
def download_jilu():
    info_jilu = Jltable.query.all()
    jilu_data = []
    for i in info_jilu:
        xh = i.id  #序号
        date = i.date
        name = i.name
        num = i.num
        site = i.site
        people = i.people
        in_out = i.in_out
        jilu_data.append([xh,date,name,num,site,people,in_out])
    df = pd.DataFrame(jilu_data)
    df.columns=['序号','日期','物品名','重量','位置','登记人','出入库']

    byte_file = io.BytesIO()  # BytesIO实现了在内存中读写bytes，创建一个BytesIO，写入df数据流
    writer = pd.ExcelWriter(byte_file, engine='xlsxwriter')  # ExcelWriter这个函数需要传一个路径参数，我们使用BytesIO类接收

    df.to_excel(excel_writer=writer, index=False, encoding="utf-8", sheet_name='sheet1')
    writer.save()
    writer.close()
    excel_bin_data = byte_file.getvalue()

    return Response(
        excel_bin_data,
        status=200,
        headers=generate_download_headers("xlsx"),
        mimetype="application/x-xls",
    )


#获取本页数据的保存原始记录保存
@app.route('/download_yuanshi_page')
def download():
    #先获取在那一页
    page_num = request.args.get('id')
    page = request.args.get('page', '%s')%page_num
    page = int(page)
    info_yuanshis = Ystable.query.order_by(Ystable.id).paginate(page, 18)
    # 获取本页的数据
    page_yuanshi_content = info_yuanshis.items
    yuanshi_page_data = []
    for i in page_yuanshi_content:
        xh = i.id  # 序号
        date = i.date
        name = i.name
        num = i.num
        site = i.site
        yuanshi_page_data.append([xh, date, name, num, site])
    df = pd.DataFrame(yuanshi_page_data)
    df.columns = ['序号', '日期', '物品名', '重量', '位置']

    byte_file = io.BytesIO()  # BytesIO实现了在内存中读写bytes，创建一个BytesIO，写入df数据流
    writer = pd.ExcelWriter(byte_file, engine='xlsxwriter')  # ExcelWriter这个函数需要传一个路径参数，我们使用BytesIO类接收

    df.to_excel(excel_writer=writer, index=False, encoding="utf-8", sheet_name='sheet1')
    writer.save()
    writer.close()
    excel_bin_data = byte_file.getvalue()

    return Response(
        excel_bin_data,
        status=200,
        headers=generate_download_headers("xlsx"),
        mimetype="application/x-xls",
    )



#获取本页数据的保存登记记录保存
@app.route('/download_jilu_page')
def download_jilu_page():
    #先获取在那一页
    page_num = request.args.get('id')
    page = request.args.get('page', '%s')%page_num
    page = int(page)
    info_jilus = Jltable.query.order_by(Jltable.id).paginate(page, 18)
    # 获取本页的数据
    page_jilu_content = info_jilus.items
    jilu_page_data = []
    for i in page_jilu_content:
        xh = i.id  # 序号
        date = i.date
        name = i.name
        num = i.num
        site = i.site
        people = i.people
        in_out = i.in_out
        jilu_page_data.append([xh, date, name, num, site, people, in_out])
    df = pd.DataFrame(jilu_page_data)
    df.columns = ['序号', '日期', '物品名', '重量', '位置', '登记人', '出入库']

    byte_file = io.BytesIO()  # BytesIO实现了在内存中读写bytes，创建一个BytesIO，写入df数据流
    writer = pd.ExcelWriter(byte_file, engine='xlsxwriter')  # ExcelWriter这个函数需要传一个路径参数，我们使用BytesIO类接收

    df.to_excel(excel_writer=writer, index=False, encoding="utf-8", sheet_name='sheet1')
    writer.save()
    writer.close()
    excel_bin_data = byte_file.getvalue()

    return Response(
        excel_bin_data,
        status=200,
        headers=generate_download_headers("xlsx"),
        mimetype="application/x-xls",
    )







if __name__ == '__main__':
    app.run(debug=True)