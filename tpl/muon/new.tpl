%from api import body_render
%include("tpl/{}/header.tpl".format(template))
<center>
<div id="content">
<div id="menu">
<h1>IDEC</h1>
<ul id="buttons">
<li><a href="/">Главная</a></li> |
<li><a href="/s/fetch">Синхронизация</a></li> |
<li><a href="/settings">Настройки</a></li>
</ul>
</div><br>
%include("tpl/{}/sidebar.tpl".format(template), echoareas=echoareas, fechoareas=fechoareas)
<div id="messages">
%if messages:
<h2>Новые сообщения:</h2>
%for msg in messages:
<div class="message">
<div class="message-head">
%tags = msg[1].split("/")
%if "repto" in tags:
%reptoid = tags[tags.index("repto") + 1]
Ответ на <a href="/{{reptoid}}">{{reptoid}}</a><br>
%end
<a target="new" href="/{{msg[0]}}">#</a> {{msg[4]}} [{{msg[5]}}] 🠞 {{msg[6]}} ({{msg[3]}}) в <a href="/{{msg[2]}}">{{msg[2]}}</a><br>
{{msg[7]}}
</div>
%msg = "\n".join(msg[9:])
{{!body_render(msg)}}
</div>
%end
%else:
<h2>Новых сообщений нет</h2>
%end
%if files:
<h2>Новые файлы:</h2>
%f = ""
%for file in files:
%if f != file[0]:
%if f != "":
</ul>
%end
%f = file[0]
<h3>{{f}}:</h3>
<ul>
%end
<li><a target="new" href="/file/{{f}}/{{file[1]}}" title="{{file[2]}}">{{file[1]}}</a></li>
%end
%if f != "":
</ul>
%end
%else:
<h2>Новых файлов нет</h2>
%end
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))