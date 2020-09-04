%from api import body_render
%include("tpl/{}/header.tpl".format(template))
<center>
<div id="content">
<div id="menu">
<h1>IDEC</h1>
%include("tpl/{}/menu.tpl".format(template), page=0)
</div><br>
%include("tpl/{}/sidebar.tpl".format(template), echoareas=echoareas, fechoareas=fechoareas)
<div id="messages">
%if messages:
<h2>Последние сообщения:</h2>
%for msg in messages:
<div class="message">
<div class="message-head">
<div class="reply">
<a href="/reply/{{msg[2]}}/{{msg[0]}}">Ответить</a>
</div>
<a href="/{{msg[0]}}">#</a> {{msg[3]}} [{{msg[4]}}] 🠞 {{msg[5]}} ({{msg[2]}}) в <a href="/{{msg[1]}}">{{msg[1]}}</a><br>
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