%from api import body_render
%include("tpl/{}/header.tpl".format(template))
<center>
<div id="content">
<div id="menu">
<h1>IDEC</h1>
<ul id="buttons">
<li><a href="/">Главная</a></li> |
<li><a href="/s/fetch">Синхронизация</a></li> |
<li><a href="/new">Новые сообщения</a></li> |
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
<h2>{{echo[0]}}: {{echo[1]}}</h2>
<a id="new_message" href="/new_message/{{echo[0]}}">Новое сообщение</a>
%include("tpl/{}/paginator.tpl".format(template), page=page, pages=pages)
%for msg in messages:
<div class="message">
<div class="message-head">
<div class="reply">
<a href="/reply/{{echo[0]}}/{{msg[0]}}">Ответить</a>
</div>
%tags = msg[1].split("/")
%if "repto" in tags:
%reptoid = tags[tags.index("repto") + 1]
Ответ на <a href="/{{reptoid}}">{{reptoid}}</a><br>
%end
<a href="/{{msg[0]}}">#</a> {{msg[4]}} [{{msg[5]}}] 🠞 {{msg[6]}} ({{msg[3]}})<br>
{{msg[7]}}
</div>
%msg = "\n".join(msg[8:])
{{!body_render(msg)}}
</div>
%end
%else:
<h2>Нет сообщений в {{echo[0]}}</h2>
<a href="/new_message/{{echo[0]}}">Новое сообщение</a>
%end
<br>
%include("tpl/{}/paginator.tpl".format(template), page=page, pages=pages)
</div>
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))