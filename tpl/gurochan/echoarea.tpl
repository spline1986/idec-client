%from api import body_render
%include("tpl/{}/header.tpl".format(template))
<center>
<div id="content">
<div id="menu">
<h1>IDEC</h1>
%include("tpl/{}/menu.tpl".format(template), page=-1)
</div><br>
%include("tpl/{}/sidebar.tpl".format(template), echoareas=echoareas, fechoareas=fechoareas)
<div id="messages">
%if messages:
<h2>{{echo[0]}}: {{echo[1]}}</h2>
<div>
&nbsp;<div class="new-message">
<a href="/list/{{echo[0]}}">Список сообщений</a> | <a href="/new_message/{{echo[0]}}">Новое сообщение</a>
</div>
%include("tpl/{}/paginator.tpl".format(template), page=page, pages=pages)
</div>
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
<div>
&nbsp;<a class="new_message" href="/new_message/{{echo[0]}}">Новое сообщение</a>
</div>
%end
<br>
%if messages:
<div>
&nbsp<a href="/list/{{echo[0]}}">Список сообщений</a> | <a class="new_message" href="/new_message/{{echo[0]}}">Новое сообщение</a>
%include("tpl/{}/paginator.tpl".format(template), page=page, pages=pages)
</div>
%end
</div>
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))