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
%include("tpl/{}/paginator.tpl".format(template), page=page, pages=pages)
</div>
<br>
<table id="files" cellpadding="5" cellspacing="0" border="1">
%for msg in messages:
<tr>
<td class="fit-column">{{msg[4]}}</td>
<td><a href="/{{msg[0]}}">{{msg[1]}}</a></td>
<td class="fit-column">{{msg[2]}} 🠞 {{msg[3]}}</td>
</tr>
%end
%else:
<tr><td><h2>Нет сообщений в {{echo[0]}}</h2></td></tr>
%end
</table>
<br>
%if messages:
<div>
%include("tpl/{}/paginator.tpl".format(template), page=page, pages=pages)
</div>
%end
</div>
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))