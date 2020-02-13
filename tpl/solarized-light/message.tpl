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
</div>
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))