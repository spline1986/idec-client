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
<h2>Сообщение сохранено</h2>
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))