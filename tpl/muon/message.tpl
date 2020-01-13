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
%if message:
<h2>Сообщение {{msgid}}</h2>
<div class="message">
<div class="message-head">
%tags = message[0].split("/")
%if "repto" in tags:
%reptoid = tags[tags.index("repto") + 1]
Ответ на <a href="/{{reptoid}}">{{reptoid}}</a><br>
%end
{{message[3]}} [{{message[4]}}] 🠞 {{message[5]}} ({{message[2]}}) в <a href="/{{message[1]}}">{{message[1]}}</a><br>
{{message[6]}}
</div>
%message = "\n".join(message[7:])
{{!body_render(message)}}
</div>
%end
</div>
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))