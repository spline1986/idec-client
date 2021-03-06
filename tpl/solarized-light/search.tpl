%from api import body_render
%include("tpl/{}/header.tpl".format(template))
<center>
<div id="content">
<div id="menu">
<h1>IDEC</h1>
%include("tpl/{}/menu.tpl".format(template), page=3)
</div><br>
%include("tpl/{}/sidebar.tpl".format(template), echoareas=echoareas, fechoareas=fechoareas)
<div id="messages">
%include("tpl/{}/search_form.tpl".format(template), echoareas=echoareas, echoarea=echoarea, text=text)
%if messages:
<h2>Результаты поиска</h2>
%for msg in messages:
<div class="message">
<div class="message-head">
<a href="/{{msg[0]}}">#</a>
{{msg[1][3]}} [{{msg[1][4]}}] 🠞 {{msg[1][5]}} ({{msg[1][2]}}) в <a href="/{{msg[1][1]}}">{{msg[1][1]}}</a><br>
{{msg[1][6]}}
</div>
%msg = "\n".join(msg[1][7:])
{{!body_render(msg)}}
</div>
%end
%end
%end
</div>
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))