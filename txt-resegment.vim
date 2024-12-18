normal ggVGJ
%s/  / /ge
%s/\. /\.\r/ge
%s/? /\?\r/ge
%s/, because/,\rbecause/ge
%s/ because/\rbecause/ge
%s/, so/,\rso/ge
%s/ so /\rso /ge
%s/, but/,\rbut/ge
%s/ but /\rbut /ge
%s/, and/,\rand/ge
%s/ and then/\rand then/ge
%s/, then/,\rthen/ge
%s/, which/,\rwhich/ge
%s/, what/,\rwhat/ge
%s/, when/,\rwhen/ge
%s/, where/,\rwhere/ge
%s/, why/,\rwhy/ge
%s/, how/,\rhow/ge
%s/, instead of/,\rinstead of/ge
%s/; /;\r/ge
%s/^ //ge
silent! g/^$/d
w
