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
%include("tpl/{}/sidebar.tpl".format(template), echoareas=echoareas, fechoareas=fechoareas)
<div id="messages">
<h2>Файлы в {{fechoarea}}</h2>
%if files:
<ul>
%for f in files:
<li><a target="_blank" href="/file/{{fechoarea}}/{{f[1]}}" title="{{f[4]}}">{{f[1]}}</a></li>
%end
</ul>
%else:
Нет файлов.
%end
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))