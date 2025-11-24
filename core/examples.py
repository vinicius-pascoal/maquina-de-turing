EXAMPLES = {
    "1. Paridade de 1s (Par/Ímpar)": """states: qeven,qodd,qaccept,qreject
blank: _
start: qeven
accept: qaccept
reject: qreject
transitions:
qeven,0 -> qeven,0,R
qeven,1 -> qodd,1,R
qeven,_ -> qaccept,_,N
qodd,0 -> qodd,0,R
qodd,1 -> qeven,1,R
qodd,_ -> qreject,_,N""",

    "2. Palíndromo Simples (ex: 010)": """states: q0,q1,q2,q3,q4,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q1,_,R
q0,1 -> q2,_,R
q0,_ -> qaccept,_,N
q1,0 -> q1,0,R
q1,1 -> q1,1,R
q1,_ -> q3,_,L
q2,0 -> q2,0,R
q2,1 -> q2,1,R
q2,_ -> q4,_,L
q3,0 -> q0,_,L
q3,1 -> qreject,1,N
q3,_ -> q0,_,L
q4,1 -> q0,_,L
q4,0 -> qreject,0,N
q4,_ -> q0,_,L""",

    "3. Duplicador (0 -> 00, 1 -> 11)": """states: q0,q1,q2,q3,q4,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q1,_,R
q0,1 -> q3,_,R
q0,_ -> qaccept,_,N
q1,0 -> q1,0,R
q1,1 -> q1,1,R
q1,_ -> q2,0,L
q2,0 -> q2,0,L
q2,1 -> q2,1,L
q2,_ -> q0,_,R
q3,0 -> q3,0,R
q3,1 -> q3,1,R
q3,_ -> q4,1,L
q4,0 -> q4,0,L
q4,1 -> q4,1,L
q4,_ -> q0,_,R""",

    "4. Complemento (0 -> 1, 1 -> 0)": """states: q0,qback,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q0,1,R
q0,1 -> q0,0,R
q0,_ -> qback,_,L
qback,0 -> qback,0,L
qback,1 -> qback,1,L
qback,_ -> qaccept,_,N""",

    "5. Aceita 0^n1^n (mesma qtd 0 e 1)": """states: q0,q1,q2,qcheck,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,X -> q0,X,R
q0,Y -> q0,Y,R
q0,0 -> q1,X,R
q0,1 -> qreject,1,N
q0,_ -> qcheck,_,L
q1,X -> q1,X,R
q1,Y -> q1,Y,R
q1,0 -> qreject,0,N
q1,1 -> q2,Y,L
q1,_ -> qreject,_,N
q2,X -> q2,X,L
q2,Y -> q2,Y,L
q2,0 -> q2,0,L
q2,1 -> q2,1,L
q2,_ -> q0,_,R
qcheck,X -> qcheck,X,R
qcheck,Y -> qcheck,Y,R
qcheck,0 -> qreject,0,N
qcheck,1 -> qreject,1,N
qcheck,_ -> qaccept,_,N""",

    "6. Aceita 0*1* (0s antes de 1s)": """states: q0,q1,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q0,0,R
q0,1 -> q1,1,R
q0,_ -> qaccept,_,N
q1,1 -> q1,1,R
q1,0 -> qreject,0,N
q1,_ -> qaccept,_,N""",

    "7. Somador Unário (111+11=11111)": """states: q0,q1,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,1 -> q0,1,R
q0,+ -> q1,1,R
q0,_ -> qaccept,_,N
q1,1 -> q1,1,R
q1,_ -> qaccept,_,N""",

    "8. Multiplicador por 2 (Binário)": """states: q0,q1,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q0,0,R
q0,1 -> q0,1,R
q0,_ -> q1,0,N
q1,_ -> qaccept,_,N""",

    "9. Contador de Símbolos (marca fim)": """states: q0,q1,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q0,0,R
q0,1 -> q0,1,R
q0,_ -> q1,#,N
q1,# -> qaccept,#,N""",

    "10. Reconhece 1*0*1* (padrão)": """states: q0,q1,q2,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,1 -> q0,1,R
q0,0 -> q1,0,R
q0,_ -> qaccept,_,N
q1,0 -> q1,0,R
q1,1 -> q2,1,R
q1,_ -> qaccept,_,N
q2,1 -> q2,1,R
q2,0 -> qreject,0,N
q2,_ -> qaccept,_,N""",

    "11. Apaga Tudo (limpa fita)": """states: q0,qback,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q0,_,R
q0,1 -> q0,_,R
q0,_ -> qback,_,L
qback,_ -> qback,_,L
qback,0 -> qaccept,_,N
qback,1 -> qaccept,_,N""",

    "12. Shift Right (desloca direita)": """states: q0,q1,q2,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q1,_,R
q0,1 -> q2,_,R
q0,_ -> qaccept,_,N
q1,0 -> q1,0,R
q1,1 -> q1,1,R
q1,_ -> qaccept,0,N
q2,0 -> q2,0,R
q2,1 -> q2,1,R
q2,_ -> qaccept,1,N"""
}
