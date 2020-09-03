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
<table id="files" cellpadding="5" cellspacing="0" border="1">
%for f in files:
<tr>
<td>
%images = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
%if any(x in f[1] for x in images):
<a target="_blank" href="/file/{{fechoarea}}/{{f[1]}}"><img src="/file/{{fechoarea}}/{{f[1]}}" height="200"><br>{{f[1]}}</a>
%else:
<a target="_blank" href="/file/{{fechoarea}}/{{f[1]}}">{{f[1]}}</a>
%end
</td>
<td valign="top">{{f[4]}}</td>
%end
</tr>
</table>
%else:
Нет файлов.
%end
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))