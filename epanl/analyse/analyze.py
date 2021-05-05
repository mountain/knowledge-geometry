import re

with open('concept.txt', 'w') as f:
    with open('../epanlz.tex', encoding='utf-8') as g:
        for ln in g:
            is_empty = True
            for wd in re.findall(r"\\gls\{\w+\}", ln, re.S):
                f.write('%s, ' % wd[5:-1])
                is_empty = False
            if not is_empty:
                f.write('\n')
