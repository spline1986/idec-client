%if pages > 2:

%st = page - 4
%if st < 1:
%st = 1
%end

%en = page + 5
%if en > pages:
%en = pages + 1
%end

%if st > 1:
<a href="/{{echo[0]}}/1">1</a>
.
.
.
%end

%for p in range(st, en):
%if page == p:
{{p}}
%else:
<a href="/{{echo[0]}}/{{p}}">{{p}}</a>
%end
%end

%if en < pages:
.
.
.
<a href="/{{echo[0]}}">{{pages - 1}}</a>
%end
%end