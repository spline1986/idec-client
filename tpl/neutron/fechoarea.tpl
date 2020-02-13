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
<h2>Файлы в {{fechoarea}}</h2>
%if files:
<table cellpadding="5" cellspacing="0" border="1">
%for f in files:
<tr>
<td><a target="_blank" href="/file/{{fechoarea}}/{{f[1]}}">{{f[1]}}</a></</td>
<td>{{f[4]}}</td>
</tr>
%end
</table>
%else:
Нет файлов.
%end
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))