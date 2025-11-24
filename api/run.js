import { TuringMachine } from '../core/turing_machine.js';

export default function handler(req, res) {
  try {
    const { machine, steps = 1, max_steps = 1000 } = req.body;

    if (!machine) {
      return res.status(400).json({
        success: false,
        error: 'Dados da máquina ausentes'
      });
    }

    const tm = TuringMachine.fromDict(machine);

    let stepsExecuted = 0;

    if (steps === -1) {
      // Rodar até parar
      stepsExecuted = tm.run(max_steps);
    } else {
      // Rodar N passos
      for (let i = 0; i < Math.min(steps, max_steps); i++) {
        if (tm.halted) break;
        tm.step();
        stepsExecuted++;
      }
    }

    return res.status(200).json({
      success: true,
      machine: tm.toDict(),
      steps_executed: stepsExecuted
    });
  } catch (e) {
    return res.status(500).json({
      success: false,
      error: `Erro no servidor: ${e.message}`
    });
  }
}
