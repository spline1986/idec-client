<div id="sidebar">
%if echoareas:
<b>Конференции:</b>
<ul>
%for echoarea in echoareas:
<li><a href="/{{echoarea[0]}}" title="{{echoarea[1]}}">{{echoarea[0]}}</a></li>
%end
</ul>
%end
%if fechoareas:
<b>Файловые конференции:</b>
<ul>
%for fechoarea in fechoareas:
<li><a href="/fecho/{{fechoarea[0]}}" title="{{fechoarea[1]}}">{{fechoarea[0]}}</a></li>
%end
</ul>
%end
</div>