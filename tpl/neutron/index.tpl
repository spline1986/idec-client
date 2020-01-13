%from api import body_render
%include("tpl/{}/header.tpl".format(template))
<center>
<div id="content">
<div id="menu">
<h1>IDEC</h1>
<ul id="buttons">
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
<h2>Последние сообщения:</h2>
%for msg in messages:
<h3><a href="/{{msg[1]}}">{{msg[1]}}</a> [{{counts[msg[1]]}}]</h3>
<div class="message">
<div class="message-head">
{{msg[3]}} [{{msg[4]}}] 🠞 {{msg[5]}} ({{msg[2]}})<br>
{{msg[6]}}
</div>
%msg = "\n".join(msg[7:])
{{!body_render(msg)}}
</div>
%end
%end
</div>
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))