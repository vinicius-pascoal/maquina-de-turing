const EXAMPLES = {
  "0^n1^n (mesma quantidade de 0 e 1)": `states: q0,q1,q2,qcheck,qaccept,qreject
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
qcheck,_ -> qaccept,_,N`,

  "Paridade de 1s (aceita se quantidade for par)": `states: qeven,qodd,qaccept,qreject
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
qodd,_ -> qreject,_,N`,

  "Linguagem 0*1* (todos 0 antes dos 1)": `states: q0,q1,qaccept,qreject
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
q1,_ -> qaccept,_,N`,

  "Incremento unário (adiciona um 1 ao final)": `states: q0,qwrite,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,1 -> q0,1,R
q0,_ -> qwrite,_,L
qwrite,_ -> qaccept,1,N`,

  "Reconhece cadeia vazia apenas": `states: q0,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,_ -> qaccept,_,N
q0,0 -> qreject,0,N
q0,1 -> qreject,1,N`,

  "Duplicador (01 -> 0101)": `states: q0,q1,q2,q3,q4,qaccept,qreject
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
q4,_ -> q0,_,R`
};

export default function handler(req, res) {
  res.status(200).json({
    success: true,
    examples: EXAMPLES
  });
}
