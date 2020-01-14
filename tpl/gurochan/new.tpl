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
<div id="sidebar">
<b>Конференции:</b>
<ul id="echolist">
%for echoarea in echoareas:
<li><a href="/{{echoarea[0]}}" title="{{echoarea[1]}}">{{echoarea[0]}}</a></li>
%end
</ul>
</div>
<div id="messages">
%if messages:
<h2>Новые сообщения:</h2>
%for msg in messages:
<div class="message">
<div class="message-head">
%tags = msg[0].split("/")
%if "repto" in tags:
%reptoid = tags[tags.index("repto") + 1]
Ответ на <a href="/{{reptoid}}">{{reptoid}}</a><br>
%end
<a href="/{{msg[0]}}">#</a> {{msg[3]}} [{{msg[4]}}] 🠞 {{msg[5]}} ({{msg[2]}}) в <a href="/{{msg[1]}}">{{msg[1]}}</a><br>
{{msg[6]}}
</div>
%msg = "\n".join(msg[8:])
{{!body_render(msg)}}
</div>
%end
%else:
<h2>Новых сообщений нет</h2>
%end
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))